# coding=utf-8

import sys
from indexer import indexer


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: merge <index_dir_name> <file_index>\n")
        exit(1)

    index = indexer.Index(sys.argv[1])
    index.fileIndex = int(sys.argv[2])

    index.finalize()
