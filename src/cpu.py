import argparse

import psutil


def get_cpu_usage(interval: int, percpu: bool) -> str:
    """Display CPU usage as a percentage"""
    cpu_usage = psutil.cpu_percent(interval=interval, percpu=percpu)

    if percpu:
        percpu_str = ", ".join(map(str, cpu_usage))
        return percpu_str
    return f"{cpu_usage}%"


def main(args):
    cpu_usage = get_cpu_usage(args.interval, args.percpu)
    print(cpu_usage)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--interval", type=int, default=1, help="interval in seconds"
    )
    parser.add_argument(
        "--percpu", action="store_true", default=False, help="display per cpu usage"
    )
    args = parser.parse_args()
    main(args)
