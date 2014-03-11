#!/usr/bin/env python

import random

# This is my own interpretation of what I read of the Dissociated Press
# algorithm. It may not match up with other implementations.

# Possible TODOs:
# (1) Make chunk size randomizable
# (2) Make a configurable starting chunk
# (3) Make the starting chunks a little more intelligent, e.g. starting right
# after a period so that it does not begin mid-sentence.
# (4) Be lenient about capitalization and throw out punctuation.
# (5) More efficient memory usage or out-of-core processing for those cases
# when your text really can't all be fit in memory at once
# (6) Letter-based version rather than word-based

def dissociated_press_from_file(fnames, chunk_size, chunks):
    """Run the Dissociated Press algorithm on the text in the given files.
    All other behavior is identical to the dissociated_press() function."""
    text = ""
    for fname in fnames:
        f = open(fname)
        text += f.read()
        f.close()
    return dissociated_press(text, chunk_size, chunks)

def dissociated_press(text, chunk_size, chunks):
    """Run the Dissociated Press algorithm (word-based) on the given text.

    text -- The body of text on which to run the algorithm.
    chunk_size -- The number of words to operate on at once.
    chunks -- The number of chunk_size units to generate.

    Thus, the result will have around (chunk_size * chunks) words in it.
    Newlines will be removed.
    """
    text_clean = text.replace("\n", " ").replace("\r", "")
    # Separate into a list of words, and remove empty spaces.
    words = list(filter(None, text_clean.split(" ")))
    # Pick 'chunk_size' consecutive random words.
    start_index = random.randrange(0, len(words) - chunk_size + 1)
    end_index = start_index + chunk_size
    seed = words[start_index:end_index]
    strs = seed
    total_choices = 1
    for i in range(chunks):
        seed, match_count = dissociated_press_iterate(words, seed[-chunk_size:])
        total_choices *= match_count
        strs += seed
    # This can provide some insight into how "random" the generated text was:
    #print(total_choices)
    return " ".join(strs)

def dissociated_press_iterate(words, last_chunk, chunk_size = -1):
    # Assume last_chunk is the chunk size
    size = len(last_chunk)
    matches = list(find_in_list_consecutive(words, last_chunk))
    # Pick a random match.
    start = random.choice(matches)
    return words[start + size:start + size*2], len(matches)

def find_in_list_consecutive(l, pattern):
    """Find a pattern inside of a list. Yields indices to 'l' where
    'pattern' is found.

    l -- The list (or list-like object) inside of which to search
    pattern -- The list (or list-like object) to find inside of 'l'. It must
    appear in order, consecutively and in entirety.
    """
    # (Python probably already has a better, more Pythonic way to do this. I
    # don't know what it is though.)
    # This case is an automatic failure:
    if len(pattern) > len(l):
        return
    # Iterate over matches for the first element.
    for element in pattern:
        # s = start index. -1 is an initial value.
        s = -1
        try:
            while True:
                s = l.index(element, s + 1)
                # We have a potential match, so check all else:
                all_matched = True
                i = 0
                while all_matched and i < len(pattern):
                    # If we have pattern left to match, but have hit the list's
                    # end, this is not a match:
                    if (s + i) >= len(l):
                        all_matched = False
                        break
                    all_matched = all_matched and l[s + i] == pattern[i]
                    i += 1
                if all_matched:
                    yield s
        except ValueError:
            pass

def main(argv):
    if (len(argv) < 3):
        print("Dissociated Press implementation")
        print('("An algorithm for generating text based on another text.")')
        print("Usage: %s <chunk_size> <chunks> <input_file> [input_file2...]" % argv[0])
        print("Final text will be about chunk_size * chunks words long.")
        return -1
    fnames = argv[3:]
    chunk_size = int(argv[1])
    chunks = int(argv[2])
    print(dissociated_press_from_file(fnames, chunk_size, chunks))

import sys
main(sys.argv)
