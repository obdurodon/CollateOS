#!/usr/bin/env python
# -*-coding: utf8-*-
# ==============================================================================
# Derived from http://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixtrees.pdf
# Filename:  suffix_tree.py
# Developer: David J. Birnbaum (djbpitt@gmail.com; http://www.obdurodon.org)
# Date:      Created 2013-06-21; last modified 2013-06-28
# Summary:   Module to build and traverse suffix tries
#            See full documentation at ***ADD URL***
# License:   Original material is CC BY-NC-SA 
#            http://creativecommons.org/licenses/by-nc-sa/3.0/deed.en_US
# ==============================================================================

class Node(object):
    """Node in a suffix tree.
    
    Attributes (2):
      1) .children: dictionary with links from string keys to Node object values
      2) .suffix_link: pointer to another Node object
      
    Method (1):
      1) .add_link add a suffix link that points to the next longest suffix
         (e.g., the same suffix, starting one unit closer to the end)
    """
    def __init__(self, suffix_link = None):
        self.children = {}
        if suffix_link is None:
            self.suffix_link = self
        else:
            self.suffix_link = suffix_link
    def add_link(self, c, v):
        """Add a suffix link to a Node.
        
        Parameters:
            c == key (Unicode string)
            v == value (pointer to a Node)
        """
        self.children[c] = v

def build_st(s,key_length = 1):
    """Create a suffix trie from a single string and return it
    
    Parameter:
        s: input (Unicode) string
    """
    # the input string must be non-zero and evenly divisble by the key length
    assert len(s) > 0, "The input string cannot be zero-length"
    assert len(s) % key_length == 0, "The length of the input string must be evenly divisible by the key length"
    # create Root plus first child outside the loop, so that Root can be used to flag the
    #   the end of the loop
    # Longest will be the starting point to end the next node (see below)
    Root = Node()
    Longest = Node(suffix_link = Root)
    Root.add_link(s[0:key_length], Longest)
    # if only one word, return minimal tree
    if len(s) > key_length:
        # word are four characters long, so tokenize the string into words and
        #   use each one to add any necessary nodes
        #   first was already created separately before the loop
        for pointer in range(key_length,len(s),key_length):
            word = s[pointer:pointer+key_length]
            # start from the longest branch by setting Longest to Current
            # reset Current to walk up the links to Root
            # Longest initially has no previous, so no suffix_link points to it
            Current = Longest; Previous = None;
            # either a word exists at the current location or it doesn't
            # If a word doesn't exist:
            # add it to the end of the branch
            # the end of the longest branch (there is always exactly one) is
            #   held in the variable Current when the >for loop begins
            # the suffix_link in each endpoint points to the next longest, so
            #   walk up them and add the word to each branch, including the root
            while word not in Current.children:
                new = Node()
                Current.add_link(word,new)
                if Previous is not None:
                    Previous.suffix_link = new
                Previous = new # this is about to be where we'll come from
                Current = Current.suffix_link # reset current to the next longest
            #when the word doesn't exist, we're at the last context
            #if the condition is true, this is the link we just added, so link 
            #  from it up to the root 
            #
            #========================================================#
            # IS THIS CORRECT? WHAT IF WE DIDN'T ADD UNDER THE ROOT? #
            #========================================================#
            #
            #  otherwise it's an existing non-root node, already linked upward,
            #    and we link to it
            if Current.children[word] is Previous:
                Previous.suffix_link = Root
            else:
                Previous.suffix_link = Current.children[word]
            Longest = Longest.children[word]
    return Root

def traverse_st(trie, key_length = 1, depth = 0):
    """Output all suffixes, with indentation to show branching"""
    # based on http://www.siafoo.net/snippet/91
    if len(trie.children) == 0:
        print depth, " (no more)\n"
    else:
        for item in trie.children:
            print depth, ' ' * key_length * depth, item
            traverse_st(trie.children[item], key_length, depth + 1)

def find(trie, input = 'qqqq', key_length = 1):
    """Find the input (Unicode) string in the trie"""
    if len(input) == 0:
        print "found"
    else:
        bite = input[0:key_length]
        print "bite = ",bite
        if bite in trie.children:
            # can we avoid creating new strings and use pointers instead?
            # apparently not; buffer() and memoryview() don't support Unicode
            # http://docs.python.org/2/library/stdtypes.html (class memoryview(obj))
            # might change in v. 3; check back then
            find(trie.children[bite],input=input[key_length:],key_length = key_length)
        else:
            print "not found"

def post_order(trie, depth = 0):
    """Print all suffixes, using post-order traversal"""
    for child in trie.children:
        print "child = ",child," (",depth,")"
        try:
            print "trie.children[child] = ", trie.children[child]
            post_order(trie.children[child], depth + 1)
        except:
            print child," (",depth,")"

# To do:
#
# Fix post_order() to generate all suffixes (for testing)
#
# Unique terminators may not be needed if we keep track of input sources
#   within the nodes themselves
#   1) Annotate nodes when added or visited according to input source
#   2) Include offset(s) into input source
#   3) Use this information to find MEMs and MUM without having to walk
#      the whole tree
# Parse XML input
# Accept multiple input strings for generalized suffix trie
# Create soundex representations from raw Cyrillic text (function)
# Perhaps tokenize input string into list, instead of treating as string
#   more natural with XML input, where soundex will be applied to 
#   individual words, so early tokenization is required anyway (function)
# Return XML-encoded output with alignment markup added
#   Use offset into original string to retrieve output, 
#   since trie contains only soundex representations
# Separate module:
#   DONE: Suffix tree attributes and methods, generalized extends simple
#   Soundex conversion
#   Driver to parse XML, soundex convert, align and collate, write output
# Write full documentation for use


