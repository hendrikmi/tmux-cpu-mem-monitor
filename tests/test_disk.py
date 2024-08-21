import re

from src import disk


def test_disk_percentage_format():
    """Assert that the disk percentage is properly formatted
    Example: 5.7%
    """
    percent = disk.get_disk_usage_percent()

    # Check that the output is formatted as a decimal number followed by a percent sign
    assert re.match(r"\d+(\.\d+)?%", percent) is not None


def test_disk_free_format():
    """Assert that the disk free space is properly formatted
    Example: 55.7G
    """
    free = disk.get_disk_usage_free()

    # Check that the output is formatted as a decimal number followed by a unit
    assert re.match(r"\d+(\.\d+)?[A-Z]", free) is not None


def test_disk_total_format():
    """Assert that the total disk is properly formatted
    Example: 55.7G/1006.9G
    """
    total = disk.get_disk_usage_total()

    # Check that the output is used/total where used and total are formatted as decimal numbers followed by a unit
    assert re.match(r"^\d+(\.\d+)?[A-Z]/\d+(\.\d+)?[A-Z]$", total) is not None
