import datetime

from ulmo import util


def test_convert_date_from_string():
    compare_dates = [
        ('2011-12-31', datetime.date(2011, 12, 31)),
        ('12/31/2011', datetime.date(2011, 12, 31)),
        ('2012-02-29', datetime.date(2012, 2, 29)),
        ('2012-2-29', datetime.date(2012, 2, 29)),
        ('2/29/2012', datetime.date(2012, 2, 29)),
        ('02/29/2012', datetime.date(2012, 2, 29)),
        ('2013-01-01', datetime.date(2013, 1, 1)),
    ]

    for test_str, test_date in compare_dates:
        date = util.convert_date(test_str)
        assert date == test_date


def test_convert_date_from_date():
    compare_dates = [
        datetime.date(2011, 12, 31),
        datetime.date(2012, 2, 29),
        datetime.date(2013, 1, 1),
    ]

    for test_date in compare_dates:
        date = util.convert_date(test_date)
        assert date == test_date


def test_convert_date_from_datetime():
    compare_dates = [
        (datetime.datetime(2011, 12, 31, 20),
            datetime.date(2011, 12, 31)),
        (datetime.datetime(2011, 12, 31, 0, 0, 0),
            datetime.date(2011, 12, 31)),
        (datetime.datetime(2011, 12, 31, 23, 59, 59),
            datetime.date(2011, 12, 31)),
    ]

    for test_datetime, test_date in compare_dates:
        date = util.convert_date(test_datetime)
        assert date == test_date


def test_convert_datetime_from_string():
    compare_datetimes = [
        ('2011-12-31', datetime.datetime(2011, 12, 31)),
        ('2011-12-31 4:28', datetime.datetime(2011, 12, 31, 4, 28)),
        ('2011-12-31 4:28:15', datetime.datetime(2011, 12, 31, 4, 28, 15)),
        ('12/31/2011', datetime.datetime(2011, 12, 31)),
        ('12/31/2011 1:30:29', datetime.datetime(2011, 12, 31, 1, 30, 29)),
        ('12/31/2011 01:30:29', datetime.datetime(2011, 12, 31, 1, 30, 29)),
        ('12/31/2011 01:30', datetime.datetime(2011, 12, 31, 1, 30, 0)),
        ('2012-02-29', datetime.datetime(2012, 2, 29)),
        ('2012-2-29', datetime.datetime(2012, 2, 29)),
        ('2/29/2012', datetime.datetime(2012, 2, 29)),
        ('02/29/2012', datetime.datetime(2012, 2, 29)),
        ('2013-01-01', datetime.datetime(2013, 1, 1)),
    ]

    for test_str, test_datetime in compare_datetimes:
        converted = util.convert_datetime(test_str)
        assert converted == test_datetime


def test_convert_datetime_from_datetime():
    compare_datetimes = [
        datetime.datetime(2011, 12, 31),
        datetime.datetime(2011, 12, 31, 3, 30),
        datetime.datetime(2011, 12, 31, 1, 30, 19),
        datetime.datetime(2011, 12, 31, 0, 0, 1),
        datetime.datetime(2012, 2, 29),
        datetime.datetime(2013, 1, 1),
    ]

    for test_datetime in compare_datetimes:
        converted = util.convert_datetime(test_datetime)
        assert converted == test_datetime


def test_convert_datetime_from_date():
    compare_datetimes = [
        (datetime.date(2011, 12, 31),
            datetime.datetime(2011, 12, 31, 0, 0, 0)),
    ]

    for test_date, test_datetime in compare_datetimes:
        converted = util.convert_datetime(test_date)
        assert converted == test_datetime
