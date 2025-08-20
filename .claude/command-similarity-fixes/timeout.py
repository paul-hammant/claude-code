#!/usr/bin/env python3
"""
Command Similarity Fixer for 'timeout <digits>'
===============================================
Pattern: ^timeout \d+
"""

import json
import sys
import re

def normalize_command(command: str) -> str:
    """
    Normalizes a 'timeout <digits>' command by replacing the digits
    with a placeholder.
    """
    return re.sub(r'^(timeout)\s+\d+', r'\1 [timeout_duration]', command, count=1)

def main():
    try:
        input_data = json.load(sys.stdin)
        command = input_data.get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError):
        sys.exit(0)

    if not command:
        print(json.dumps(input_data))
        sys.exit(0)

    normalized_command = normalize_command(command)

    if normalized_command != command:
        input_data["tool_input"]["command"] = normalized_command

    print(json.dumps(input_data))

if __name__ == "__main__":
    main()
