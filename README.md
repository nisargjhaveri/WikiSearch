WikiSearch - IRE mini-project
================

> Please note that project is dead! It was a course project and I never touched it again.

What is it?
-----------
This is small hand-made search engine for Wikipedia.
Developed as a part of course project for course Information Retrieval and Extraction in Spring 2016 at IIIT Hyderabad.

Given a Wikipedia xml dump, it is supposed to index it, and then use the index to perform queries later. This will work better for English, for other languages some updates are required in tokenizer and stemmer.

How to Use
----------
First, index.

Then, run the search interface. You can use following field queries, or can just write simple query and the engine takes care of everything else!

- title:
- heading:
- info:
- body:
- link:
- cat:
- ref:

You need to write this for every word.

To run
------
### Indexing

`$ ./index index <wikidump_xml> <index_out_dir>`

- `<wikidump_xml>` is an valid wikipedia XML dump.
- `<index_out_dir>` will be created

You need to build secondary indexes once the primary index is built. The scripts for these are in `code/utils`.

### Search
`$ ./index search <index_dir>`

This might take about a minute to start.
