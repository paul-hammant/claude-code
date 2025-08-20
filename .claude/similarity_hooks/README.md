# Command Similarity Hook System (Reference Implementation)

This directory contains a reference implementation for a hypothetical command similarity hook system for the Claude Code agent.

## Purpose

This system allows you to define rules that "normalize" commands before the agent checks if they are similar to a previously approved command. This is useful for cases where commands are functionally similar but have different parameters, such as:

- `npm test -- --grep "feature-a"` vs `npm test -- --grep "feature-b"`
- `timeout 30 my_command` vs `timeout 60 my_command`

By normalizing these commands to a common string (e.g., `npm test` or `timeout [timeout_duration] my_command`), you can give blanket approval to the normalized form once, and the agent will not have to ask for permission again for variations.

**Note:** This is a reference implementation built "as if" a dedicated hook for this purpose existed in the Claude agent. The central dispatcher script (`/.claude/normalise_for_previously_run_check.sh`) simulates how such a hook would operate.

## How It Works

1.  A central dispatcher script (`/.claude/normalise_for_previously_run_check.sh`) is the entry point. It takes a command string as input.
2.  The dispatcher reads the configuration from `/.claude/similarity_hooks.json`.
3.  This configuration file maps regular expression patterns to normalizer scripts located in this directory.
4.  The dispatcher checks the input command against each pattern.
5.  If a pattern matches, the corresponding script is executed. The script receives the full command on its standard input and should print the normalized command to its standard output.
6.  If no pattern matches, the original command is returned unchanged.

## How to Add a New Normalizer

1.  **Create your normalizer script:**
    -   Create a new script (e.g., `my_normalizer.sh` or `my_normalizer.py`) inside this directory (`/.claude/similarity_hooks/`).
    -   The script must be executable (`chmod +x my_normalizer.sh`).
    -   The script should read a single line of text from standard input (the command to normalize).
    -   It should print a single line of text to standard output (the normalized command).

2.  **Add a rule to the configuration file:**
    -   Open `/.claude/similarity_hooks.json`.
    -   Add a new JSON object to the array with two keys:
        -   `"pattern"`: A regular expression that will trigger your script. Remember to escape backslashes in the JSON string (e.g., `\\d+` for a digit).
        -   `"script"`: The path to your new script, relative to the project root (e.g., `.claude/similarity_hooks/my_normalizer.sh`).
    -   The new rule will be active immediately for the next run.
