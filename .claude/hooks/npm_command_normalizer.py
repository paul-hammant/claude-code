#!/usr/bin/env python3
"""
Claude Code Hook: NPM Test Command Normalizer
==============================================
This hook runs as a PreToolUse hook for the Bash tool.
It normalizes 'npm test' commands by removing the '--grep' option
before they are passed to the approval logic.

This allows blanket approval for 'npm test' to cover all variations
with different '--grep' parameters.
"""

import json
import sys
import shlex

def normalize_npm_test_command(command: str) -> str:
    """
    Normalizes an 'npm test' command by removing the --grep option.
    """
    if "npm test" not in command:
        return command

    # Use shlex to split the command into a list of tokens
    try:
        parts = shlex.split(command)
    except ValueError:
        # If shlex fails to parse, fall back to simple splitting
        parts = command.split()

    # Find the index of 'npm' and 'test'
    try:
        npm_index = parts.index('npm')
        test_index = parts.index('test', npm_index)
    except ValueError:
        return command # 'npm' or 'test' not found in expected order

    # Rebuild the command, filtering out --grep and its value
    new_parts = []
    skip_next = False
    for i, part in enumerate(parts):
        if skip_next:
            skip_next = False
            continue

        if part == '--grep':
            # Check if there is a next part to skip
            if i + 1 < len(parts):
                skip_next = True
            continue

        # Also handle --grep=value
        if part.startswith('--grep='):
            continue

        new_parts.append(part)

    normalized_command = ' '.join(new_parts)

    # Clean up trailing '--' if it's now at the end
    if normalized_command.endswith(' --'):
        normalized_command = normalized_command[:-3].strip()

    return normalized_command


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No input, nothing to do
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        # Not a bash command, so we don't need to do anything
        print(json.dumps(input_data))
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        # No command, nothing to do
        print(json.dumps(input_data))
        sys.exit(0)

    normalized_command = normalize_npm_test_command(command)

    # If the command was changed, update the input data
    if normalized_command != command:
        input_data["tool_input"]["command"] = normalized_command

    # Output the modified (or original) input data as JSON
    print(json.dumps(input_data))


if __name__ == "__main__":
    main()
