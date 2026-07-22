from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from src.transactions.models import ETL_RedFlag


@dataclass
class VerificationDefaults:
    default_gst_rate: Decimal = Decimal("0")
    default_tds_rate: Decimal = Decimal("0")
    max_commission: Decimal | None = None


class CrossVerificationService:
    """Cross-verifies reported values against configured default rates and limits."""

    def __init__(self, tolerance: Decimal | None = None):
        self.tolerance = tolerance or Decimal("0.01")

    @staticmethod
    def _d(value: Any, default: str = "0") -> Decimal:
        if value in (None, ""):
            return Decimal(default)
        try:
            return Decimal(str(value))
        except Exception:
            return Decimal(default)

    @staticmethod
    def _q2(value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def verify_revenue(self, row_data: dict[str, Any], defaults: VerificationDefaults) -> dict[str, Any]:
        reported_amount = self._d(row_data.get("reported_amount") or row_data.get("base_revenue_amount") or row_data.get("amount"))
        reported_gst = self._d(row_data.get("reported_gst") or row_data.get("gst_amount"))
        reported_tds = self._d(row_data.get("reported_tds") or row_data.get("tds_amount"))

        gst_rate = self._d(defaults.default_gst_rate)
        tds_rate = self._d(defaults.default_tds_rate)

        system_gst = self._q2(reported_amount * (gst_rate / Decimal("100")))
        system_tds = self._q2(reported_amount * (tds_rate / Decimal("100")))

        gst_match = abs(reported_gst - system_gst) <= self.tolerance
        tds_match = abs(reported_tds - system_tds) <= self.tolerance

        flags: list[dict[str, str]] = []
        if not gst_match:
            flags.append(
                {
                    "severity": "WARNING",
                    "category": "gst",
                    "field": "reported_gst",
                    "message": f"GST mismatch: reported {reported_gst}, expected {system_gst}",
                    "reported_value": str(reported_gst),
                    "expected_value": str(system_gst),
                }
            )
        if not tds_match:
            flags.append(
                {
                    "severity": "WARNING",
                    "category": "tds",
                    "field": "reported_tds",
                    "message": f"TDS mismatch: reported {reported_tds}, expected {system_tds}",
                    "reported_value": str(reported_tds),
                    "expected_value": str(system_tds),
                }
            )

        return {
            "reported_amount": reported_amount,
            "reported_gst": reported_gst,
            "reported_tds": reported_tds,
            "reported_net": self._d(row_data.get("reported_net") or row_data.get("net_amount")),
            "system_gst": system_gst,
            "system_tds": system_tds,
            "gst_match": gst_match,
            "tds_match": tds_match,
            "red_flags": flags,
        }

    def verify_commission(self, row_data: dict[str, Any], defaults: VerificationDefaults) -> dict[str, Any]:
        reported_commission = self._d(
            row_data.get("reported_commission")
            or row_data.get("gross_commission_amount")
            or row_data.get("base_commission_amount")
            or row_data.get("amount")
        )
        reported_gst = self._d(row_data.get("reported_gst") or row_data.get("gst_amount"))
        reported_tds = self._d(row_data.get("reported_tds") or row_data.get("tds_amount"))

        gst_rate = self._d(defaults.default_gst_rate)
        tds_rate = self._d(defaults.default_tds_rate)

        system_gst = self._q2(reported_commission * (gst_rate / Decimal("100")))
        system_tds = self._q2(reported_commission * (tds_rate / Decimal("100")))

        gst_match = abs(reported_gst - system_gst) <= self.tolerance
        tds_match = abs(reported_tds - system_tds) <= self.tolerance

        max_commission = defaults.max_commission
        exceeds_max = bool(max_commission is not None and reported_commission > self._d(max_commission))

        flags: list[dict[str, str]] = []
        if exceeds_max:
            flags.append(
                {
                    "severity": "CRITICAL",
                    "category": "commission",
                    "field": "reported_commission",
                    "message": f"Commission exceeds max: reported {reported_commission}, max {max_commission}",
                    "reported_value": str(reported_commission),
                    "expected_value": str(max_commission),
                }
            )
        if not gst_match:
            flags.append(
                {
                    "severity": "WARNING",
                    "category": "gst",
                    "field": "reported_gst",
                    "message": f"GST mismatch on commission: reported {reported_gst}, expected {system_gst}",
                    "reported_value": str(reported_gst),
                    "expected_value": str(system_gst),
                }
            )
        if not tds_match:
            flags.append(
                {
                    "severity": "WARNING",
                    "category": "tds",
                    "field": "reported_tds",
                    "message": f"TDS mismatch on commission: reported {reported_tds}, expected {system_tds}",
                    "reported_value": str(reported_tds),
                    "expected_value": str(system_tds),
                }
            )

        return {
            "reported_commission": reported_commission,
            "reported_gst": reported_gst,
            "reported_tds": reported_tds,
            "reported_net": self._d(row_data.get("reported_net") or row_data.get("net_amount")),
            "system_gst": system_gst,
            "system_tds": system_tds,
            "gst_match": gst_match,
            "tds_match": tds_match,
            "exceeds_max": exceeds_max,
            "red_flags": flags,
        }

    @staticmethod
    def build_red_flag(
        company_id: int,
        batch_guid: str | None,
        record_type: str,
        record_id: int,
        payload: dict[str, str],
    ) -> ETL_RedFlag:
        return ETL_RedFlag(
            company_id=company_id,
            batch_guid=batch_guid,
            record_type=record_type,
            record_id=record_id,
            severity=payload["severity"],
            category=payload["category"],
            message=payload["message"],
            field=payload.get("field"),
            reported_value=payload.get("reported_value"),
            expected_value=payload.get("expected_value"),
            status="OPEN",
        )
