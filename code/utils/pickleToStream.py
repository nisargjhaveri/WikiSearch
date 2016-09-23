# coding=utf-8

import sys
# import codecs
import cPickle


def convert(inFilename, outFilename):
    with open(inFilename, "rb") as infile:
        index = cPickle.load(infile)

    with open(outFilename, "wb") as outfile:
        cPickle.dump(len(index), outfile, 2)
        for entry in index:
            cPickle.dump(entry, outfile, 2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: merge <secondary_index_pickle> <out_index>\n")
        exit(1)

    convert(sys.argv[1], sys.argv[2])
