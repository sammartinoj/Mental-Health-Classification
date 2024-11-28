#!/bin/bash

file="cleaned-output"

while read -r line; do
	category=$(echo "$line" | cut -f3 -d ',')
	if [ -s mini-csvs/"$category.csv" ]; then
		echo $line >> mini-csvs/$category.csv
	else
		echo $line > mini-csvs/$category.csv
	fi
done < $file
