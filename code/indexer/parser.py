# coding=utf-8

import xml.sax

import config

from document import Document


class WikiSAXHandler(xml.sax.ContentHandler):
    def __init__(self, q):
        self.q = q
        self.pages = 0

        self.currentPath = []
        self.data = ""
        self._locator = None

        self.doc = None

    def setDocumentLocator(self, l):
        self._locator = l

    def startElement(self, name, attr):
        self.currentPath.append(name)
        self.data = ""
        if name == "page":
            self.doc = Document(self._locator.getLineNumber())
            self.pages += 1
        elif name == "redirect":
            self.doc.setRedirect(attr["title"])

    def characters(self, content):
        if self.currentPath[-1] in ["title", "id", "text"]:
            self.data += content

    def endElement(self, name):
        self.currentPath.pop()
        if name == "page":
            self.q.put(self.doc)
            self.doc = None
        elif name == "title":
            self.doc.setTitle(self.data)
        elif name == "id" and self.currentPath[-1] == "revision":
            self.doc.setRevId(self.data)
        elif name == "id" and self.currentPath[-1] == "page":
            self.doc.setId(self.data)
        elif name == "text":
            self.doc.setText(self.data)

    def endDocument(self):
        for i in xrange(config.preprocessorPoolSize):
            self.q.put("stop")
        self.q.close()
        self.q.join()


def parseXML(filePath, parsedDocs):
    # create an XMLReader
    parser = xml.sax.make_parser()

    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = WikiSAXHandler(parsedDocs)
    parser.setContentHandler(Handler)

    parser.parse(filePath)
