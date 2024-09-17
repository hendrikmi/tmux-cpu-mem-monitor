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


def get_battery_long():
    """Display the remaining battery amount in a fun human-readable format.

    Examples:
    - Fully charged
    - Almost full
    - More than half full
    ...
    """
    if _get_charging_status():
        return "Charging"

    battery = psutil.sensors_battery().secsleft
    hours, remainder = divmod(battery, 3600)
    minutes, _ = divmod(remainder, 60)

    # Switch statements for hours and minutes to return human-readable output
    match hours:
        case 0:
            match minutes:
                case 0:
                    return "Out of battery"
                case 1:
                    return "1 minute remaining"
                case _:
                    return f"{minutes} minutes remaining"
        case 1:
            return "1+ hour remaining"
        case _:
            return f"more than {hours} hours remaining"


def main(args):
    if args.time:
        battery = get_battery_time()
    elif args.long:
        battery = get_battery_long()
    else:
        battery = get_battery_percent()

    print(battery)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--percent", action="store_true", default=False)
    group.add_argument("-t", "--time", action="store_true", default=False)
    group.add_argument("-l", "--long", action="store_true", default=False)
    args = parser.parse_args()
    main(args)
