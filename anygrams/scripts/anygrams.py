import nltk
from nltk.util import ngrams
from collections import Counter

# Tokenize
def tokenize(text):
    words = text.split()  # Tokenize by splitting on spaces
    return words

# File organizing / ngram specs
input_file = input("Enter the file name you generated in preprocess_for_ngrams.sh: ")
output_file = input("What would you like to call your file? ")
n = int(input("Enter the value of n for n-grams (1 for unigrams, 2 for bigrams, and so on): "))

with open(input_file, "r") as f:
    text = f.read()

# Call tokenizer
words = tokenize(text)

# Generate n-grams
ngrams_list = list(ngrams(words, n))

# Keep track of frequencies
ngram_counts = Counter(ngrams_list)

# Write n-grams to output file
with open(output_file, "w") as f:
    for ngram, count in ngram_counts.most_common():
        f.write(f"{' '.join(ngram)}: {count}\n")

print(f"Your {n}-gram counts have been saved to '{output_file}'. Create another ngrams file, then edit file names in sort_comm.sh accordingly to capture unique ngrams between any two disorders files.")
