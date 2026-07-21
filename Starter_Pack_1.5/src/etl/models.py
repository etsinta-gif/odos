"""ETL model stubs for IMP-1.5."""

from dataclasses import dataclass

@dataclass
class ETL_ImportBatch:
    BatchGUID: str
    CompanyID: int
    SourceSystem: str
    FileName: str
    ImportStatus: str
    IsAtomicTransaction: bool
    IsComplete: bool
    ImportDateTime: str
    TotalRows: int
    SuccessfulRows: int
    FailedRows: int

@dataclass
class ETL_StagingRawData:
    StagingID: int
    BatchGUID: str
    CompanyID: int
    TableName: str
    ColumnName: str
    SourceRowNumber: int
    SourceColumnName: str
    SourceValue: str
    TargetField: str
    StoredValue: str
    ValidationStatus: str
    ErrorMessage: str
    ImportDateTime: str

@dataclass
class ETL_ErrorLog:
    ErrorLogID: int
    BatchGUID: str
    CompanyID: int
    TableName: str
    RowNumber: int
    ColumnName: str
    ErrorType: str
    ErrorMessage: str
    ErrorDateTime: str
