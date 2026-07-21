"""Configuration for the Rule Engine."""

from typing import Any


RULE_ENGINE_CONFIG: dict[str, Any] = {
    "enable_validation": True,
    "enable_commission": True,
    "enable_gst": True,
    "enable_tds": True,
    "default_severity": "ERROR",
    "cache_rules": True,
    "cache_ttl_seconds": 300,
    "rule_execution_timeout": 30,
}
