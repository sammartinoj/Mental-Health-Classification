#!/bin/bash

folder="$HOME/text_tools_project/pos/tagged-csvs"

new_file="pos_count.txt"

tags=("NOUN" "VERB" "ADJ" "ADV" "PRON" "PROPN" "AUX" "MD" "DET" "CONJ" "SCONJ" "INTJ" "SYM")

for file in "$folder"/*.csv; do
	file_name=$(basename "$file")
	echo "Working on: $file_name"

	echo "Counts for $file_name:" >> "$new_file"
	temp_file=$(mktemp)

	for pos in "${tags[@]}"; do
		counter=$(cut -d',' -f5 "$file" | grep -c "^$pos$")
		
		echo "$pos: $counter" >> "$temp_file"
	done

	sort -t':' -k2 -nr "$temp_file" >> "$new_file"
	echo "" >> "$new_file"
done
echo "Check $new_file for results!"

