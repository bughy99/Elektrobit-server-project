#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set environment variables
export PORT=50030
export CLIENT_NUM=0
declare -a port_arr=(50001 50002 50003)

# Launch server.py from the same directory as this script
python3 "$SCRIPT_DIR/server.py"

