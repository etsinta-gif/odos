"""Configuration model stubs for IMP-1.3."""

from dataclasses import dataclass

@dataclass
class CFG_CompanySettings:
    CompanyID: int
    DefaultCurrency: str
    DefaultDateFormat: str
    Timezone: str
    LogoPath: str
    ThemeColor: str
    AI_ConfidenceThreshold: float

@dataclass
class CFG_FinancialYear:
    FinancialYearID: int
    CompanyID: int
    FiscalYearStart: str
    FiscalYearEnd: str
    IsActive: bool

@dataclass
class CFG_AutoNumbering:
    AutoNumberingID: int
    CompanyID: int
    EntityType: str
    FormatString: str
    StartingNumber: int
    CurrentNumber: int
    Suffix: str
    YearSuffix: str

@dataclass
class CFG_Calendar:
    CalendarID: int
    CompanyID: int
    Date: str
    IsHoliday: bool
    Description: str
