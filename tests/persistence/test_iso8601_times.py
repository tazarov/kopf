import datetime

import pytest

from kopf._core.actions.progression import format_iso8601, parse_iso8601

TZ = datetime.timezone.utc


@pytest.mark.parametrize('basetime, val, expected', [
    (datetime.datetime(2000, 1, 1), None, None),
    # TZ-naive:
    (datetime.datetime(2000, 1, 1), 0, '2000-01-01T00:00:00.000000'),
    (datetime.datetime(2000, 1, 1), 123.456789, '2000-01-01T00:02:03.456789'),
    (datetime.datetime(2000, 1, 1), -123.456789, '1999-12-31T23:57:56.543211'),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321), 0, '2000-01-01T09:08:07.654321'),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321), 123.456789, '2000-01-01T09:10:11.111110'),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321), -123.456789, '2000-01-01T09:06:04.197532'),
    # TZ-aware:
    (datetime.datetime(2000, 1, 1, tzinfo=TZ), 0, '2000-01-01T00:00:00.000000+00:00'),
    (datetime.datetime(2000, 1, 1, tzinfo=TZ), 123.456789, '2000-01-01T00:02:03.456789+00:00'),
    (datetime.datetime(2000, 1, 1, tzinfo=TZ), -123.456789, '1999-12-31T23:57:56.543211+00:00'),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321, tzinfo=TZ), 0, '2000-01-01T09:08:07.654321+00:00'),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321, tzinfo=TZ), 123.456789, '2000-01-01T09:10:11.111110+00:00'),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321, tzinfo=TZ), -123.456789, '2000-01-01T09:06:04.197532+00:00'),
])
def test_format_iso8601(val, basetime, expected):
    result = format_iso8601(val, basetime)
    assert result == expected


@pytest.mark.parametrize('basetime, val, expected', [
    (datetime.datetime(2000, 1, 1), None, None),
    # TZ-naive:
    (datetime.datetime(2000, 1, 1), '2000-01-01T00:00:00.000000', 0),
    (datetime.datetime(2000, 1, 1), '2000-01-01T00:02:03.456789', 123.456789),
    (datetime.datetime(2000, 1, 1), '1999-12-31T23:57:56.543211', -123.456789),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321), '2000-01-01T09:08:07.654321', 0),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321), '2000-01-01T09:10:11.111110', 123.456789),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321), '2000-01-01T09:06:04.197532', -123.456789),
    # TZ-aware:
    (datetime.datetime(2000, 1, 1, tzinfo=TZ), '2000-01-01T00:00:00.000000+00:00', 0),
    (datetime.datetime(2000, 1, 1, tzinfo=TZ), '2000-01-01T00:02:03.456789+00:00', 123.456789),
    (datetime.datetime(2000, 1, 1, tzinfo=TZ), '1999-12-31T23:57:56.543211+00:00', -123.456789),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321, tzinfo=TZ), '2000-01-01T09:08:07.654321+00:00', 0),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321, tzinfo=TZ), '2000-01-01T09:10:11.111110+00:00', 123.456789),
    (datetime.datetime(2000, 1, 1, 9, 8, 7, 654321, tzinfo=TZ), '2000-01-01T09:06:04.197532+00:00', -123.456789),
])
def test_parse_iso8601(val, basetime, expected):
    result = parse_iso8601(val, basetime)
    assert result == expected


def test_format_on_stretched_interval_with_precision_loss():
    seconds_in_100yr = (datetime.datetime(2099, 1, 1) - datetime.datetime(2000, 1, 1)).total_seconds()
    result = format_iso8601(seconds_in_100yr, datetime.datetime(2000, 1, 1))
    assert result == '2099-01-01T00:00:00.000000'


def test_parse_on_stretched_interval_with_precision_loss():
    seconds_in_100yr = (datetime.datetime(2099, 1, 1) - datetime.datetime(2000, 1, 1)).total_seconds()
    result = parse_iso8601('2099-01-01T00:00:00.000000', datetime.datetime(2000, 1, 1))
    assert result == seconds_in_100yr
