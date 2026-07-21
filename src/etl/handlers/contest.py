import uuid

from sqlalchemy.orm import Session

from src.rules.models import RUL_Contest


def promote_contest(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    records: list[tuple[dict, int]] = []

    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        contest_name = str(row_data.get("contest_name") or row_data.get("notes") or "").strip()
        if not contest_name:
            contest_name = str(row_data.get("period") or "Contest").strip()

        if not contest_name:
            failed += 1
            continue

        contest_code = str(row_data.get("contest_code") or "").strip()
        if not contest_code:
            period = str(row_data.get("period") or "").strip()
            contest_code = f"CONTEST-{uuid.uuid4().hex[:8]}" if not period else f"CONTEST-{period.upper().replace(' ', '-')[:32]}"

        existing = session.query(RUL_Contest).filter(RUL_Contest.contest_code == contest_code).first()

        if existing:
            if conflict_resolution == "SKIP":
                skipped += 1
                records.append((item, existing.contest_id))
                continue
            if conflict_resolution == "FAIL":
                failed += 1
                continue

            existing.contest_name = contest_name or existing.contest_name
            existing.frequency = row_data.get("frequency") or existing.frequency
            existing.target_amount = row_data.get("target_amount", existing.target_amount)
            existing.bonus_percent = row_data.get("bonus_percent", existing.bonus_percent)
            existing.period = row_data.get("period") or existing.period
            existing.notes = row_data.get("notes") or existing.notes
            existing.is_active = True
            session.add(existing)
            session.flush()
            updated += 1
            records.append((item, existing.contest_id))
            continue

        contest = RUL_Contest(
            contest_code=contest_code,
            contest_name=contest_name,
            frequency=row_data.get("frequency"),
            target_amount=row_data.get("target_amount"),
            bonus_percent=row_data.get("bonus_percent"),
            period=row_data.get("period"),
            notes=row_data.get("notes"),
            is_active=True,
        )
        session.add(contest)
        session.flush()
        created += 1
        records.append((item, contest.contest_id))

    return {
        "table": "RUL_Contest",
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "records": records,
    }