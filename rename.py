#!/usr/bin/env python3

import sys
import os
import os.path
import argparse
import re

def set_case(to_upper, filenames):
    for i in range(len(filenames)):
        if to_upper:
            filenames[i] = filenames[i].upper()
        else:
            filenames[i] = filenames[i].lower()

def replace(filenames, oldstring, newstring):
    for i in range(len(filenames)):
        filenames[i] = re.sub(oldstring, newstring, filenames[i])

def main():
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true',
                        help='verbose output, print old and new filenames during processing')
    parser.add_argument('-i', action='store_true',
                        help='interactive mode, ask user prior to renaming each file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', action='store_true', help='convert filenames to lowercase')
    group.add_argument('-u', action='store_true', help='convert filenames to uppercase')
    parser.add_argument('-t', metavar='n', type=int,
                        help='trim n chars from the start of each filename if n is positive, trim n chars from the end of each filename if n is negative')
    parser.add_argument('-r', nargs=2, metavar=('\"oldstring\"', '\"newstring\"'), type=str,
                        help='replace oldstring with newstring in filenames')
    parser.add_argument('-n', metavar='\"countstring\"', type=int,
                        help='rename files in sequence using countstring')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files to operate on')
    args = parser.parse_args()

    # make sure all files given exist
    for f in args.files:
        if not os.path.exists(f):
            print('file', f, 'does not exist')
            exit()

    modified_filenames = args.files[:]

    if args.r:
        replace(modified_filenames, args.r[0], args.r[1])

    if args.u or args.l:
        set_case(args.u, modified_filenames)

    if args.v:
        for i in range(len(args.files)):
            print('renaming', args.files[i], 'to', modified_filenames[i])

if __name__ == '__main__':
    main()
