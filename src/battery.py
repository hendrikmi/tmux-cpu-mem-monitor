import argparse

import psutil


def _get_charging_status():
    """Get the battery charging status"""
    battery = psutil.sensors_battery()
    return battery.power_plugged


def get_battery_percent():
    """Display battery percentage"""
    if _get_charging_status():
        return "Charging"

    battery = round(psutil.sensors_battery().percent)
    return f"{battery}%"


def get_battery_time():
    """Display battery time remaining in hours and minutes"""
    if _get_charging_status():
        return "Charging"

    battery = psutil.sensors_battery().secsleft
    hours, remainder = divmod(battery, 3600)
    minutes, _ = divmod(remainder, 60)
    if hours == 0:
        return f"{minutes}m"
    return f"{hours}h {minutes}m"


def get_battery_human_readable():
    """Display the remaining battery amount in a fun human-readable format.

    Examples:
    - Fully charged
    - Almost full
    - More than half full
    ...
    """
    if _get_charging_status():
        return "Charging"

    battery = psutil.sensors_battery().percent
    if battery == 100:
        return "Fully charged"
    elif battery >= 95:
        return "Almost full"
    elif battery >= 75:
        return "More than half full"
    elif battery == 50:
        return "Half full"
    elif battery <= 25:
        return "Less than half full"
    elif battery <= 5:
        return "Battery is almost empty"
    elif battery == 1:
        return "I'm dying over here!"
    return "Battery is empty"


def main(args):
    if args.time:
        battery = get_battery_time()
    elif args.human_readable:
        battery = get_battery_human_readable()
    else:
        battery = get_battery_percent()

    print(battery)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--percent", action="store_true", default=False)
    group.add_argument("-t", "--time", action="store_true", default=False)
    group.add_argument("-hr", "--human-readable", action="store_true", default=False)
    args = parser.parse_args()
    main(args)
