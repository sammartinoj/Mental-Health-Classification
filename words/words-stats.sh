input="$HOME/text_tools_project/local"

output="$HOME/text_tools_project/words/word-counts.txt"

for file in "$input/"* ; do
    while IFS=',' read -r col1 col2 col3 col4 col5; do
        word=$col3
        pos=$col5

        if [ "$word" = "'s" ] && [ "$pos" = "AUX" ]; then
            # Replace "'s" with "is" in the file
            sed -i "s/'s/is/g" "$file"
        fi
    done < "$file"

	echo "Working on... $(basename "$file")..."
	echo "$(basename "$file")" >> "$output"
	cut -f3 -d ',' "$file" | tr 'A-Z' 'a-z' | sed -e "s/'d/ would/g" -e "s/n't/ not/g" -e "s/'m/ am/g" -e "s/'ve/ have/g" -e "s/'ll/ will/g" |sort|uniq -c|sort -r |head >>  "$output"
done

