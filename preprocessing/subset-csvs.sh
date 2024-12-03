#!/bin/bash

file="$HOME/data/cleaned-output"
mkdir "$HOME/text_tools_project/data/mini-csvs

while read -r line; do
	category=$(echo "$line" | cut -f3 -d ',')
	if [ -s mini-csvs/"$category.csv" ]; then
		echo $line >> $HOME/mini-csvs/$category.csv
	else
		echo $line > $HOME/mini-csvs/$category.csv
	fi
done < $file
