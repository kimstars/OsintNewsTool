# BM25
An implementation of Okapi BM25 algorithm in C++. The library is splitted into 2 file: header (`BM25.hpp`) & source (`BM25.cpp`)

## Basic Search Engine
This program (`basic_se.cpp`) demonstrates the usage of BM25 library (`BM25.cpp`) and reverse index algorithm to score documents

Usage: `$ {this program} {queries_file} {docs_file} {output prefix}`

`{doc_file}`: For simple demonstration, each doc is a line in this file. Modify the program to suit your needs.

eg. `$ basic_se queries.txt docs.txt res`

It will create 2 output files: `res_bm25` & `res_reverse_index` with format:

````
+---------+-----------+-----------+-----+-----------+
|         |  query-1  |  query-2  | ... |  query-n  |
+---------+-----------+-----------+-----+-----------+
| doc-1   | score-1.1 | score-1.2 | ... | score-1.n |
| doc-2   | score-2.1 | score-2.2 | ... | score-2.n |
| ...     | ...       | ...       | ... | ...       |
| doc-n   | score-n.1 | score-n.2 | ... | score-n.n |
+---------+-----------+-----------+-----+-----------+
````

Note that reverse index algorithm is much simpler, and has worse quality than BM25.

TODO: 
* Work with lower and upper case. Sometimes they are almost the same ("C++" & "c++"), but sometime they are different ("Bill" and "bill")
* Work with non-tone Vietnamese text. We can use the function `utility::remove_vn_tone()` to remove tone, but how to score a non-tone text? We understand that full-tone and none-tone should have similar score (eg. "bún chả rất ngon" and "bun cha rat ngon"), but what exactly?

#### References:

BM25: https://en.wikipedia.org/wiki/Okapi_BM25

Reverse index: https://www.elastic.co/guide/en/elasticsearch/guide/current/inverted-index.html
