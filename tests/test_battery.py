import re

from src import battery


def test_battery_percentage_format():
    """Assert that the battery percentage is properly formatted
    Example: 20%
    """
    percent = battery.get_battery_percent()

    assert re.match(r"\d+(\.\d+)?%", percent) is not None


def test_battery_time_format():
    """Assert that the battery time is properly formatted
    Example: 1h 30m
    """
    time = battery.get_battery_time()

    assert re.match(r"\d+(h\ \d+m)", time)
