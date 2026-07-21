"""Metadata model stubs for IMP-1.3."""

from dataclasses import dataclass

@dataclass
class META_TableDefinition:
    TableDefID: int
    CompanyID: int
    TableName: str
    FriendlyName: str
    TableDescription: str
    SchemaLayer: str
    IsActive: bool
    Version: int

@dataclass
class META_FieldDefinition:
    FieldDefID: int
    TableDefID: int
    FieldName: str
    FriendlyName: str
    LogicalDataType: str
    IsMandatory: bool
    IsSensitive: bool
    MaskingRule: str
    ValidationRuleID: str
    UI_ControlType: str
    IsDimension: bool
    IsMeasure: bool
    IndexCandidate: bool
    AI_Generated: bool
    HumanApprovalRequired: bool
