# coding=utf-8

import codecs
import os

import merger

import config


class Index:
    def __init__(self, indexDirName):
        self.dir = indexDirName
        self.fileIndex = 0

        self.index = {}
        self.docs = 0

    def addDoc(self, docId, fields):
        for fieldName in fields:
            for token in fields[fieldName]:
                indexToken = token + "_" + fieldName

                if indexToken not in self.index:
                    self.index[indexToken] = {}

                if docId not in self.index[indexToken]:
                    self.index[indexToken][docId] = 0

                self.index[indexToken][docId] += 1

        self.docs += 1

        if self.docs >= config.indexedDocsInMemory:
            self.dumpTemp()

    def getFilename(self, fileIndex=None):
        if fileIndex is None:
            fileIndex = self.fileIndex
            self.fileIndex += 1

        return self.dir + '/index' + str(fileIndex)

    def dumpTemp(self):
        self.dumpTofile(self.getFilename())

        self.index = {}
        self.docs = 0

    def dumpTofile(self, filename):
        print "Dumping intermediate index to", filename
        tokens = self.index.keys()
        tokens.sort()

        dumpFile = codecs.open(filename, "w", "utf-8")

        for token in tokens:
            docs = sorted(self.index[token].keys(), key=lambda x: int(x))
            dumpFile.write(token + "_" + str(len(self.index[token])) + ":")
            for docId in docs:
                dumpFile.write(str(docId) +
                               "_" + str(self.index[token][docId]) + ",")
            dumpFile.write("\n")
            del self.index[token]

        dumpFile.close()

    def mergeTemp(self, filesToMerge):
        if not filesToMerge or len(filesToMerge) <= 1:
            return

        print "Merging", ', '.join(filesToMerge)

        m = merger.Merger(self.getFilename())
        for file in filesToMerge:
            m.addFile(file)
        m.merge()
        del m

    def finalize(self):
        self.dumpTemp()

        filesToMerge = []
        currentFileIndex = 0
        while True:
            if currentFileIndex >= self.fileIndex:
                break

            filesToMerge.append(self.getFilename(currentFileIndex))

            if config.mergeFileCount <= len(filesToMerge):
                self.mergeTemp(filesToMerge)
                filesToMerge = []

            currentFileIndex += 1

        self.mergeTemp(filesToMerge)


def handleQueue(processedDocs, indexDirName):
    index = Index(indexDirName)

    if not os.path.exists(indexDirName):
        os.makedirs(indexDirName)

    while True:
        doc = processedDocs.get()

        if doc == "stop":
            processedDocs.task_done()
            break

        index.addDoc(doc["docId"], doc["fields"])

        processedDocs.task_done()

    index.finalize()
