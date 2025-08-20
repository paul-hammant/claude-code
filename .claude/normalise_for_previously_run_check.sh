#!/bin/bash

# This script normalizes a command string based on rules defined in
# .claude/similarity_hooks.json.
# It's a reference implementation for a hypothetical 'IsSimilarHook'.

# Input command is the first argument
input_command="$1"

# Config file path
config_file=".claude/similarity_hooks.json"

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq could not be found, passing command through." >&2
    echo "$input_command"
    exit 0
fi

# Read the config and find a matching normalizer
# The `jq -c '.[]'` command iterates over the JSON array, outputting each object on a new line.
while IFS= read -r rule; do
    pattern=$(echo "$rule" | jq -r '.pattern')
    script=$(echo "$rule" | jq -r '.script')

    # Check if the input command matches the pattern
    if [[ "$input_command" =~ $pattern ]]; then
        # If it matches, execute the associated script
        # The original command is passed to the script's standard input
        normalized_command=$(echo "$input_command" | "$script")
        echo "$normalized_command"
        exit 0
    fi
done < <(jq -c '.[]' "$config_file")

# If no rules matched, return the original command
echo "$input_command"
