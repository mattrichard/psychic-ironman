#!/usr/bin/env python3

import sys
import os
import os.path
import argparse
import re

def count_string(modified_filenames, count_str ):
    groups = re.findall( "#+", count_str )
    for i in range(len(modified_filenames)):
        new_filename = count_str
        for j in groups:
            numbers = len(j) # number of pound signs in string
            new_filename = new_filename.replace ( j, ("%0"+str(numbers)+"d") %i, 1 )
        modified_filenames[i] = new_filename

def interactive(modified_filenames):
    for item in range(len(args.files)):
        direct = input("Do you want to rename " + args.files[item] +\
                       " to " + modified_filenames[item] + "?  \
                       Yes or No")
        while not direct == "Yes" and not direct == "No":
            direct = input("Please enter a valid option of Yes or No\n")
        if direct == "No":
            modified_filenames[item] = args.files[item]
                
def set_case(to_upper, filenames):
    for i in range(len(filenames)):
        if to_upper:
            filenames[i] = filenames[i].upper()
        else:
            filenames[i] = filenames[i].lower()

def trimming( n, modified_filenames ):
    if n > 0:
        for i in range(len(modified_filenames)):
            modified_filenames[i] = modified_filenames[i][n:]
    else:
        for i in range(len(modified_filenames)):
            modified_filenames[i] = modified_filenames[i][:-n]

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
    parser.add_argument('-n', metavar='\"countstring\"', type=str,
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

    #New stuff

    if args.i:
        interactive( modified_filenames )

    if not args.t == None:
        trimming( args.t, modified_filenames )

    if not args.n == None:
        count_string(modified_filenames, args.n)

    if args.v:
        for i in range(len(args.files)):
            print('renaming', args.files[i], 'to', modified_filenames[i])

    #end new stuff
if __name__ == '__main__':
    main()
