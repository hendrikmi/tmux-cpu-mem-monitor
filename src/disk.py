import argparse
import psutil
from psutil._common import bytes2human

def get_disk_usage_percent():
    """Display disk usage as a percentage"""
    disk = psutil.disk_usage("/")
    disk_usage = disk.percent
    return f"{disk_usage}%"

def get_disk_usage_free():
    """Display free disk in GB"""
    disk = psutil.disk_usage("/")
    return f"{bytes2human(disk.free)}"

def get_disk_usage_total():
    """Display disk usage as used/total in GB"""
    disk = psutil.disk_usage("/")
    return f"{bytes2human(disk.used)}/{bytes2human(disk.total)}"

def main(args):
    if args.total:
        disk_usage = get_disk_usage_total()
    elif args.free:
        disk_usage = get_disk_usage_free()
    else:
        disk_usage = get_disk_usage_percent()
    
    print(disk_usage)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--total", action="store_true", default=False)
    parser.add_argument("-f", "--free", action="store_true", default=False)
    args = parser.parse_args()
    main(args)
