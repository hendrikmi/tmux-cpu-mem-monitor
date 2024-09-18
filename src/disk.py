import argparse
import os
import sys

import psutil
from psutil._common import bytes2human


def _get_default_path():
    """Get the default path for the current platform"""
    if sys.platform == "win32":
        return "C:"
    elif sys.platform == "darwin":
        return "/System/Volumes/Data"
    elif (
        # IF kind of linux AND WSL is installed
        sys.platform.startswith("linux") and os.path.exists("/usr/lib/wsl")
    ):
        return "/usr/lib/wsl/drivers"
    else:
        return "/"


def get_disk_usage_percent(path=None):
    """Display disk usage as a percentage"""
    if path is None:
        path = _get_default_path()

    disk = psutil.disk_usage(path)
    disk_usage = disk.percent
    return f"{disk_usage}%"


def get_disk_usage_free(path=None):
    """Display free disk in GB"""
    if path is None:
        path = _get_default_path()

    disk = psutil.disk_usage(path)
    return f"{bytes2human(disk.free)}"


def get_disk_usage_total(path=None):
    """Display disk usage as used/total in GB"""
    if path is None:
        path = _get_default_path()

    disk = psutil.disk_usage(path)
    return f"{bytes2human(disk.used)}/{bytes2human(disk.total)}"


def main(args):
    if args.total:
        disk_usage = get_disk_usage_total(args.path)
    elif args.free:
        disk_usage = get_disk_usage_free(args.path)
    else:
        disk_usage = get_disk_usage_percent(args.path)

    print(disk_usage)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t",
        "--total",
        action="store_true",
        default=False,
        help="display disk usage as used/total in GB",
    )
    group.add_argument(
        "-f",
        "--free",
        action="store_true",
        default=False,
        help="display free disk in GB",
    )
    parser.add_argument(
        "-p", "--path", type=str, default=None, help="path to check disk usage"
    )
    args = parser.parse_args()
    main(args)
