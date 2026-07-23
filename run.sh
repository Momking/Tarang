#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Find gtk4-layer-shell shared library
for dir in /usr/lib64 /usr/lib /lib64 /lib; do
    if [[ -d "$dir" ]]; then
        lib=$(find "$dir" -maxdepth 1 -name 'libgtk4-layer-shell.so*' | sort -V | tail -n1)
        if [[ -n "$lib" ]]; then
            LAYER_SHELL_LIB="$lib"
            break
        fi
    fi
done

if [[ -z "${LAYER_SHELL_LIB}" ]]; then
    echo "Error: libgtk4-layer-shell.so not found."
    echo
    echo "Please install gtk4-layer-shell."
    exit 1
fi

echo "Using: $LAYER_SHELL_LIB"

export LD_PRELOAD="$LAYER_SHELL_LIB${LD_PRELOAD:+:$LD_PRELOAD}"

exec python3 src/main.py "$@"
