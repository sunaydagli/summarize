from flask import Flask
from flask import request
from re import sub

import nltk
from sys import argv
from io import open
from os import path
from heapq import nlargest
from string import punctuation, printable

app = Flask(__name__)

@app.route("/")
def index():
    text = request.args.get("text", "")
    print(text)
    summarized = summarize_text(text)
    return (
        """<form action="" method="get">
                <input type="text" name="text">
                <input type="submit" value="Summarize">
            </form>"""
        + summarized
    )

def summarize_text(text):
    """Convert Celsius to Fahrenheit degrees."""
    printable_ = set(printable)
    modified_string = ''.join(filter(lambda x: x in printable, text))
    print(modified_string)
    return summarize(modified_string)

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)