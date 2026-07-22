from decimal import Decimal

from src.etl.services.cross_verify import CrossVerificationService, VerificationDefaults


def test_verify_revenue_detects_gst_tds_mismatch() -> None:
    svc = CrossVerificationService()
    defaults = VerificationDefaults(default_gst_rate=Decimal("18"), default_tds_rate=Decimal("2"))

    result = svc.verify_revenue(
        {
            "reported_amount": 1000,
            "reported_gst": 100,
            "reported_tds": 10,
        },
        defaults,
    )

    assert result["system_gst"] == Decimal("180.00")
    assert result["system_tds"] == Decimal("20.00")
    assert result["gst_match"] is False
    assert result["tds_match"] is False
    assert len(result["red_flags"]) == 2


def test_verify_commission_flags_exceeds_max() -> None:
    svc = CrossVerificationService()
    defaults = VerificationDefaults(
        default_gst_rate=Decimal("18"),
        default_tds_rate=Decimal("5"),
        max_commission=Decimal("2500"),
    )

    result = svc.verify_commission(
        {
            "reported_commission": 3000,
            "reported_gst": 540,
            "reported_tds": 150,
        },
        defaults,
    )

    assert result["system_gst"] == Decimal("540.00")
    assert result["system_tds"] == Decimal("150.00")
    assert result["gst_match"] is True
    assert result["tds_match"] is True
    assert result["exceeds_max"] is True
    assert any(flag["category"] == "commission" for flag in result["red_flags"])


def test_verify_revenue_matching_values_yields_no_flags() -> None:
    svc = CrossVerificationService()
    defaults = VerificationDefaults(default_gst_rate=Decimal("18"), default_tds_rate=Decimal("2"))

    result = svc.verify_revenue(
        {
            "reported_amount": 1000,
            "reported_gst": 180,
            "reported_tds": 20,
            "reported_net": 800,
        },
        defaults,
    )

    assert result["gst_match"] is True
    assert result["tds_match"] is True
    assert result["red_flags"] == []


def test_verify_commission_matching_values_and_under_limit() -> None:
    svc = CrossVerificationService()
    defaults = VerificationDefaults(
        default_gst_rate=Decimal("18"),
        default_tds_rate=Decimal("5"),
        max_commission=Decimal("5000"),
    )

    result = svc.verify_commission(
        {
            "reported_commission": 3000,
            "reported_gst": 540,
            "reported_tds": 150,
            "reported_net": 2310,
        },
        defaults,
    )

    assert result["gst_match"] is True
    assert result["tds_match"] is True
    assert result["exceeds_max"] is False
    assert result["red_flags"] == []
