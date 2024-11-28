#!/bin/bash

file="mental-health.csv"
cat $file | sed -e '/^[[:space:]]*$/d'|tr -s ' '| tr -d '\r' |sed 's/--//g'|sed '/,,/d' | perl -0777 -pe 's/[\n]*([^\d])/\1/g'> temp-output 

tr -cd "A-Za-z0-9,\n\'\!\?\. " < temp-output | tr -s ' '|sed 's/Personality disorder/Personality-disorder/g' > cleaned-output
 
cat cleaned-output | cut -f3 -d ','|sort|uniq -c > disorders
cat cleaned-output | cut -f2 -d ',' > statements
