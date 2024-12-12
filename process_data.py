""" Programa que gera a tabela de frequências de um texto (passado como argumento do programa) """

import sys
import json
import itertools 
from unidecode import unidecode 
from string import ascii_lowercase
from math import log2

fname = sys.argv[1]
with open(fname) as f:
    data = unidecode(f.read()).lower()

data = ''.join(filter(lambda c: c in ascii_lowercase, data))

dct_occur = {}
for i in range(len(data) - 1):
    par = data[i:i+2]
    if par not in dct_occur:
        dct_occur[par] = 1
    else:
        dct_occur[par] += 1
    par = data[i:i+3]
    if par not in dct_occur:
        dct_occur[par] = 1
    else:
        dct_occur[par] += 1

        
dct_prob = {}

for a in ascii_lowercase:
    tota = sum(dct_occur[a+x] for x in ascii_lowercase if (a+x) in dct_occur) + len(ascii_lowercase)
    tota = log2(tota)
    
    for b in ascii_lowercase:
        par = a + b
        
        if par not in dct_occur:
            #dct_prob[par] = 1 / tota
            dct_prob[par] = -tota 
        else:
            #dct_prob[par] = (dct_occur[par] + 1) / tota
            dct_prob[par] = log2(dct_occur[par] + 1) - tota

for a, b in itertools.product(ascii_lowercase, repeat=2):
    tota = sum(dct_occur[a+b+x] for x in ascii_lowercase if (a+b+x) in dct_occur) + len(ascii_lowercase)**2
    tota = log2(tota)

    for c in ascii_lowercase:
        tri = a + b + c
        if tri not in dct_occur:
            dct_prob[tri] = -tota
        else:
            dct_prob[tri] = log2(dct_occur[tri] + 1) - tota 

print(json.dumps(dct_prob))

