from __future__ import annotations

import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

import requests
from jinja2 import Template
from sqlalchemy.orm import Session

from src.alerts.models import ALERT_Notification

logger = logging.getLogger(__name__)


class NotificationEngine:
    """Send notifications via email, webhook, and in-app channels."""

    def __init__(self, session: Session, company_id: int):
        self.session = session
        self.company_id = company_id

    def render_alert_email(self, context: dict[str, Any]) -> str:
        template_path = Path(__file__).resolve().parents[2] / "templates" / "email" / "alert_email.html"
        if not template_path.exists():
            return context.get("message", "Alert notification")

        template = Template(template_path.read_text(encoding="utf-8"))
        return template.render(**context)

    def send_email(
        self,
        subject: str,
        body: str,
        recipients: list[str],
        rule_id: int | None = None,
        red_flag_id: int | None = None,
    ) -> dict[str, Any]:
        if not recipients:
            return {"success": False, "message": "No recipients provided"}

        email_from = os.getenv("EMAIL_FROM", "noreply@odos.local")
        email_host = os.getenv("EMAIL_HOST")
        email_port = int(os.getenv("EMAIL_PORT", "587"))
        email_username = os.getenv("EMAIL_USERNAME")
        email_password = os.getenv("EMAIL_PASSWORD")
        tls_enabled = os.getenv("EMAIL_USE_TLS", "1") in {"1", "true", "True"}

        delivered = True
        error_message = None

        if not email_host:
            delivered = False
            error_message = "EMAIL_HOST is not configured"
        else:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = email_from
            msg["To"] = ", ".join(recipients)
            msg.attach(MIMEText(body, "html"))

            try:
                with smtplib.SMTP(email_host, email_port, timeout=10) as server:
                    if tls_enabled:
                        server.starttls()
                    if email_username and email_password:
                        server.login(email_username, email_password)
                    server.send_message(msg)
            except Exception as exc:  # pragma: no cover - execution depends on SMTP availability
                delivered = False
                error_message = str(exc)
                logger.error("Email sending failed: %s", exc)

        for recipient in recipients:
            self.session.add(
                ALERT_Notification(
                    company_id=self.company_id,
                    rule_id=rule_id,
                    red_flag_id=red_flag_id,
                    type="EMAIL",
                    subject=subject,
                    content=body,
                    recipient_email=recipient,
                    sent_at=datetime.utcnow(),
                    delivered=delivered,
                    error_message=error_message,
                    is_read=False,
                )
            )

        self.session.commit()
        if delivered:
            return {"success": True, "message": f"Email sent to {len(recipients)} recipients"}
        return {"success": False, "message": error_message or "Email sending failed"}

    def send_webhook(
        self,
        url: str,
        payload: dict[str, Any],
        rule_id: int | None = None,
        red_flag_id: int | None = None,
    ) -> dict[str, Any]:
        if not url:
            return {"success": False, "message": "Webhook URL is required"}

        delivered = True
        error_message = None

        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            message = f"Webhook sent to {url}"
        except Exception as exc:
            delivered = False
            error_message = str(exc)
            message = error_message
            logger.error("Webhook sending failed: %s", exc)

        self.session.add(
            ALERT_Notification(
                company_id=self.company_id,
                rule_id=rule_id,
                red_flag_id=red_flag_id,
                type="WEBHOOK",
                subject="Webhook Notification",
                content=json.dumps(payload, default=str),
                payload=payload,
                sent_at=datetime.utcnow(),
                delivered=delivered,
                error_message=error_message,
                is_read=False,
            )
        )
        self.session.commit()

        return {"success": delivered, "message": message}

    def send_in_app(
        self,
        user_id: int,
        message: str,
        subject: str = "Alert Notification",
        payload: dict[str, Any] | None = None,
        rule_id: int | None = None,
        red_flag_id: int | None = None,
    ) -> dict[str, Any]:
        notification = ALERT_Notification(
            company_id=self.company_id,
            rule_id=rule_id,
            red_flag_id=red_flag_id,
            type="IN_APP",
            subject=subject,
            content=message,
            payload=payload,
            recipient_user_id=user_id,
            sent_at=datetime.utcnow(),
            delivered=True,
            is_read=False,
        )
        self.session.add(notification)
        self.session.commit()

        return {"success": True, "message": "In-app notification sent"}
