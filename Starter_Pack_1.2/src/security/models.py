"""Security model stubs for IMP-1.2."""

from dataclasses import dataclass

@dataclass
class SEC_Role:
    RoleID: int
    RoleName: str
    Description: str
    IsSystem: bool
    CompanyID: int

@dataclass
class SEC_Permission:
    PermissionID: int
    Resource: str
    Action: str
    Description: str

@dataclass
class SEC_User:
    UserID: int
    CompanyID: int
    Username: str
    PasswordHash: str
    RoleID: int
    IsActive: bool

@dataclass
class SEC_AuditTrail:
    AuditID: int
    TableName: str
    RecordID: int
    Action: str
    OldValues_JSON: str
    NewValues_JSON: str
    ChangedByUserID: int
    ChangeDateTime: str
    CompanyID: int
