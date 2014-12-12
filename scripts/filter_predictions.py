#!/usr/bin/env python

import os

from select_predicates import predicates_to_annotate

def main():
    for file in os.listdir('data'):
        if not file.endswith('csv'): continue
        print file
        outfile = 'data/filtered/' + file
        out = open(outfile, 'w')
        for line in open('data/' + file):
            fields = line.split('\t')
            if fields[0] in predicates_to_annotate:
                out.write(line)
        out.close()


if __name__ == '__main__':
    main()
