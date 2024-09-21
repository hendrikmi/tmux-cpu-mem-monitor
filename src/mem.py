import argparse

import psutil


def get_mem_usage_percent():
    """Display memory usage as a percentage"""
    mem = psutil.virtual_memory()
    mem_usage = mem.percent
    return f"{mem_usage}%"


def get_mem_usage_total():
    """Display memory usage as used/total in GB"""
    mem = psutil.virtual_memory()
    available_gb = mem.available / (1024**3)  # Convert to GB
    total_gb = mem.total / (1024**3)
    used_gb = total_gb - available_gb
    return f"{used_gb:.2f}GB/{total_gb:.2f}GB"


def main(args):
    if args.total:
        mem_usage = get_mem_usage_total()
    else:
        mem_usage = get_mem_usage_percent()
    print(mem_usage)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--total",
        action="store_true",
        default=False,
        help="display memory usage as used/total in GB",
    )
    args = parser.parse_args()
    main(args)
