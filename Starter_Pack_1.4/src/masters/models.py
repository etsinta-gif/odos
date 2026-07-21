"""Master model stubs for IMP-1.4."""

from dataclasses import dataclass

@dataclass
class MST_Company:
    CompanyID: int
    CompanyCode: str
    CompanyName: str
    PAN: str
    GSTIN: str
    CIN: str
    TAN: str
    RegisteredAddress: str
    ContactNumber: str
    Email: str
    IsActive: bool

@dataclass
class MST_Party:
    PartyID: int
    CompanyID: int
    PartyTypeID: int
    FullName: str
    PAN: str
    GSTIN: str
    KYCStatus: str

@dataclass
class MST_Customer:
    PartyID: int
    CompanyID: int
    CibilScore: int
    DateOfBirth: str
    Occupation: str
    Industry: str
    AnnualIncome: float
    CustomerSince: str
    IsActive: bool
