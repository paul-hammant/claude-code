#!/bin/bash
read -r cmd
echo "$cmd" | sed -E 's/^(timeout) [0-9]+/\1 [timeout_duration]/'
