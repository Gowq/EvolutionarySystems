import sys
import json
import itertools 
from unidecode import unidecode 
from string import ascii_lowercase
from math import log2

# Read the input file passed as a command-line argument
fname = sys.argv[1]
with open(fname) as f:
    # Normalize text by removing accents and converting to lowercase
    data = unidecode(f.read()).lower()

# Filter the text to keep only lowercase alphabets
data = ''.join(filter(lambda c: c in ascii_lowercase, data))

# Dictionary to store occurrences of 2-grams and 3-grams
dct_occur = {}

# Generate the frequency of 2-grams and 3-grams in the text
for i in range(len(data) - 1):
    # 2-gram
    par_2gram = data[i:i+2]
    dct_occur[par_2gram] = dct_occur.get(par_2gram, 0) + 1
    
    # 3-gram
    # par_3gram = data[i:i+3]
    # dct_occur[par_3gram] = dct_occur.get(par_3gram, 0) + 1

# Dictionary to store the probabilities (or entropy-based values) of 2-grams and 3-grams
dct_prob = {}

# Calculate probabilities for 2-grams
for a in ascii_lowercase:
    # Total count of all possible 2-grams starting with 'a'
    total_2gram_count = sum(dct_occur.get(a + x, 0) for x in ascii_lowercase) + len(ascii_lowercase)
    total_2gram_count = log2(total_2gram_count)
    
    # Calculate the log-probability for each 2-gram (a + b)
    for b in ascii_lowercase:
        par_2gram = a + b
        if par_2gram not in dct_occur:
            # If the 2-gram doesn't exist, assign it a log-probability value
            dct_prob[par_2gram] = -total_2gram_count
        else:
            # Apply Laplace smoothing to the probability calculation
            dct_prob[par_2gram] = log2(dct_occur[par_2gram] + 1) - total_2gram_count

# Calculate probabilities for 3-grams
# for a, b in itertools.product(ascii_lowercase, repeat=2):
#     # Total count of all possible 3-grams starting with 'a' and 'b'
#     total_3gram_count = sum(dct_occur.get(a + b + x, 0) for x in ascii_lowercase) + len(ascii_lowercase) ** 2
#     total_3gram_count = log2(total_3gram_count)
    
#     # Calculate the log-probability for each 3-gram (a + b + c)
#     for c in ascii_lowercase:
#         tri_3gram = a + b + c
#         if tri_3gram not in dct_occur:
#             # If the 3-gram doesn't exist, assign it a log-probability value
#             dct_prob[tri_3gram] = -total_3gram_count
#         else:
#             # Apply Laplace smoothing to the probability calculation
#             dct_prob[tri_3gram] = log2(dct_occur[tri_3gram] + 1) - total_3gram_count

# Output the resulting probabilities in JSON format
print(json.dumps(dct_prob))
