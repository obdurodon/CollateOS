#!/usr/bin/env python
# -*-coding: utf8-*-
# ==============================================================================
# Filename:  collate.py
# Developer: David J. Birnbaum (djbpitt@gmail.com; http://www.obdurodon.org)
# Date:      Created 2013-06-28; last modified 2013-06-28
# Summary:   Driver to collate and align early Cyrillic manuscripts
#            See full documentation at ***ADD URL***
# Requires:  suffix_tree.py, soundex.py
# License:   Original material is CC BY-NC-SA 
#            http://creativecommons.org/licenses/by-nc-sa/3.0/deed.en_US
# ==============================================================================

from soundex import *
from suffix_tree import *

input = 'aaaabbbbccccaaaabbbb$$$$'
key_length = 4
trie = build_st(input,key_length)
traverse_st(trie,key_length)
find(trie,'aaaa',key_length = 4)
find(trie,'bbbb',key_length = 4)