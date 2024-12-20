#!/bin/bash
# Change to file of choice
cat /$HOME/text_tools_project/mini-csvs/Suicidal.csv | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z ]//g' | sed 's/[0-9]//g' | tr -s ' ' > preprocessed_suicidal.txt
echo "File preprocessed. Check file name and run anygrams.py"
