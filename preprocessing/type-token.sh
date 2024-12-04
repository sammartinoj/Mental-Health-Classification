for file in $HOME/text_tools_project/data/mini-csvs/*.csv; do
	cut -f2 -d ',' "$file" > statement
    sed 's/[[:punct:]]//g' statement | tr 'A-Z' 'a-z' | tr -s ' ' '\n' > statements.out
	tokens=$(wc -w < statements.out)
    types=$(sort -u statements.out | wc -l)
	fn=$(basename "$file")

	echo $fn  "type/token ration is:" 
    awk -v type="$types" -v token="$tokens" 'BEGIN {print type / token}'
	rm statement
	rm statements.out
done

