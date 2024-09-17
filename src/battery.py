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
    """Display the remaining battery amount in a human-readable format.

    Examples:
    - Charging
    - Out of battery
    - 1 minute remaining
    - 5 minutes remaining
    - 1+ hour remaining
    - more than 2 hours remaining
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


def get_battery_compact():
    """Display battery percentage in a compact format"""
    if _get_charging_status():
        return "Charging"

    # Remap the battery percentage into a whole number from 0 up to 7
    def remap_range(value, low, high, remap_low, remap_high):
        return remap_low + (value - low) * (remap_high - remap_low) / (high - low)

    battery = remap_range(psutil.sensors_battery().percent, 0, 100, 0, 7)

    # Unicode characters for the battery indicator
    # 0x00002581-0x00002588
    battery_indicator = chr(0x00002581 + int(battery))

    return f"{battery_indicator}"


def main(args):
    if args.time:
        battery = get_battery_time()
    elif args.long:
        battery = get_battery_long()
    elif args.compact:
        battery = get_battery_compact()
    else:
        battery = get_battery_percent()

    print(battery)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--percent", action="store_true", default=False)
    group.add_argument("-t", "--time", action="store_true", default=False)
    group.add_argument("-l", "--long", action="store_true", default=False)
    group.add_argument("-c", "--compact", action="store_true", default=False)
    args = parser.parse_args()
    main(args)
