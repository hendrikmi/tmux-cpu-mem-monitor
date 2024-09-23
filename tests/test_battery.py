import unittest
from unittest.mock import patch

from src.battery import get_battery_compact, get_battery_long


@patch("src.battery._get_charging_status", return_value=True)
def test_charging(mock_charging_status):
    """Test the battery charging status"""
    result = get_battery_long()
    assert result == "Charging"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_out_of_battery(mock_battery, mock_charging_status):
    """Test battery completely out (0 hours, 0 minutes)"""
    mock_battery.return_value.secsleft = 0
    result = get_battery_long()
    assert result == "Out of battery"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_1_minute_remaining(mock_battery, mock_charging_status):
    """Test battery with 1 minute remaining (0 hours, 1 minute)"""
    mock_battery.return_value.secsleft = 60
    result = get_battery_long()
    assert result == "1 minute remaining"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_5_minutes_remaining(mock_battery, mock_charging_status):
    """Test battery with 5 minutes remaining (0 hours, 5 minutes)"""
    mock_battery.return_value.secsleft = 5 * 60
    result = get_battery_long()
    assert result == "5 minutes remaining"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_1_hour_remaining(mock_battery, mock_charging_status):
    """Test battery with 1 hour remaining (1 hour, 0 minutes)"""
    mock_battery.return_value.secsleft = 3600
    result = get_battery_long()
    assert result == "1+ hour remaining"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_more_than_1_hour_remaining(mock_battery, mock_charging_status):
    """Test battery with more than 2 hours remaining (2 hours, 0 minutes)"""
    mock_battery.return_value.secsleft = 2 * 3600
    result = get_battery_long()
    assert result == "more than 2 hours remaining"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_fun_less_than_1_minute(mock_battery, mock_charging_status):
    """Test battery with less than 1 minute remaining (0 hours, 0 minutes)"""
    mock_battery.return_value.secsleft = 30
    result = get_battery_long(mode="humor")
    assert result == "Needs juice"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_fun_less_than_2_minutes(mock_battery, mock_charging_status):
    """Test battery with less than 2 minutes remaining (0 hours, 1 minute, 30 seconds)"""
    mock_battery.return_value.secsleft = 90
    result = get_battery_long(mode="humor")
    assert result == "It's getting dark"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_fun_5_minutes(mock_battery, mock_charging_status):
    """Test battery with 5 minutes remaining (0 hours, 5 minutes)"""
    mock_battery.return_value.secsleft = 5 * 60
    result = get_battery_long(mode="humor")
    assert result == "5m left, hurry!"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_fun_10_minutes(mock_battery, mock_charging_status):
    """Test battery with 10 minutes remaining (0 hours, 10 minutes)"""
    mock_battery.return_value.secsleft = 10 * 60
    result = get_battery_long(mode="humor")
    assert result == "My final hour"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_fun_1_hour(mock_battery, mock_charging_status):
    """Test battery with 1 hour remaining (1 hour, 0 minutes)"""
    mock_battery.return_value.secsleft = 3600
    result = get_battery_long(mode="humor")
    assert result == "The sun is setting"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_fun_2_hour(mock_battery, mock_charging_status):
    """Test battery with 2 hours remaining (2 hours, 0 minutes)"""
    mock_battery.return_value.secsleft = 3600 * 2
    result = get_battery_long(mode="humor")
    assert result == "Off the grid"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
def test_battery_compact(mock_battery, mock_charging_status):
    """Test battery compact mode with a range of percentages"""
    print("Battery percentage:", end=" ")
    for i in range(0, 101, 10):
        mock_battery.return_value.percent = i
        character = get_battery_compact()
        print(i, character, end=" ")

        result = ord(character)
        assert 0x00002581 <= result <= 0x00002588
