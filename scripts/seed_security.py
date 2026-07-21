import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.security.auth import get_password_hash
from src.security.models import SEC_Role, SEC_User


def seed_security() -> None:
    db = SessionLocal()
    try:
        roles = [
            ("ADMIN", "Full system access"),
            ("OPS", "Upload, view, and case operations"),
            ("FINANCE", "Financial reads and reconciliations"),
            ("AUDITOR", "Read-only operations"),
            ("MANAGER", "Operational approvals and dashboard visibility"),
        ]

        role_by_name = {}
        for role_name, desc in roles:
            role = db.query(SEC_Role).filter(SEC_Role.role_name == role_name).first()
            if not role:
                role = SEC_Role(role_name=role_name, description=desc, is_system=True)
                db.add(role)
                db.flush()
            role_by_name[role_name] = role

        admin = db.query(SEC_User).filter(SEC_User.username == "admin").first()
        if not admin:
            admin = SEC_User(
                company_id=1,
                username="admin",
                password_hash=get_password_hash("Admin@123"),
                email="admin@odos.local",
                full_name="System Administrator",
                is_active=True,
            )
            db.add(admin)
            db.flush()

        if not admin.has_role("ADMIN"):
            admin.roles.append(role_by_name["ADMIN"])

        db.commit()
        print("Security seed complete: roles + admin user")
    finally:
        db.close()


if __name__ == "__main__":
    seed_security()
