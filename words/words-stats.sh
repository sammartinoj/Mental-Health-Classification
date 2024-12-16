input="$HOME/tat/files"

output="$HOME/tat/temp-counts.txt"


for file in "$input/"* ; do
    echo "Working on... $(basename "$file")..."
    echo "$(basename "$file")" >> "$output"
    
    cut -f3 -d ',' "$file" | tr 'A-Z' 'a-z' | sed -e "s/'d/ would/g" -e "s/n't/ not/g" -e "s/'m/ am/g" -e "s/'ve/ have/g" -e "s/'ll/ will/g" |sed -e '/[[:punct:]]/d'|tr -d '0-9'| sed -e '/^[[:space:]]*$/d'| sort > "temp.txt"
        
    while read -r line; do
        var=$(comm -23 $line stopwords.txt)
        
        if [ -n $var ]; then
            $var >> "test.txt"
        fi
            
    done > "temp.txt" 
    
    uniq -c "test.txt" | sort -nr | head >> $output
    rm "test.txt"
    rm "temp.txt"
    
done

echo 'done'
