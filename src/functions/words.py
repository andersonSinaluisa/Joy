from sys import path

import numpy as np
from nltk import ngrams
from tqdm.auto import tqdm
from nltk.tokenize import RegexpTokenizer
import src as _
from os import path,stat




def bigram_probs(inital , words, clean_text, n=2):

    denominator= sum(clean_text==inital)
    ngram = list(ngrams(clean_text,n))
    probs=[]

    for i,x in enumerate(words):
        bigram=(inital,x)
        counter =0

        for j,k in enumerate(ngram):
            if k == bigram:
                counter+=1
            else:
                continue
        probs.append(counter)
    final = np.array(probs)/denominator
    return final

def trigram_probs(initial_1, initial_2, words, clean_text, n=3):

    denominator = bigram_probs(initial_1,words,clean_text)[words.index(initial_2)]*np.sum(clean_text==initial_1)
    ngram= list(ngrams(clean_text,n))
    probs=[]

    for i, x in enumerate(words):
        trigram= (initial_1,initial_2,x)
        counter=0

        for j,k in enumerate(ngram):
            if k == trigram:
                counter+=1
            else:
                continue
        probs.append(counter)

    final= np.array(probs)/denominator
    return final
def senteces(words, clean_text, freq, n=5):
    #primera palabra

    string1 = np.random.choice(words, p=freq)
    sol = string1

    #siguiente palabra
    bi_prob = bigram_probs(string1,words,clean_text)
    string2= np.random.choice(words,p=bi_prob)
    sol = string1 +' '+string2

    for i in tqdm(range(n-2)):
        tri_prob =trigram_probs(string1,string2,words,clean_text)
        new = np.random.choice(words,p=tri_prob)
        sol =sol+' '+new
        string1=string2
        string2=new

    return sol


np.seterr(divide='ignore', invalid='ignore')
ruta = path.join(_.DIRNAME, 'files/listword.txt')
rutaf = ruta.replace('\\', '/')
with open(rutaf) as f:
    text = f.read()
tokenizer = RegexpTokenizer(r'\w+')
clean_text = np.array(tokenizer.tokenize(text.lower()))

long_string = ' '
for i in clean_text:
    long_string=long_string+i+''



frequency =[]
words=[]

for word in set(clean_text):
    frequency.append(long_string.count(' '+word+' '))
    words.append(word)


freq = list(frequency / np.sum(frequency))

senteces(words,clean_text,frequency)