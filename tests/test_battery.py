from unittest.mock import patch

import pytest

from src.battery import get_battery_compact, get_battery_long


@patch("src.battery._get_charging_status", return_value=True)
def test_charging(mock_charging_status):
    """Test the battery charging status"""
    result = get_battery_long()
    assert result == "Charging"


@patch("src.battery._get_charging_status", return_value=False)
@patch("psutil.sensors_battery")
@pytest.mark.parametrize(
    "percentage,status",
    [
        (100, "Fully charged"),
        (95, "Almost full"),
        (74, "More than 3/4 full"),
        (50, "More than half full"),
        (26, "Less than half full"),
        (6, "Battery is running low"),
        (2, "Battery is almost empty"),
        (1, "I'm dying over here"),
        (0, "Out of battery"),
    ],
)
def test_battery_long(mock_battery, mock_charging_status, percentage, status):
    """Test battery with a range of percentages"""
    mock_battery.return_value.percent = percentage
    result = get_battery_long()
    assert result == status


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
