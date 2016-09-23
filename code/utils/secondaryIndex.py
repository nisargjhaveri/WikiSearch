# coding=utf-8

import sys
import cPickle


def secondaryIndex(inFilename, outFilename):
    index = []
    infile = open(inFilename, "r")

    pos = 0
    for i, line in enumerate(infile):
        parts = (unicode(line[:line.rfind(':')], "utf-8")).rsplit('_', 1)
        word = (parts[0], pos, int(parts[1]))
        index.append(word)
        pos += len(line)

    infile.close()

    print len(index)

    with open(outFilename, "wb") as outfile:
        cPickle.dump(len(index), outfile, 2)
        for entry in index:
            cPickle.dump(entry, outfile, 2)

    outfile.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: merge <index_file> <out_index>\n")
        exit(1)

    secondaryIndex(sys.argv[1], sys.argv[2])
