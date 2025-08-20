#!/usr/bin/env python3
import sys
import shlex

def normalize_command(command: str) -> str:
    if "npm test" not in command:
        return command

    try:
        parts = shlex.split(command)
    except ValueError:
        parts = command.split()

    npm_index = -1
    for i, part in enumerate(parts):
        if part.endswith('/npm') or part == 'npm':
            npm_index = i
            break

    if npm_index == -1:
        return command # npm not found

    try:
        # Look for 'test' after the 'npm' part
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
    # Read command from stdin
    command = sys.stdin.read().strip()

    if not command:
        sys.exit(0)

    normalized_command = normalize_command(command)
    print(normalized_command)

if __name__ == "__main__":
    main()
