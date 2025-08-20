#!/usr/bin/env python3
"""
Claude Code Hook: Auto Approver
===============================
This hook runs as a PreToolUse hook for the Bash tool.
It checks the command against a list of approved patterns and,
if a match is found, returns a JSON object to Claude to
auto-approve the command execution.
"""

import json
import sys
import os
import re

def main():
    # Load the JSON input from stdin, which contains the command details
    try:
        input_data = json.load(sys.stdin)
        command = input_data.get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError):
        # If there's no input or it's malformed, exit silently
        sys.exit(0)

    if not command:
        sys.exit(0)

    # Construct the path to the auto_approve.json file
    # It's assumed to be in the .claude directory at the project root.
    project_dir = os.path.dirname(os.path.dirname(__file__)) # .claude/hooks -> .claude -> project_root
    config_path = os.path.join(project_dir, 'auto_approve.json')

    if not os.path.exists(config_path):
        sys.exit(0)

    # Load the auto-approval rules
    try:
        with open(config_path, 'r') as f:
            rules = json.load(f)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    # Check the command against each rule
    for rule in rules:
        pattern_str = rule.get("pattern")
        reason = rule.get("reason", "Auto-approved by custom hook")

        if not pattern_str:
            continue

        try:
            if re.search(pattern_str, command):
                # Match found. Print the JSON to auto-approve the command.
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "permissionDecisionReason": reason
                    },
                    "suppressOutput": True
                }
                print(json.dumps(output))
                sys.exit(0) # Exit after the first match
        except re.error:
            # Ignore invalid regex patterns in the config
            continue

    # If no rules matched, exit silently to allow the normal permission prompt to proceed.
    sys.exit(0)


if __name__ == "__main__":
    main()
