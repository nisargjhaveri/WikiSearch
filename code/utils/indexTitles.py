# coding=utf-8

import xml.sax
import sys


class WikiSAXHandler(xml.sax.ContentHandler):
    def __init__(self, indexFile):
        self.index = open(indexFile, "w")

        self.id = 0
        self.title = ""

        self.currentPath = []
        self.data = ""

    def startElement(self, name, attr):
        self.currentPath.append(name)
        self.data = ""

    def characters(self, content):
        if self.currentPath[-1] in ["title", "id"]:
            self.data += content

    def endElement(self, name):
        self.currentPath.pop()
        if name == "page":
            self.index.write(self.id.encode('utf8'))
            self.index.write(":")
            self.index.write(self.title.encode('utf8'))
            self.index.write("\n")
            self.id = 0
            self.title = ""
        if name == "title":
            self.title = self.data
        elif name == "id" and self.currentPath[-1] == "page":
            self.id = self.data

    def endDocument(self):
        pass


def parseXML(filePath, indexFile):
    # create an XMLReader
    parser = xml.sax.make_parser()

    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = WikiSAXHandler(indexFile)
    parser.setContentHandler(Handler)

    parser.parse(filePath)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: merge <wiki_dump> <out_index>\n")
        exit(1)

    parseXML(sys.argv[1], sys.argv[2])
