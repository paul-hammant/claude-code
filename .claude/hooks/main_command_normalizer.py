#!/usr/bin/env python3
"""
Claude Code Hook: Main Command Normalizer
=========================================
This hook runs as a PreToolUse hook for the Bash tool.
It acts as a dispatcher, scanning for and executing specific
normalizer scripts based on regex patterns in their docstrings.
"""

import json
import sys
import os
import re
import subprocess

def get_pattern_from_script(script_path):
    """
    Extracts the 'Pattern:' from a script's docstring.
    """
    with open(script_path, 'r') as f:
        content = f.read()

    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if not docstring_match:
        return None

    docstring = docstring_match.group(1)
    pattern_match = re.search(r'^\s*Pattern:\s*(.*)', docstring, re.MULTILINE)

    if pattern_match:
        return pattern_match.group(1).strip()

    return None

def main():
    try:
        input_data = json.load(sys.stdin)
        command = input_data.get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError):
        sys.exit(0)

    if not command:
        print(json.dumps(input_data))
        sys.exit(0)

    fixers_dir = os.path.join(os.path.dirname(__file__), '..', 'command-similarity-fixes')

    for filename in os.listdir(fixers_dir):
        if filename.endswith('.py'):
            script_path = os.path.join(fixers_dir, filename)
            pattern_str = get_pattern_from_script(script_path)

            if pattern_str:
                try:
                    pattern = re.compile(pattern_str)
                    if pattern.search(command):
                        # This script matches, execute it
                        process = subprocess.run(
                            ['python3', script_path],
                            input=json.dumps(input_data),
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        # Print the output of the normalizer script
                        print(process.stdout)
                        sys.exit(0) # Exit after the first match
                except (re.error, subprocess.CalledProcessError):
                    # Ignore errors in fixer scripts or patterns
                    continue

    # If no fixer matched, just pass the original command through
    print(json.dumps(input_data))

if __name__ == "__main__":
    main()
