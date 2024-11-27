#!/bin/bash

file="cleaned-output"

while read -r line; do
	category=$(echo "$line" | cut -f3 -d ',')
	if [ -s "$category.csv" ]; then
		echo $line >> $category.csv
	else
		echo $line > $category.csv
	fi
done < $file
