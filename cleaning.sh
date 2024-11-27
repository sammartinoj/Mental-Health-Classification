#!/bin/bash

file=$"mental-health.csv"
cat $file | sed -e '/^[[:space:]]*$/d'|tr -s ' '| tr -d '\r' |sed 's/--//g'|sed '/,,/d' | perl -0777 -pe 's/\n([^\d])/\1/g' > bep-bile

cat bep-bile | cut -f3 -d ','|sort|uniq -c > disorders
cat bep-bile | cut -f2 -d ',' > statements
