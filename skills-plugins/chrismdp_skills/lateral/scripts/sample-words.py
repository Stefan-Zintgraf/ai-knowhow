#!/usr/bin/env python3
"""Sample random words from the dictionary for /lateral skill."""

import argparse
import os
import random
import subprocess
import sys

DICT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "words.txt")
DICT_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"


def ensure_dict():
    if os.path.exists(DICT_PATH):
        return
    print(f"Downloading dictionary to {DICT_PATH}...", file=sys.stderr)
    subprocess.run(["curl", "-s", "-o", DICT_PATH, DICT_URL], check=True)


def sample(n=10, min_len=4, max_len=9):
    ensure_dict()
    words = [
        w.strip()
        for w in open(DICT_PATH)
        if w.strip().isalpha() and min_len <= len(w.strip()) <= max_len
    ]
    return random.sample(words, min(n, len(words)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, nargs="?", default=10, help="Number of words")
    parser.add_argument("--min-len", type=int, default=4)
    parser.add_argument("--max-len", type=int, default=9)
    args = parser.parse_args()

    for word in sample(args.n, args.min_len, args.max_len):
        print(word)
