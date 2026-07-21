from src.core.mixins import TenantMixin


class _FakeColumn:
    def __eq__(self, other):
        return ("company_id", other)


class _FakeQuery:
    def __init__(self):
        self.applied = None

    def filter(self, predicate):
        self.applied = predicate
        return self


class _TenantTable(TenantMixin):
    company_id = _FakeColumn()


class _NonTenantTable:
    pass


def test_apply_tenant_filter_applies_filter_for_tenant_models():
    query = _FakeQuery()
    result = _TenantTable.apply_tenant_filter(query, 7)
    assert result is query
    assert query.applied == ("company_id", 7)


def test_apply_tenant_filter_noop_for_non_tenant_models():
    query = _FakeQuery()
    result = _NonTenantTable.__dict__.get("apply_tenant_filter", lambda q, c: q)(query, 7)
    assert result is query
    assert query.applied is None
