# TMUX CPU & Memory Monitor

This project is a simple yet flexible tool designed to display CPU and memory usage in the Tmux status bar.

## Screenshots

All options:

<img src="img/full.png" alt="" style="width:30%; height:30%;"/>

Without separator:

<img src="img/full_no_separator.png" alt="" style="width:30%; height:30%;"/>

Without icons:

<img src="img/full_no_icons.png" alt="" style="width:30%; height:30%;"/>

CPU and memory reversed:

<img src="img/full_reversed.png" alt="" style="width:30%; height:30%;"/>

Just CPU with icon:

<img src="img/just_cpu_with_icon.png" alt="" style="width:30%; height:30%;"/>

Just memory with prefix:

<img src="img/just_mem_with_prefix.png" alt="" style="width:30%; height:30%;"/>

## Features

- Display CPU usage as a percentage.
- Display memory usage as a percentage or as a used/total ratio in gigabytes (GB).
- Customize the display with icons and text prefixes.
- Optionally reverse the order of CPU and memory information.

## Installation

1. Install it with the TPM plugin manager by including the following lines in your `.tmux.conf` file.

   ```bash
   set -g @plugin 'tmux-plugins/tpm'
   set -g @plugin 'hendrikmi/tmux-cpu-mem-monitor'
   run '~/.tmux/plugins/tpm/tpm'
   ```

1. Then trigger the installation with `Prefix + I`.

1. Integrate it into your status bar as with the `#{cpu_mem}` format string.

   ```bash
   set -g status-right "#{cpu_mem}"
   ```

   Optionally you can provide arguments:

   ```bash
   set -g status-right "#{cpu_mem -c -m -i -s}"
   ```

## Options

- `-c, --cpu`: Display CPU usage as a percentage.
- `-m, --mem`: Display memory usage as a percentage or as used/total in GB.
- `-i, --icons`: Prefix the output with icons.
- `-p, --prefix`: Prefix the output with text labels `CPU:` and `MEM:`.
- `-s, --separator`: Separate CPU and memory outputs with a `|`.
- `-r, --reverse`: Reverse the order of CPU and memory outputs.
- `--mem-raw`: Display memory usage as used/total in GB instead of a percentage.
