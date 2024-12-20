cut -f1 -d':' suicidal_4grams.txt > /$HOME/text-tools-project/word_suicidal_4grams.txt
cut -f1 -d':' depression_4grams.txt > word_depression_4grams.txt
cat word_depression_4grams.txt | sort > depression_4sort.txt
cat word_suicidal_4grams.txt | sort > suicidal_4sort.txt

comm -13 depression_4sort.txt suicidal_4sort.txt | grep -E 'tomorrow|tonight|today' | wc -w
