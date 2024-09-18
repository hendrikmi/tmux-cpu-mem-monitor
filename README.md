# Tmux CPU & Memory Monitor

A simple yet flexible tool designed to display CPU and memory usage in the Tmux status bar.

<img src="img/demo.png" alt="" style="width:100%; height:100%;"/>

## Installation

1. Install it with the [Tmux Plugin Manager (TPM)](https://github.com/tmux-plugins/tpm) by including the following line in your `.tmux.conf` file.

   ```bash
   set -g @plugin 'hendrikmi/tmux-cpu-mem-monitor'
   ```

1. Then trigger the installation with `Prefix + I`.

## Basic Usage

Once installed, the plugin exposes the placeholders `#{cpu}` and `#{mem}`, which can be used in `status-right` and `status-left`. By default, these placeholders display the current CPU and memory usage as a raw percentage.

You can customize the display by passing additional options. For example, `#{mem --total}` will display memory usage as used/total in GB.

## Options

### `#{cpu}` Placeholder

- `-i <num>, --interval <num>` (default `1`):
  - `0`: Compares system CPU times elapsed since last call (non-blocking).
  - `>0`: Compares system CPU times (seconds) elapsed before and after the interval (blocking).
- `--precpu`: Shows the utilization as a percentage for each CPU.

For more details, see the documentation of the underlying [psutil library](https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent).

### `#{mem}` Placeholder

- `-t, --total`: Display memory usage as used/total in GB instead of a percentage.

### `#{disk}` Placeholder
- `-p <path>, --path <path>`: Specify the path to monitor. Defaults: `C:` for Windows, `/System/Volumes/Data` for Mac, and `/` for Linux.
- `-t, --total`: Display disk usage as used/total in GB instead of a percentage.
- `-f, --free`: Display free disk space in GB.

### `#{battery}` Placeholder
- `-t, --time`: Display the remaining battery life time.
- `-p, --percentage`: Display the remaining battery percentage.
- `-l, --long`: Display the remaining battery as a sentence.
- `-c, --compact`: Display the remaining battery using an icon.
- `-f, --fun`: Display the remaining battery in a fun way.

## Examples

```bash
set -g status-right "#{cpu} | #{mem} | #{disk}"
```

<img src="img/cpu_mem_disk.png" alt="" style="width:100%; height:100%;"/>

```bash
set -g status-right " CPU: #{cpu} |  MEM: #{mem -t} | 󱛟 DISK: #{disk -t}"
```

<img src="img/cpu_mem_t_disk_t.png" alt="" style="width:100%; height:100%;"/>

```bash
set -g status-right " CPU: #{cpu -i 3} |  MEM: #{mem} | 󱛟 DISK: #{disk -f}"
```

<img src="img/cpu_mem_disk_f.png" alt="" style="width:100%; height:100%;"/>

## Why Another Plugin?

This plugin was created as a personal project to learn more about Tmux plugins and Python scripting. While exploring existing plugins that display CPU and memory usage, I noticed a few limitations that sparked my interest in building something exactly how I wanted it:

1. **Predefined Styling:** Many of the plugins I found came with predefined styling that didn't quite match what I was looking for.

2. **Missing Metrics:** Either CPU or memory metrics were missing.

3. **Lack of Configurability:** I found that other plugins often didn't offer the level of configurability I wanted. For example, I wanted to add icons to the display.

Overall, I prefer a minimalist approach, where I can simply use placeholders like `#{cpu}` and `#{mem}` with full flexibility to choose how they're presented.

## Why Python?

I chose to write this plugin in Python instead of Shell as part of my learning journey, and because of several practical reasons:

- **Powerful Libraries:** Python’s [psutil](https://psutil.readthedocs.io/en/latest/#) library provides a wide range of system and process utilities that are easy to use. For example, displaying CPU usage per core (`--precpu`) is much simpler with `psutil` compared to implementing it in a shell script.

- **Ease of Adaptation:** Working with Python makes it easier for me to adapt and add functionalities.

- **Simplified Argument Parsing:** Python's built-in `argparse` module makes it straightforward to handle command-line arguments, allowing me to easily add and manage options like `--interval` and `--total`. Additional features of `psutil` can be easily adapted.

- **Cross-Platform Compatibility:** Python with `psutil`, offers a consistent way to gather system metrics across different operating systems, which avoids dealing with the quirks of different shell environments.
