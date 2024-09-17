import unittest
from unittest.mock import patch

from src.battery import get_battery_compact, get_battery_long


# Test when the device is charging
@patch("src.battery._get_charging_status", return_value=True)
def test_charging(mock_charging_status):
    result = get_battery_long()
    assert result == "Charging"


# Test battery completely out (0 hours, 0 minutes)
@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_out_of_battery(mock_battery, mock_charging_status):
    mock_battery.return_value.secsleft = 0
    result = get_battery_long()
    assert result == "Out of battery"


# Test battery with 1 minute remaining (0 hours, 1 minute)
@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_1_minute_remaining(mock_battery, mock_charging_status):
    mock_battery.return_value.secsleft = 60
    result = get_battery_long()
    assert result == "1 minute remaining"


# Test battery with 5 minutes remaining (0 hours, 5 minutes)
@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_5_minutes_remaining(mock_battery, mock_charging_status):
    mock_battery.return_value.secsleft = 5 * 60
    result = get_battery_long()
    assert result == "5 minutes remaining"


# Test battery with more than 1 hour (1+ hour remaining)
@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_1_hour_remaining(mock_battery, mock_charging_status):
    mock_battery.return_value.secsleft = 3600
    result = get_battery_long()
    assert result == "1+ hour remaining"


# Test battery with more than 2 hours (e.g., 2 hours remaining)
@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_more_than_1_hour_remaining(mock_battery, mock_charging_status):
    mock_battery.return_value.secsleft = 2 * 3600
    result = get_battery_long()
    assert result == "more than 2 hours remaining"


# Test battery compact mode with a range of percentages
@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_compact(mock_battery, mock_charging_status):
    print("Battery percentage:", end=" ")
    for i in range(0, 101, 10):
        mock_battery.return_value.percent = i
        character = get_battery_compact()
        print(i, character, end=" ")

        result = ord(character)
        assert 0x00002581 <= result <= 0x00002588
