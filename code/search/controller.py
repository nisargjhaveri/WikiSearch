# coding=utf-8

# from multiprocessing import Process, Queue

import search
import server


def start(indexDir):
    # searchQueue = Queue()
    # resultQueue = Queue()
    #
    # preprocessorProcess = Process(
    #     target=searchHandler.handleQueue,
    #     args=(searchQueue, resultQueue),
    # )
    # preprocessorProcess.start()

    print "Initializing... Please wait (this may take around a minute)"

    search.initialize(indexDir)

    bold_start = "\033[1m"
    bold_end = "\033[0;0m"
    light_red_start = "\033[1;31m"
    green_start = "\033[0;32m"
    cyan_start = "\033[0;36m"
    color_end = "\033[0m"
    while True:
        print light_red_start + "Enter query" + color_end
        query = raw_input()

        result = search.search(query.strip())

        print cyan_start + \
            "Results showed in", result["time"], "seconds" + \
            color_end
        for page in result["pages"]:
            print bold_start + green_start + page[1] + bold_end + color_end, \
                '(' + page[0] + ')'

    # server.start(indexDir)
