#!/bin/bash

input="$HOME/text_tools_project/mini-csvs"

for file in "$input"/*; do
	row_count=$(tail -n +2 "$file" | wc -l)
	echo "$(basename "$file") example count: $row_count"
done
