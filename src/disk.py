import argparse
import psutil

def get_disk_usage_percent():
    """Display disk usage as a percentage"""
    disk = psutil.disk_usage("/")
    disk_usage = disk.percent
    return f"{disk_usage}%"

def get_disk_usage_total():
    """Display disk usage as used/total in GB"""
    disk = psutil.disk_usage("/")
    available_gb = disk.free / (1024**3)  # Convert to GB
    total_gb = disk.total / (1024**3)
    used_gb = total_gb - available_gb
    return f"{used_gb:.2f}GB/{total_gb:.2f}GB"

def main(args):
    if args.total:
        disk_usage = get_disk_usage_total()
    else:
        disk_usage = get_disk_usage_percent()
    print(disk_usage)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--total", action="store_true", default=False)
    args = parser.parse_args()
    main(args)
