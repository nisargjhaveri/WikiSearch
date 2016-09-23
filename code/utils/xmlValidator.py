# coding=utf-8

import xml.sax
import sys


def parseXML(filePath):
    # create an XMLReader
    parser = xml.sax.make_parser()

    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    parser.parse(filePath)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: xmlValidator <xml_filename>\n")
        exit(1)

    parseXML(sys.argv[1])
