mkdir -p ./type-token-ratios
new_file="ttr.txt"

for file in $HOME/text_tools_project/data/mini-csvs/*.csv; do
	fn=$(basename "$file")
	echo "Working on..." $fn
	cut -f2 -d ',' "$file" > statement
    sed 's/[[:punct:]]//g' statement | tr 'A-Z' 'a-z' | tr -s ' ' '\n' > statements.out
	tokens=$(wc -w < statements.out)
    types=$(sort -u statements.out | wc -l)

	echo $fn  "type/token ration is:" >> "$new_file"
    awk -v type="$types" -v token="$tokens" 'BEGIN {print type / token}' >> "$new_file"
	echo $tokens "tokens" >> "$new_file"
	echo $types "types" >> "$new_file"
	rm statement
	rm statements.out
done
mv type-token.sh ./type-token-ratios
mv ttr.txt ./type-token-ratios
echo "Type-token-ratios can be found in file" "$new_file"
