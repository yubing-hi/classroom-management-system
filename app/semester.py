import os
from datetime import date, datetime, timedelta

SEMESTER_START_DATE = os.getenv('SEMESTER_START_DATE', '2026-02-24')
SEMESTER_TOTAL_WEEKS = int(os.getenv('SEMESTER_TOTAL_WEEKS', '20'))


def parse_date(value) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    return datetime.strptime(str(value), '%Y-%m-%d').date()


def get_semester_start() -> date:
    return parse_date(SEMESTER_START_DATE)


def get_total_weeks() -> int:
    return SEMESTER_TOTAL_WEEKS


def date_to_week(target) -> int | None:
    """Convert a calendar date to 1-based academic week number."""
    target_date = parse_date(target)
    start = get_semester_start()
    delta = (target_date - start).days
    if delta < 0:
        return None
    week = delta // 7 + 1
    if week > get_total_weeks():
        return None
    return week


def week_to_range(week: int) -> tuple[date, date] | None:
    if week < 1 or week > get_total_weeks():
        return None
    start = get_semester_start() + timedelta(days=(week - 1) * 7)
    return start, start + timedelta(days=6)


def week_dates(week: int) -> list[date]:
    rng = week_to_range(week)
    if not rng:
        return []
    start, _ = rng
    return [start + timedelta(days=i) for i in range(7)]


def week_overlap(s1: int, e1: int, s2: int, e2: int) -> bool:
    return s1 <= e2 and s2 <= e1


def current_week() -> int:
    today = date.today()
    week = date_to_week(today)
    return week if week else 1
