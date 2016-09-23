# coding=utf-8

class Document():
    def __init__(self, lineNo):
        self.lineNo = lineNo
        self.id = None
        self.title = ""
        self.redirect = None
        self.revId = None
        self.text = ""

        self.wikiParsedText = None
        self.wikiTitles = None
        self.wikiRefs = None
        self.wikiCategories = None
        self.wikiLinks = None
        self.wikiInfo = None

    def setId(self, id):
        self.id = id

    def setTitle(self, title):
        self.title = title

    def setRedirect(self, redirect):
        self.redirect = redirect

    def setRevId(self, revId):
        self.revId = revId

    def setText(self, text):
        self.text = text
