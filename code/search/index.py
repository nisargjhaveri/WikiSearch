# coding=utf-8

import cPickle
import array
from bisect import bisect_left
# import datetime


class Index:
    fullIndexName = "index.full"
    secondIndexName = "index.second"
    synonymIndexName = "index.syn"
    titlesIndexName = "index.titles"

    def __init__(self, indexDir):
        self.indexDir = indexDir
        self.wordIndex = []
        self.posIndex = array.array('L')
        self.freqIndex = array.array('I')
        self.synonymIndex = {}

        self.docList = array.array('L')
        self.titlePos = array.array('I')

        self.loadSecondary()
        self.fullIndexFile = open(self.getFilename("full"), "r")
        self.titlesIndexFile = open(self.getFilename("titles"), "r")

    def getFilename(self, type):
        if type == "full":
            return self.indexDir + '/' + self.fullIndexName
        elif type == "second":
            return self.indexDir + '/' + self.secondIndexName
        elif type == "synonym":
            return self.indexDir + '/' + self.synonymIndexName
        elif type == "titles":
            return self.indexDir + '/' + self.titlesIndexName

    def loadSecondary(self):
        with open(self.getFilename("second"), "rb") as infile:
            size = cPickle.load(infile)
            for i in xrange(size):
                posting = cPickle.load(infile)
                self.wordIndex.append(posting[0])
                self.posIndex.append(posting[1])
                self.freqIndex.append(posting[2])

        with open(self.getFilename("synonym"), "rb") as infile:
            self.synonymIndex = cPickle.load(infile)

        with open(self.getFilename("titles"), "r") as infile:
            pos = 0
            for line in infile:
                self.docList.append(int(line.split(':', 1)[0]))
                self.titlePos.append(pos)
                pos += len(line)

    def getTitle(self, docId):
        i = bisect_left(self.docList, docId)
        pos = None
        if i != len(self.docList) and self.docList[i] == docId:
            pos = self.titlePos[i]

        if pos is None:
            return None

        self.titlesIndexFile.seek(pos)
        line = self.titlesIndexFile.readline()
        return unicode(line.split(':', 1)[1], 'utf-8').strip()

    def _getPos(self, word):
        i = bisect_left(self.wordIndex, word)
        if i != len(self.wordIndex) and self.wordIndex[i] == word:
            return i
        return None

    def getSynonyms(self, term):
        if term in self.synonymIndex:
            return self.synonymIndex[term]
        return [term]

    def getCount(self, word):
        words = self.getSynonyms(word)

        count = 0
        for word in words:
            pos = self._getPos(word)
            if pos:
                count += self.freqIndex[pos]

        return count

    def getPosting(self, word):
        # print "Searching for", word, datetime.datetime.now()

        origWord = word

        words = self.getSynonyms(word)

        totalCount = 0
        postings = {}
        for word in words:
            pos = self._getPos(word)

            if pos is None:
                # print "Not found"
                continue
            else:
                totalCount += self.freqIndex[pos]
                # print "Seeking", datetime.datetime.now()
                self.fullIndexFile.seek(self.posIndex[pos])
                # print "Reading", datetime.datetime.now()
                line = unicode(self.fullIndexFile.readline().strip(), 'utf-8')
                # print "Posting retrieved", datetime.datetime.now()

                for doc in line.split(':')[1][:-1].split(','):
                    doc = doc.rsplit('_', 1)
                    if doc[0] not in postings:
                        postings[doc[0]] = 0
                    postings[doc[0]] += int(doc[1])

        # print origWord, totalCount
        return postings
