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


def get_battery_long(mode: str = None):
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
        if mode == "fun":
            return "Unlimited power!"
        return "Charging"

    battery = psutil.sensors_battery().secsleft
    hours, remainder = divmod(battery, 3600)
    minutes, _ = divmod(remainder, 60)

    def default_output():
        if hours == 0:
            if minutes == 0:
                return "Out of battery"
            elif minutes == 1:
                return "1 minute remaining"
            return f"{minutes} minutes remaining"
        elif hours == 1:
            return "1+ hour remaining"
        return f"more than {hours} hours remaining"

    def humor_output():
        if hours == 0:
            if minutes == 0:
                return "Needs juice"
            elif minutes == 1:
                return "It's getting dark"
            elif minutes == 5:
                return f"{minutes}m left, hurry!"
            return "My final hour"
        elif hours == 1:
            return "The sun is setting"
        return "Off the grid"

    return humor_output() if mode == "humor" else default_output()


def _remap_range(value, low, high, remap_low, remap_high):
    """Remap the battery percentage into a whole number from 0 up to 7"""
    return remap_low + (value - low) * (remap_high - remap_low) // (high - low)


def get_battery_compact():
    """Display battery percentage in a compact format"""
    if _get_charging_status():
        return chr(0x00002593)

    battery = _remap_range(psutil.sensors_battery().percent, 0, 100, 0, 7)

    # Unicode characters for the battery indicator
    # 0x00002581-0x00002588
    battery_indicator = chr(0x00002581 + int(battery))

    return f"{battery_indicator}"


def main(args):
    if args.time:
        battery = get_battery_time()
    elif args.long:
        battery = get_battery_long()
    elif args.fun:
        battery = get_battery_long(mode="humor")
    elif args.compact:
        battery = get_battery_compact()
    else:
        battery = get_battery_percent()

    print(battery)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    type_option = parser.add_mutually_exclusive_group()
    type_option.add_argument(
        "-p",
        "--percent",
        action="store_true",
        default=False,
        help="display remaining battery percentage",
    )
    type_option.add_argument(
        "-t",
        "--time",
        action="store_true",
        default=False,
        help="display remaining battery time",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--long",
        action="store_true",
        default=False,
        help="display remaining battery as a sentence",
    )
    group.add_argument(
        "-f",
        "--fun",
        action="store_true",
        default=False,
        help="display remaining battery with humor",
    )

    parser.add_argument(
        "-c",
        "--compact",
        action="store_true",
        default=False,
        help="display remaining battery as an icon",
    )
    args = parser.parse_args()
    main(args)
