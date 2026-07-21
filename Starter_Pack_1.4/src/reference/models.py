"""Reference model stubs for IMP-1.4."""

from dataclasses import dataclass

@dataclass
class REF_Country:
    CountryID: int
    CountryCode: str
    CountryName: str
    IsActive: bool

@dataclass
class REF_State:
    StateID: int
    StateCode: str
    StateName: str
    CountryID: int
    IsActive: bool

@dataclass
class REF_District:
    DistrictID: int
    DistrictName: str
    StateID: int
    IsActive: bool
