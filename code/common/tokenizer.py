# coding=utf-8

import re

from PorterStemmer import PorterStemmer
stemmer = PorterStemmer()

punct_space = re.compile(ur"[\\\/\{\}\(\)\<\>\:\!\?\;\|\=\*\&\$\#\@\^\-\+\×\%\.\,\"“”″•֊‐‑‒–—―⸺⸻〜﹘﹣－−__]")
punct_nospace = re.compile(ur"[\'\`′‘’\[\]]")

stopwords = ["i", "a", "about", "an", "are", "as", "at", "be", "by", "com", "for", "from", "how", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when", "where", "who", "will", "with", "the", "www"]


def tokenize(text, removeStopwords=True):
    text = re.sub(punct_space, " ", text)
    text = re.sub(punct_nospace, "", text)

    tokens = text.split()
    if (removeStopwords):
        tokens = filter(lambda x: x and x not in stopwords, tokens)
    # tokens = map(lambda x: stemmer.stem(x, 0, len(x) - 1), tokens)

    return tokens
