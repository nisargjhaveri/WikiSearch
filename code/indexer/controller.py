# coding=utf-8

from multiprocessing import Process, JoinableQueue

import parser
import preprocessor
import indexer

import config


def index(xmlFilePath, indexFilename):
    preprocessorCount = config.preprocessorPoolSize

    parsedDocs = JoinableQueue(config.parsedDocsQueueSize)
    processedDocs = JoinableQueue(config.processedDocsQueueSize)

    parserProcess = Process(
        target=parser.parseXML,
        args=(xmlFilePath, parsedDocs),
    )
    parserProcess.start()

    preprocessorProcess = Process(
        target=preprocessor.handleQueue,
        args=(parsedDocs, processedDocs, preprocessorCount),
    )
    preprocessorProcess.start()

    indexProcess = Process(
        target=indexer.handleQueue,
        args=(processedDocs, indexFilename),
    )
    indexProcess.start()

    parserProcess.join()
    preprocessorProcess.join()
    indexProcess.join()
