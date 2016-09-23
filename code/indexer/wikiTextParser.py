# coding=utf-8

import HTMLParser
import re

html_parser = None


def html_decode(text):
    global html_parser
    if not html_parser:
        html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(text)


def parseText(text):
    removeRe = re.compile(ur"(<!--.*?-->|<su[bp].*?>)", re.DOTALL)
    text = re.sub(removeRe, "", text)

    n = 1
    findLinkRe = re.compile(ur"\[\[([^\]]*?)\]\]", re.DOTALL)
    # replaceLinkRe = re.compile(ur"\[\[(?:[^\]]*?\|)*([^\]]*?)\]\]",
    #                            re.DOTALL)
    while n:
        # print "Printing match"
        # for i in re.finditer(linkRe, text):
        #     print i.group()
        text, n = re.subn(findLinkRe,
                          lambda x: x.group(1).split('|')[-1],
                          text)

    # url = re.compile(ur"((?:https?|ftp)\:\/\/[^\]\s]+)(?:[\?\#][^\]\s]+)?")
    # text = re.sub(url, lambda a: urllib.unquote(a.groups()[0]), text)
    url = re.compile(ur"((?:https?|ftp)\:\/\/[^\]\s]+)")
    text = re.sub(url, "", text)

    return text


def getTitles(text):
    return ([
        re.findall(ur"^==([^=]*)==$", text, re.M),
        re.findall(ur"^===([^=]*)===$", text, re.M),
        re.findall(ur"^====([^=]*)====$", text, re.M),
        re.findall(ur"^=====([^=]*)=====$", text, re.M)
    ], re.sub(ur"^==.*==$", "", text, flags=re.M))


def getSection(sectionName, text, remove=True):
    secRe = re.compile(ur"^==\s*" + sectionName.lower() +
                       ur"\s*==\s*$(.*?)^(?:==|$)", re.M | re.I | re.S)

    section = re.findall(secRe, text)

    if remove:
        text = re.sub(secRe, u"==", text)

    return section, text


def parseTemplates(text):
    class local:
        info = ""

    def handleTemplate(templateMatch):
        templateParts = templateMatch.group().split('|')
        templateName = templateParts[0]
        if len(templateName.split()) and templateName.split()[0] == "cite":
            return re.sub("(isbn|id)\s*=.*?\|", "", templateMatch.group())
        elif templateName == "main" or templateName == "see also" \
                or templateName == "quote":
            return ' '.join(templateParts[1:])
        elif templateName.split()[0] == "infobox":
            local.info += ' '.join(templateParts[1:])

        return ""

    templateRe = re.compile(ur"\{\{([^\}]*?)\}\}", re.M | re.S)
    text = re.sub(templateRe, handleTemplate, text)

    return local.info, text


def wikiTextParse(text):
    text = html_decode(text).lower()

    # print "templates"
    infobox, text = parseTemplates(text)
    # print "templates"
    infobox = parseText(infobox)

    # print "ref"
    refSec, text = getSection("References?", text)

    refRe = re.compile(ur"\<ref(?:\s[^\>]*[^\/])?(?:\>(.*?)\<\/ref|\/)\>",
                       re.DOTALL)
    refs = ' '.join(re.findall(refRe, text))
    refs += ' '.join(refSec)
    refs = parseText(refs)
    text = re.sub(refRe, "", text)

    # print "cat"
    catRe = re.compile(ur"\[\[category:(.*?)\]\]", re.DOTALL)
    categories = re.findall(catRe, text)
    text = re.sub(catRe, "", text)

    # print "links"
    links, text = getSection("External links", text)
    links = parseText(' '.join(links))

    # print "titles"
    titles, text = getTitles(text)

    # print "parse"
    text = parseText(text)

    return (
        text,
        titles,
        refs,
        categories,
        links,
        infobox
    )
