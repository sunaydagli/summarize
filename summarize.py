import nltk
from sys import argv
from io import open
from os import path
from heapq import nlargest
from string import punctuation, printable
print( 'Number of arguments:', len(argv), 'arguments.')
text = ''
if path.isfile(argv[1]):
    with open(argv[1],'r',encoding='utf-8',errors='ignore') as infile, \
     open(argv[1] + '_ascii','w',encoding='ascii',errors='ignore') as outfile:
        for line in infile:
            text += line
elif len(argv) == 2:
    text = argv[1]
else:
    for i in range(1,len(argv)):
        text += argv[i]
        if (i != len(argv) - 1):
            text += ' '
def summarize(text):
    if text.count('. ') > 20:
        length = int(round(text.count('. ') / 10, 0))
    else:
        length = 1

    nopunc = [char for char in text if char not in punctuation]
    nopunc = ''.join(nopunc)

    processed_text = [word for word in nopunc.split() if word.lower() not in nltk.corpus.stopwords.words('english')]

    word_freq = {}
    for word in processed_text:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] = word_freq[word] + 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = (word_freq[word]/max_freq)

    sent_list = nltk.sent_tokenize(text)
    sent_score = {}
    for sent in sent_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word]
                else:
                    sent_score[sent] = sent_score[sent] + word_freq[word]

    summary_sents = nlargest(length, sent_score, key=sent_score.get)
    summary = " ".join(summary_sents)
    return summary
# summarize(text)
    