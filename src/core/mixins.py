from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class TenantMixin:
    @declared_attr
    def company_id(cls):
        return Column(Integer, nullable=False, index=True)

    @classmethod
    def apply_tenant_filter(cls, query, company_id: int):
        if hasattr(cls, "company_id"):
            return query.filter(cls.company_id == company_id)
        return query
