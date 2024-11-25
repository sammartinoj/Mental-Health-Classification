#!/bin/bash

file=$"mental-health.csv"
#sed -e 's/\r//g' $file | sed 's/@//g'|cut -f3 -d ','|sort -u|head
#cut -f2 -d ',' $file > statements
#cut -f3 -d ',' $file > categories

cat $file | sed -e '/^[[:space:]]*$/d'|tr -s ' '| tr -d '\r' |sed 's/--//g'|sed '/,,/d' > temp-file


