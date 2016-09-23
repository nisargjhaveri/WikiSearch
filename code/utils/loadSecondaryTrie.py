# coding=utf-8

import sys
import cPickle

from trie import Trie

index = Trie()


def load(inFilename):
    with open(inFilename, "rb") as infile:
        size = cPickle.load(infile)
        for i in xrange(size):
            posting = cPickle.load(infile)
            index.add(posting[0], posting[1])
            # print i, "/", size, str(float(i)/size) + "%", "\r",

    raw_input()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: merge <secondary_index>\n")
        exit(1)

    load(sys.argv[1])
