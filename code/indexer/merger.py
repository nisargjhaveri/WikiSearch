# coding=utf-8

import codecs
from collections import deque

import config


class Merger():
    def __init__(self, outFilename):
        self.outfile = codecs.open(outFilename, "w", "utf-8")
        self.filename = []

        self.files = []
        self.inputs = []

        self.merged = []

    def addFile(self, filename):
        self.files.append(codecs.open(filename, "r", "utf-8"))
        self.inputs.append(deque([]))

    def getNextEntry(self, fileIndex):
        file = self.files[fileIndex]

        line = file.readline()

        if line == "":
            return None

        parts = line.split(':')

        token = '_'.join(parts[0].split('_')[:-1])
        postings = map(lambda x: x.split('_'),
                       parts[1].strip()[:-1].split(','))

        return (token, postings)

    def readNextChunk(self, fileIndex):
        inputs = self.inputs[fileIndex]

        line = True
        while line and len(inputs) < config.mergeChunkSize:
            line = self.getNextEntry(fileIndex)
            inputs.append(line)

    def checkAndLoadNextChunks(self):
        for i, input in enumerate(self.inputs):
            if not len(input):
                self.readNextChunk(i)

    def getMin(self):
        candidates = [(i, self.inputs[i][0])
                      for i in xrange(len(self.files))
                      if self.inputs[i][0] is not None]

        if not len(candidates):
            return None

        minToken = min(candidates, key=lambda x: x[1][0])[1][0]

        postings = filter(lambda x: x[1][0] == minToken, candidates)

        mergedPostings = []
        for posting in postings:
            self.inputs[posting[0]].popleft()
            mergedPostings.extend(posting[1][1])

        mergedPostings.sort(key=lambda x: int(x[0]))

        return (minToken, mergedPostings)

    def dumpResults(self):
        for entry in self.merged:
            self.outfile.write(entry[0] + '_' + str(len(entry[1])) + ':')
            for doc in entry[1]:
                self.outfile.write(str(doc[0]) +
                                   "_" + str(doc[1]) + ",")
            self.outfile.write('\n')

        self.merged = []

    def merge(self):
        self.checkAndLoadNextChunks()

        while True:
            nextEntry = self.getMin()

            if nextEntry is None:
                break

            self.merged.append(nextEntry)

            if len(self.merged) >= config.mergedBufferSize:
                self.dumpResults()

            self.checkAndLoadNextChunks()

        self.dumpResults()

        for file in self.files:
            file.close()


if __name__ == "__main__":
    m = Merger('../../index.dump/merged')
    m.addFile('../../index.dump/index0')
    m.addFile('../../index.dump/index1')
    m.addFile('../../index.dump/index2')
    m.merge()
