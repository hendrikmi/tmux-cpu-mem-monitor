import argparse
import psutil
import os
import sys
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


def get_disk_usage_percent(path=_get_default_path()):
    """Display disk usage as a percentage"""
    disk = psutil.disk_usage(path)
    disk_usage = disk.percent
    return f"{disk_usage}%"


def get_disk_usage_free(path=_get_default_path()):
    """Display free disk in GB"""

    disk = psutil.disk_usage(path)
    return f"{bytes2human(disk.free)}"


def get_disk_usage_total(path=_get_default_path()):
    """Display disk usage as used/total in GB"""
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
    parser.add_argument("-t", "--total", action="store_true", default=False)
    parser.add_argument("-f", "--free", action="store_true", default=False)
    parser.add_argument("-p", "--path", type=str, default=_get_default_path())
    args = parser.parse_args()
    main(args)
