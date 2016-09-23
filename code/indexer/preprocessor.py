# coding=utf-8

from multiprocessing import Value, Process
# import sys
import time
from datetime import datetime

from wikiTextParser import wikiTextParse
from common.tokenizer import tokenize


def preprocess(doc):
    tokens = {
        'docId': doc.id,
        'fields': {
            't': tokenize(doc.title, False),
            'h': [],
            'b': [],
            'r': [],
            'c': [],
            'l': [],
            'i': []
        }
    }

    if doc.redirect is None:
        print doc.id, "WikiTextParsing", datetime.now()
        doc.wikiParsedText, doc.wikiTitles, doc.wikiRefs, doc.wikiCategories,\
            doc.wikiLinks, doc.wikiInfo = wikiTextParse(doc.text)
        print doc.id, "WikiTextParsing Done", datetime.now()

        tokens['fields']['h'] = tokenize(' '.join(
            reduce(lambda a, x: a + x, doc.wikiTitles, [])
        ), False)
        tokens['fields']['b'] = tokenize(doc.wikiParsedText)
        tokens['fields']['r'] = tokenize(doc.wikiRefs)
        tokens['fields']['c'] = tokenize(' '.join(doc.wikiCategories), False)
        tokens['fields']['l'] = tokenize(doc.wikiLinks)
        tokens['fields']['i'] = tokenize(doc.wikiInfo)

    return tokens

parsedDocs = None
processedDocs = None

docs = Value('i', 0)


def preprocessorWoker(parsedDocs, processedDocs, docs):
    while True:
        doc = parsedDocs.get()

        if doc == "stop":
            parsedDocs.task_done()
            return

        print "Processing", doc.id, datetime.now()

        processedDocs.put(preprocess(doc))
        docs.value += 1

        parsedDocs.task_done()
        print doc.id, "Done", datetime.now()

        print "Total", docs.value, "documents processed"


def handleQueue(parsedQueue, processedQueue, preprocessorCount):
    global parsedDocs, processedDocs
    parsedDocs = parsedQueue
    processedDocs = processedQueue

    pool = []
    for i in xrange(preprocessorCount):
        proc = Process(target=preprocessorWoker,
                       args=(parsedDocs, processedDocs, docs),
                       name="preprocessorWoker")
        pool.append(proc)
        proc.start()

    while any(p.is_alive() for p in pool):
        time.sleep(.1)

    for p in pool:
        p.join()

    # preprocessorWoker(parsedDocs, processedDocs, docs)

    print docs.value

    processedDocs.put("stop")
    processedDocs.close()
    processedDocs.join()
