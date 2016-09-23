# coding=utf-8

import sys
import codecs
import cPickle


def convert(inFilename, outFilename):
    with open(inFilename, "rb") as infile:
        index = cPickle.load(infile)

    with codecs.open(outFilename, "w", "utf-8") as outfile:
        for word, pos in index:
            outfile.write(word)
            outfile.write(":")
            outfile.write(str(pos))
            outfile.write("\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: merge <secondary_index_pickle> <out_index>\n")
        exit(1)

    convert(sys.argv[1], sys.argv[2])
