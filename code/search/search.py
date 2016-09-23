# coding=utf-8

import math
import datetime
import re

from index import Index
from common.tokenizer import tokenize


fields = {
    'title': '_t',
    'ref': '_r',
    'heading': '_h',
    'body': '_b',
    'cat': '_c',
    'link': '_l',
    'info': '_i'
}

field_weights = {
    't': 6,
    'h': 5,
    'r': 4,
    'c': 3,
    'l': 2,
    'i': 1
}

penalizeChars = re.compile(ur'[.\/\\\|:\.]')


class Candidate:
    def __init__(self):
        self.present = 0
        self.score = 0
        self.titleScore = 0.0

    def addWord(self):
        self.present += 1

    def addScore(self, n):
        self.score += n

    def setTitle(self, title):
        self.title = title

        titleTokens = tokenize(title)
        badChars = len(re.findall(penalizeChars, title)) + 1
        if titleTokens:
            self.titleScore = (1.0 / len(titleTokens)) + (1.0 / badChars)

    def getTitle(self):
        return self.title

    def getFinalScore(self):
        return self.present + math.log10(self.score) + self.titleScore


def initialize(indexDir):
    global index
    index = Index(indexDir)


def proecssTerm(term):
    field = None
    if (term.find(':') > -1):
        field = term.split(':', 1)[0]

    search_ns = None

    if field and field in fields:
        search_ns = fields[field]
        term = term.split(':', 1)[1]

    tokens = tokenize(term, False)

    if search_ns is None:
        search_terms = []
        for token in tokens:
            search_terms.append(token + '_t')

            if index.getCount(token + '_t') < 1000:
                search_terms.append(token + '_h')

                if index.getCount(token + '_h') < 1000:
                    search_terms.append(token + '_i')

                    if index.getCount(token + '_i') < 1000:
                        search_terms.append(token + '_b')

                        if index.getCount(token + '_b') < 1000:
                            search_terms.append(token + '_c')
    else:
        search_terms = map(lambda x: x + search_ns, tokens)

    return search_terms


def getResults(postings):
    commonDocs = {}

    toIntersect = []

    for term in postings:
        if not postings[term]:
            continue
        if len(postings[term]) > 10000:
            toIntersect.append((len(postings[term]), postings[term]))
            continue
        for doc in postings[term]:
            if doc not in commonDocs:
                commonDocs[doc] = Candidate()
                commonDocs[doc].setTitle(index.getTitle(int(doc)))

            commonDocs[doc].addWord()
            commonDocs[doc].addScore(postings[term][doc])

    toIntersect.sort(key=lambda x: x[0])

    for l, posting in toIntersect:
        if len(commonDocs) < 100:
            # Copy of the code in the previous loop
            for doc in posting:
                if doc not in commonDocs:
                    commonDocs[doc] = Candidate()
                    commonDocs[doc].setTitle(index.getTitle(int(doc)))

                commonDocs[doc].addWord()
                commonDocs[doc].addScore(posting[doc])
        else:
            for doc in posting:
                if doc in commonDocs:
                    commonDocs[doc].addWord()
                    commonDocs[doc].addScore(posting[doc])

    return commonDocs


def search(query):
    startTime = datetime.datetime.now()
    terms = query.strip().lower().split()

    searchTerms = []

    for term in terms:
        searchTerms.extend(proecssTerm(term))

    # print searchTerms

    postings = {}

    for term in searchTerms:
        postings[term] = index.getPosting(term)

    results = getResults(postings)
    results = sorted(results.items(),
                     key=lambda x: x[1].getFinalScore(),
                     reverse=True)

    endTime = datetime.datetime.now()
    timeTaken = endTime - startTime

    searchResult = {
        'time': timeTaken.total_seconds(),
        'pages': []
    }

    # print "Results showed in", timeTaken.total_seconds(), "seconds"

    for i in xrange(min(len(results), 20)):
        searchResult['pages'].append((
            results[i][0],
            results[i][1].getTitle(),
            results[i][1].getFinalScore(),
        ))
        # print results[i][1].getFinalScore(), \
        #       results[i][0], \
        #       results[i][1].getTitle()

    return searchResult
