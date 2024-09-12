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

    battery = psutil.sensors_battery()
    battery_percent = battery.percent
    return f"{battery_percent}%"


def get_battery_time():
    """Display battery time remaining in hours and minutes"""
    if _get_charging_status():
        return "Charging"

    battery = psutil.sensors_battery()
    battery_time = battery.secsleft
    hours, remainder = divmod(battery_time, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"


def main(args):
    if args.time:
        battery = get_battery_time()
    else:
        battery = get_battery_percent()

    print(battery)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--percent", action="store_true", default=False)
    group.add_argument("-t", "--time", action="store_true", default=False)
    args = parser.parse_args()
    main(args)
