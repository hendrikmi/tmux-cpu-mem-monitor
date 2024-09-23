#!/usr/bin/env bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Checks if Python3 is installed
check_python_installation() {
    if ! command -v python3 >/dev/null; then
        tmux display-message "Python3 is required but not installed. Please install Python3."
        exit 1 # Exit the script if Python3 is not installed
    fi
}

# Sets up the virtual environment and install dependencies
setup_virtual_env() {
    if [ ! -d "$CURRENT_DIR/venv" ]; then
        tmux display-message "tmux-cpu-memory: Setting up virtual environment..."
        if python3 -m venv "$CURRENT_DIR/venv"; then
            if "$CURRENT_DIR/venv/bin/pip" install -r "$CURRENT_DIR/requirements.txt"; then
                tmux display-message "tmux-cpu-memory plugin installed successfully."
            else
                tmux display-message "tmux-cpu-memory: Failed to install dependencies."
                exit 1 # Exit if pip fails to install dependencies
            fi
        else
            tmux display-message "tmux-cpu-memory: Failed to create virtual environment."
            exit 1 # Exit if virtual environment creation fails
        fi
    else
        tmux display-message "tmux-cpu-memory: Virtual environment already exists."
    fi
}

# Updates tmux option with the cpu or mem script command
update_placeholder() {
    local placeholder="$1"
    local option="$2"
    local script="$3"
    local option_value="$(tmux show-option -gqv "$option")"

    # Extract everything between #{placeholder and } from the option value
    local flags=$(echo "$option_value" | awk -F "#{$placeholder" '{print $2}' | sed 's/\}.*//')

    # Construct the command to execute the Python script with the appropriate flags
    local command="#($CURRENT_DIR/venv/bin/python $CURRENT_DIR/src/$script$flags)"

    # Replace the #{placeholder ...} placeholder with the actual command in the option value
    local new_option_value="${option_value//\#\{$placeholder$flags\}/$command}"

    # Update the tmux option with the new value
    tmux set-option -g "$option" "$new_option_value"
}

main() {
    check_python_installation
    setup_virtual_env
    update_placeholder "cpu" "status-right" "cpu.py"
    update_placeholder "mem" "status-right" "mem.py"
    update_placeholder "disk" "status-right" "disk.py"
    update_placeholder "battery" "status-right" "battery.py"
    update_placeholder "cpu" "status-left" "cpu.py"
    update_placeholder "mem" "status-left" "mem.py"
    update_placeholder "disk" "status-left" "disk.py"
    update_placeholder "battery" "status-left" "battery.py"
}
main
