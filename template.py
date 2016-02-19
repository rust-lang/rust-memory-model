#!/usr/bin/python

"""
Use like this:

    pbpaste | python template.py > litmus_text/example.md

to produce a modified copy of the template.
"""

import sys

source_code_lines = sys.stdin.read().strip().split("\n")

for line in open("template.md"):
    line = line.strip()
    if line == "rust source code":
        for source_code_line in source_code_lines:
            print source_code_line
    else:
        print line
