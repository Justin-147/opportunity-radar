from datetime import datetime

import pytest

from opportunity_radar.main import parse_as_of
from opportunity_radar.pipeline.normalize import parse_datetime


def test_parse_datetime_accepts_iso_date():
    assert parse_datetime("2026-07-01") == datetime(2026, 7, 1)


def test_parse_datetime_accepts_utc_z():
    assert parse_datetime("2026-07-01T10:00:00Z") == datetime(2026, 7, 1, 10)


def test_parse_datetime_converts_offset_to_utc_naive():
    assert parse_datetime("2026-07-01T10:00:00+08:00") == datetime(2026, 7, 1, 2)


def test_parse_datetime_empty_value_returns_naive_utc_datetime():
    parsed = parse_datetime("")

    assert isinstance(parsed, datetime)
    assert parsed.tzinfo is None


def test_parse_datetime_invalid_value_raises_clear_error():
    with pytest.raises(ValueError, match="Invalid datetime value"):
        parse_datetime("not-a-date")


def test_parse_as_of_supports_date_and_timezone_conversion():
    assert parse_as_of("2026-07-06") == datetime(2026, 7, 6)
    assert parse_as_of("2026-07-06T09:00:00+08:00") == datetime(2026, 7, 6, 1)
