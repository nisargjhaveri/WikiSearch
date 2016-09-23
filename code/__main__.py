# coding=utf-8

import sys

if len(sys.argv) < 2:
    sys.stderr.write("Usage: " + sys.argv[0] +
                     " <mode> <options...>\n")
    exit(1)

if sys.argv[1] == 'index':
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: " + sys.argv[0] +
                         " index <wikidump_xml> <index_out_dir>\n")
        exit(1)

    from indexer import controller
    controller.index(sys.argv[2], sys.argv[3])

elif sys.argv[1] == 'search':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: " + sys.argv[0] +
                         " search <index_dir>\n")
        exit(1)

    from search import controller
    # search.controller.start()
    controller.start(sys.argv[2])
