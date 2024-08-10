import psutil
import argparse

CPU_ICON = ""
MEM_ICON = ""
SEPARATOR = "|"


def get_cpu_usage_percent():
    """Display CPU usage as a percentage"""
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"{cpu_usage}%"


def get_mem_usage_percent():
    """Display memory usage as a percentage"""
    mem = psutil.virtual_memory()
    mem_usage = mem.percent
    return f"{mem_usage}%"


def get_mem_raw_usage():
    """Display memory usage as used/total in GB"""
    mem = psutil.virtual_memory()
    used_gb = mem.used / (1024**3)  # Convert to GB
    total_gb = mem.total / (1024**3)  # Convert to GB
    return f"{used_gb:.2f}GB/{total_gb:.2f}GB"


def format_output(cpu_output, mem_output, args):
    # Choose the separator based on whether -s is passed"""
    separator = f" {SEPARATOR} " if args.separator else " "

    # Combine CPU and Memory outputs with separator (only if both are present)
    if args.cpu and args.mem:
        if args.reverse:
            return f"{mem_output}{separator}{cpu_output}"
        else:
            return f"{cpu_output}{separator}{mem_output}"
    elif cpu_output:
        return cpu_output
    elif mem_output:
        return mem_output

    return ""


def main(args):
    cpu_output = ""
    mem_output = ""

    # Build CPU output
    if args.cpu:
        cpu_output = f"{CPU_ICON} " if args.icons else ""
        cpu_output += "CPU: " if args.prefix else ""
        cpu_output += get_cpu_usage_percent()

    # Build Memory output
    if args.mem:
        mem_output = f"{MEM_ICON} " if args.icons else ""
        mem_output += "MEM: " if args.prefix else ""
        mem_output += get_mem_raw_usage() if args.mem_raw else get_mem_usage_percent()

    print(format_output(cpu_output, mem_output, args))


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cpu", action="store_true", help="Display CPU usage")
    parser.add_argument("-m", "--mem", action="store_true", help="Display memory usage")
    parser.add_argument("-i", "--icons", action="store_true", help="Prefix output with icons")
    parser.add_argument("-p", "--prefix", action="store_true", help="Prefix output with 'CPU:' and 'MEM:'")
    parser.add_argument("-s", "--separator", action="store_true", help="Separate CPU and memory output with '|'")
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverse the order of CPU and memory blocks")
    parser.add_argument("--mem-raw", action="store_true", help="Display memory usage as used/total in GB instead of percentage")
    # fmt: on
    args = parser.parse_args()
    main(args)
