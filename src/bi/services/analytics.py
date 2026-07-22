from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import Float, String, cast, func
from sqlalchemy.orm import Session

from src.bi.models import BI_ReportDefinition
from src.masters.models import MST_Party
from src.transactions.models import ETL_RedFlag, TRN_Commission, TRN_Payment, TRN_Revenue


class AnalyticsEngine:
    """Flexible query builder with JSON field support for BI reporting."""

    TABLE_MODELS = {
        "TRN_Revenue": TRN_Revenue,
        "TRN_Commission": TRN_Commission,
        "TRN_Payment": TRN_Payment,
        "ETL_RedFlag": ETL_RedFlag,
        "MST_Party": MST_Party,
    }

    def __init__(self, session: Session, company_id: int):
        self.session = session
        self.company_id = company_id

    @staticmethod
    def _split_json_path(field_name: str) -> tuple[str, str] | None:
        if "." not in field_name:
            return None
        left, right = field_name.split(".", 1)
        if not left or not right:
            return None
        return left, right

    def _dimension_expr(self, model: Any, field_name: str):
        parsed = self._split_json_path(field_name)
        if parsed is None:
            return getattr(model, field_name).label(field_name)
        json_col_name, json_key = parsed
        json_col = getattr(model, json_col_name)
        return cast(func.json_extract(json_col, f"$.{json_key}"), String).label(field_name)

    def _metric_expr(self, model: Any, field_name: str):
        parsed = self._split_json_path(field_name)
        if parsed is None:
            return getattr(model, field_name)
        json_col_name, json_key = parsed
        json_col = getattr(model, json_col_name)
        return cast(func.json_extract(json_col, f"$.{json_key}"), Float)

    def _filter_expr(self, model: Any, field_name: str, operator: str):
        parsed = self._split_json_path(field_name)
        if parsed is None:
            return getattr(model, field_name)
        json_col_name, json_key = parsed
        json_col = getattr(model, json_col_name)
        if operator in {"gt", "gte", "lt", "lte"}:
            return cast(func.json_extract(json_col, f"$.{json_key}"), Float)
        return cast(func.json_extract(json_col, f"$.{json_key}"), String)

    def _apply_filter(self, query, model: Any, filter_def: dict[str, Any]):
        field_name = str(filter_def.get("field") or "").strip()
        operator = str(filter_def.get("operator") or "eq").strip().lower()
        value = filter_def.get("value")
        if not field_name:
            return query

        expr = self._filter_expr(model, field_name, operator)

        if operator == "eq":
            return query.filter(expr == value)
        if operator == "neq":
            return query.filter(expr != value)
        if operator == "gt":
            return query.filter(expr > value)
        if operator == "gte":
            return query.filter(expr >= value)
        if operator == "lt":
            return query.filter(expr < value)
        if operator == "lte":
            return query.filter(expr <= value)
        if operator == "in":
            values = value if isinstance(value, list) else [value]
            return query.filter(expr.in_(values))
        if operator == "like":
            return query.filter(cast(expr, String).like(f"%{value}%"))
        if operator == "is_null":
            return query.filter(expr.is_(None))
        if operator == "is_not_null":
            return query.filter(expr.is_not(None))

        raise ValueError(f"Unsupported operator: {operator}")

    def build_query(self, definition: dict[str, Any]) -> dict[str, Any]:
        source = str(definition.get("source") or "").strip()
        if source not in self.TABLE_MODELS:
            raise ValueError(f"Unsupported source: {source}")

        model = self.TABLE_MODELS[source]
        query = self.session.query(model).filter(model.company_id == self.company_id)

        for filter_def in definition.get("filters", []):
            query = self._apply_filter(query, model, filter_def)

        dimensions: list[str] = [str(x).strip() for x in definition.get("dimensions", []) if str(x).strip()]
        metrics: list[dict[str, Any]] = list(definition.get("metrics", []))

        select_cols = []
        result_columns: list[str] = []
        group_by_cols = []
        alias_map: dict[str, Any] = {}

        for dim in dimensions:
            dim_expr = self._dimension_expr(model, dim)
            select_cols.append(dim_expr)
            group_by_cols.append(dim_expr)
            result_columns.append(dim)
            alias_map[dim] = dim_expr

        for metric in metrics:
            field_name = str(metric.get("field") or "").strip()
            if not field_name:
                continue
            agg = str(metric.get("aggregation") or "sum").strip().lower()
            alias = str(metric.get("alias") or f"{agg}_{field_name}").strip()
            if not alias:
                alias = f"{agg}_{field_name}"

            field_expr = self._metric_expr(model, field_name)
            if agg == "sum":
                col = func.sum(field_expr).label(alias)
            elif agg == "avg":
                col = func.avg(field_expr).label(alias)
            elif agg == "count":
                col = func.count(field_expr).label(alias)
            elif agg == "min":
                col = func.min(field_expr).label(alias)
            elif agg == "max":
                col = func.max(field_expr).label(alias)
            else:
                raise ValueError(f"Unsupported aggregation: {agg}")

            select_cols.append(col)
            result_columns.append(alias)
            alias_map[alias] = col

        if not select_cols:
            raise ValueError("Report definition must include dimensions and/or metrics")

        query = query.with_entities(*select_cols)
        if group_by_cols:
            query = query.group_by(*group_by_cols)

        for order in definition.get("order_by", []):
            order_field = str(order.get("field") or "").strip()
            direction = str(order.get("direction") or "asc").strip().lower()
            order_expr = alias_map.get(order_field)
            if order_expr is None:
                continue
            query = query.order_by(order_expr.desc() if direction == "desc" else order_expr.asc())

        limit = definition.get("limit")
        if limit is not None:
            query = query.limit(int(limit))

        return {
            "query": query,
            "columns": result_columns,
        }

    @staticmethod
    def _row_to_dict(row: Any, columns: list[str]) -> dict[str, Any]:
        if hasattr(row, "_mapping"):
            data = dict(row._mapping)
            return {col: data.get(col) for col in columns}
        return {columns[idx]: row[idx] for idx in range(len(columns))}

    def execute_definition(self, definition: dict[str, Any]) -> dict[str, Any]:
        built = self.build_query(definition)
        rows = built["query"].all()
        columns = built["columns"]
        data = [self._row_to_dict(row, columns) for row in rows]
        return {
            "columns": columns,
            "data": data,
            "row_count": len(data),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def execute_report(self, report_id: int, definition: dict[str, Any] | None = None) -> dict[str, Any]:
        if definition is None:
            report = (
                self.session.query(BI_ReportDefinition)
                .filter(BI_ReportDefinition.report_id == report_id)
                .filter(BI_ReportDefinition.company_id == self.company_id)
                .filter(BI_ReportDefinition.is_active == True)
                .first()
            )
            if not report:
                raise ValueError(f"Report {report_id} not found")
            definition = dict(report.definition or {})

        return self.execute_definition(definition)

    def get_trend_data(self, metric_type: str, days: int = 30) -> dict[str, Any]:
        if days < 1:
            raise ValueError("days must be >= 1")

        start_date = datetime.utcnow() - timedelta(days=days)

        if metric_type == "gst_mismatch":
            query = (
                self.session.query(func.date(TRN_Revenue.created_at).label("date"), func.count().label("count"))
                .filter(TRN_Revenue.company_id == self.company_id)
                .filter(TRN_Revenue.created_at >= start_date)
                .filter(TRN_Revenue.gst_match == False)
                .group_by(func.date(TRN_Revenue.created_at))
                .order_by(func.date(TRN_Revenue.created_at))
            )
        elif metric_type == "tds_mismatch":
            query = (
                self.session.query(func.date(TRN_Revenue.created_at).label("date"), func.count().label("count"))
                .filter(TRN_Revenue.company_id == self.company_id)
                .filter(TRN_Revenue.created_at >= start_date)
                .filter(TRN_Revenue.tds_match == False)
                .group_by(func.date(TRN_Revenue.created_at))
                .order_by(func.date(TRN_Revenue.created_at))
            )
        elif metric_type == "commission_exceed":
            query = (
                self.session.query(func.date(TRN_Commission.created_at).label("date"), func.count().label("count"))
                .filter(TRN_Commission.company_id == self.company_id)
                .filter(TRN_Commission.created_at >= start_date)
                .filter(TRN_Commission.exceeds_max == True)
                .group_by(func.date(TRN_Commission.created_at))
                .order_by(func.date(TRN_Commission.created_at))
            )
        elif metric_type == "red_flag_count":
            query = (
                self.session.query(func.date(ETL_RedFlag.created_at).label("date"), func.count().label("count"))
                .filter(ETL_RedFlag.company_id == self.company_id)
                .filter(ETL_RedFlag.created_at >= start_date)
                .group_by(func.date(ETL_RedFlag.created_at))
                .order_by(func.date(ETL_RedFlag.created_at))
            )
        else:
            raise ValueError(f"Unsupported metric type: {metric_type}")

        results = query.all()
        return {
            "metric": metric_type,
            "days": days,
            "data": [{"date": str(row[0]), "count": int(row[1])} for row in results],
        }
