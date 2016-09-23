# coding=utf-8

import sys
import cPickle

wordIndex = {}
synIndex = {}


def load(inFilename, outFilename):
    with open(inFilename, "rb") as infile:
        size = cPickle.load(infile)
        for i in xrange(size):
            posting = cPickle.load(infile)
            low = posting[0].lower()
            if low not in wordIndex:
                wordIndex[low] = []
            wordIndex[low].append(posting[0])

    for word in wordIndex:
        if len(wordIndex[word]) > 1:
            synIndex[word] = wordIndex[word]

    with open(outFilename, "wb") as outfile:
        cPickle.dump(synIndex, outfile, 2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: merge <secondary_index> <out_index>\n")
        exit(1)

    load(sys.argv[1], sys.argv[2])
