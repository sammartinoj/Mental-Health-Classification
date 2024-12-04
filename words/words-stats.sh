input = $HOME/text_tools_project/pos/tagged-csvs
output = $HOME/text_tools_project/words/word-count.txt
echo "file,word,count > "$output"

for file in "$input"/*csv; do 
	echo "Working on... $(basename "$file")..."
	cut -d ',' -f3 "$file" | tr [A-Z][a-z] 
