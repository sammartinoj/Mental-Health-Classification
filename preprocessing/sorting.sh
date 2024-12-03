#!/bin/bash

file="$HOME/data/cleaned-output"

while read -r line; do
	category=$(echo "$line" | cut -f3 -d ',')
	if [ -s mini-csvs/"$category.csv" ]; then
		echo $line >> $HOME/mini-csvs/$category.csv
	else
		echo $line > $HOME/mini-csvs/$category.csv
	fi
done < $file
