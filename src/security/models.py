from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from src.core.database import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("sec_users.user_id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("sec_roles.role_id"), primary_key=True),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("sec_roles.role_id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("sec_permissions.permission_id"), primary_key=True),
)


class SEC_Role(Base):
    __tablename__ = "sec_roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("SEC_User", secondary=user_roles, back_populates="roles")
    permissions = relationship("SEC_Permission", secondary=role_permissions, back_populates="roles")


class SEC_Permission(Base):
    __tablename__ = "sec_permissions"
    __table_args__ = (UniqueConstraint("resource", "action", name="uq_sec_permissions_resource_action"),)

    permission_id = Column(Integer, primary_key=True, index=True)
    resource = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roles = relationship("SEC_Role", secondary=role_permissions, back_populates="permissions")


class SEC_User(Base):
    __tablename__ = "sec_users"

    user_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    roles = relationship("SEC_Role", secondary=user_roles, back_populates="users")

    def has_role(self, role_name: str) -> bool:
        return any(role.role_name == role_name for role in self.roles)


class SEC_LoginHistory(Base):
    __tablename__ = "sec_login_history"

    login_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("sec_users.user_id"), nullable=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    username = Column(String(50), nullable=True, index=True)
    login_at = Column(DateTime, default=datetime.utcnow)
    auth_status = Column(String(20), nullable=False, default="SUCCESS")
    source_ip = Column(String(100), nullable=True)
    user_agent = Column(String(255), nullable=True)
    failure_reason = Column(String(100), nullable=True)


class SEC_RefreshToken(Base):
    __tablename__ = "sec_refresh_tokens"

    token_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("sec_users.user_id"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    revoked_at = Column(DateTime, nullable=True)
    replaced_by_hash = Column(String(255), nullable=True)

    user = relationship("SEC_User")
