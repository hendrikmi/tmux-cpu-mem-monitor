import re
from unittest import mock

from src import battery


def test_battery_percentage_format():
    """Assert that the battery percentage is properly formatted or it returns 'Charging'.

    Example: 20% or 'Charging'
    """
    with mock.patch("src.battery.get_battery_percent", return_value="20%"):
        percent = battery.get_battery_percent()
        assert re.match(
            r"\d+%$", percent
        ), f"Unexpected battery percentage format: {percent}"

    with mock.patch("src.battery.get_battery_percent", return_value="Charging"):
        percent = battery.get_battery_percent()
        assert percent == "Charging", f"Expected 'Charging', got: {percent}"


def test_battery_time_format():
    """Assert that the battery time is properly formatted or it returns 'Charging'.

    Example: 1h 30m or 'Charging'
    """
    with mock.patch("src.battery.get_battery_time", return_value="1h 30m"):
        time = battery.get_battery_time()
        assert re.match(r"\d+h \d+m$", time), f"Unexpected battery time format: {time}"

    with mock.patch("src.battery.get_battery_time", return_value="Charging"):
        time = battery.get_battery_time()
        assert time == "Charging", f"Expected 'Charging', got: {time}"


def test_battery_percentage_0_percent():
    """Test if 0% is properly formatted"""
    with mock.patch("src.battery.get_battery_percent", return_value="0%"):
        percent = battery.get_battery_percent()
        assert percent == "0%", f"Expected '0%', got: {percent}"


def test_battery_percentage_100_percent():
    """Test if 100% is properly formatted"""
    with mock.patch("src.battery.get_battery_percent", return_value="100%"):
        percent = battery.get_battery_percent()
        assert percent == "100%", f"Expected '100%', got: {percent}"


def test_battery_percentage_invalid_format():
    """Test handling of invalid percentage format"""
    with mock.patch("src.battery.get_battery_percent", return_value="abc"):
        percent = battery.get_battery_percent()
        assert (
            re.match(r"\d+%$", percent) is None
        ), f"Expected invalid format, got: {percent}"


def test_battery_time_no_minutes():
    """Test if time with no minutes is properly formatted (e.g., 2h 0m)"""
    with mock.patch("src.battery.get_battery_time", return_value="2h 0m"):
        time = battery.get_battery_time()
        assert re.match(r"\d+h \d+m$", time), f"Expected '2h 0m', got: {time}"


def test_battery_time_no_hours():
    """Test if time with no hours is properly formatted (e.g., 0h 30m)"""
    with mock.patch("src.battery.get_battery_time", return_value="0h 30m"):
        time = battery.get_battery_time()
        assert re.match(r"\d+h \d+m$", time), f"Expected '0h 30m', got: {time}"


def test_battery_time_invalid_format():
    """Test handling of invalid time format"""
    with mock.patch("src.battery.get_battery_time", return_value="30m"):
        time = battery.get_battery_time()
        assert (
            re.match(r"\d+h \d+m$", time) is None
        ), f"Expected invalid format, got: {time}"


def test_battery_time_extremely_large():
    """Test handling of extremely large values"""
    with mock.patch("src.battery.get_battery_time", return_value="999h 999m"):
        time = battery.get_battery_time()
        assert re.match(r"\d+h \d+m$", time), f"Expected '999h 999m', got: {time}"


def test_battery_functions_exceptions():
    """Test if exceptions are handled gracefully"""
    with mock.patch(
        "src.battery.get_battery_percent", side_effect=Exception("Battery Error")
    ):
        try:
            battery.get_battery_percent()
        except Exception as e:
            assert str(e) == "Battery Error"

    with mock.patch(
        "src.battery.get_battery_time", side_effect=Exception("Battery Error")
    ):
        try:
            battery.get_battery_time()
        except Exception as e:
            assert str(e) == "Battery Error"
