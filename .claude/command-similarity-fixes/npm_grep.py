#!/usr/bin/env python3
"""
Command Similarity Fixer for 'npm test -- --grep'
==================================================
Pattern: ^npm test.*--grep
"""

import json
import sys
import shlex

def normalize_command(command: str) -> str:
    """
    Normalizes an 'npm test' command by removing the --grep option.
    """
    if "npm test" not in command:
        return command

    try:
        parts = shlex.split(command)
    except ValueError:
        parts = command.split()

    try:
        npm_index = parts.index('npm')
        test_index = parts.index('test', npm_index)
    except ValueError:
        return command

    new_parts = []
    skip_next = False
    for i, part in enumerate(parts):
        if skip_next:
            skip_next = False
            continue

        if part == '--grep':
            if i + 1 < len(parts):
                skip_next = True
            continue

        if part.startswith('--grep='):
            continue

        new_parts.append(part)

    normalized_command = ' '.join(new_parts)

    if normalized_command.endswith(' --'):
        normalized_command = normalized_command[:-3].strip()

    return normalized_command

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
