#!/usr/bin/env python3

'''=============================================================================
 Program: File Rename Utility in Python
 Authors: Matthew Richard, Matthew De Young
 Class:   CSC 461 Programming Languages
 Instructor: Dr. Weiss
 Date: 02-10-2015
 Description: Command line arguments are accepted from the user including
              triggers for operations to be performed upon filenames as well as
              filenames to be operated upon. Each argument checked for validity,
              and the specified operations are performed upon the provided
              filenames.
 Input: Command line arguments and filenames to be operated upon
 Output: None ?
 Compilation instructions: Compile using Python 3.4
 Usage: ?
 Modifications: None
 Date        Comment
 ----        ------------------------------------------------
 01-30-2015  Programming Partners Assigned
 02-01-2015  Began working on Python files
 02-05-2015  Functions set_case, replace, count_string, interactive, and
             trimming completed

 02-XX-2015  Program Submitted
============================================================================='''

'''===========================Imported Modules==============================='''
import sys
import os
import os.path
import argparse
import glob
import re
'''=========================================================================='''

'''=============================================================================
 Function:
 Description:
 Parameters:
============================================================================='''
def count_string(modified_filenames, count_str, args):
    groups = re.findall( "#+", count_str )
    for i in range(len(modified_filenames)):
        new_filename = count_str
        for j in groups:
            numbers = len(j) # number of pound signs in string
            new_filename = new_filename.replace(j,
                ("%0"+str(numbers)+"d") %i, 1 )
        if args.v:
            print("Changing " + count_str + " to " + new_filename + "\n")
        modified_filenames[i] = new_filename

'''=============================================================================
 Function:
 Description:
 Parameters:
============================================================================='''
def interactive(modified_filenames, original_filenames):
    for item in range(len(modified_filenames)):
        direct = input("Do you want to rename " + original_filenames[item] +
                       " to " + modified_filenames[item] + "?\nYes or No: ")
        while not direct == "Yes" and not direct == "No":
            direct = input("Please enter a valid option of Yes or No\n").lower()
        if direct == "no":
            modified_filenames[item] = original_filenames[item]

'''=============================================================================
 Function:
 Description:
 Parameters:
============================================================================='''
def replace(filenames, oldstring, newstring, args):
    for i in range(len(filenames)):
        if args.v:
            print("Replacing " + oldstring + " with " + newstring + "\n")
        filenames[i] = re.sub(oldstring, newstring, filenames[i])

'''=============================================================================
 Function:
 Description:
 Parameters:
============================================================================='''
def set_case(to_upper, filenames, args):
    for i in range(len(filenames)):
        if to_upper:
            if args.v:
                print("Changing " + filenames[i] + " to " +
                      filenames[i].upper() + "\n")
            filenames[i] = filenames[i].upper()
        else:
            if args.v:
                print("Changing " + filenames[i] + " to " +
                      filenames[i].lower() + "\n")
            filenames[i] = filenames[i].lower()

'''=============================================================================
 Function:
 Description:
 Parameters:
============================================================================='''
def trimming(n, modified_filenames, args):
    if n > 0:
        for i in range(len(modified_filenames)):
            if args.v:
                print("Trimming " + modified_filenames[i] + " to " +
                      modified_filenames[i][n:])
            modified_filenames[i] = modified_filenames[i][n:]
    else:
        for i in range(len(modified_filenames)):
            if args.v:
                print("Trimming " + modified_filenames[i] + " to " +
                      modified_filenames[i][:n])
            modified_filenames[i] = modified_filenames[i][:n]

'''=============================================================================
 Function:
 Description:
 Parameters:
============================================================================='''
def main():
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true',
                        help='verbose output, print old and new filenames \
                        during processing')
    parser.add_argument('-i', action='store_true',
                        help='interactive mode, ask user prior to renaming \
                        each file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', action='store_true', help='convert filenames \
                        to lowercase')
    group.add_argument('-u', action='store_true', help='convert filenames \
                        to uppercase')
    parser.add_argument('-t', metavar='n', type=int,
                        help='trim n chars from the start of each filename \
                        if n is positive, trim n chars from the end of each \
                        filename if n is negative')
    parser.add_argument('-r', nargs=2, metavar=('\"oldstring\"',
                                                '\"newstring\"'), type=str,
                        help='replace oldstring with newstring in filenames')
    parser.add_argument('-n', metavar='\"countstring\"', type=str,
                        help='rename files in sequence using countstring')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files to operate on')
    args = parser.parse_args()

    i = 0
    while i < len(args.files):
        files = glob.glob(args.files[i])
        args.files[i:i+1] = files
        i += len(files)

    # make sure all files given exist
    for f in args.files:
        if not os.path.exists(f):
            print('file', f, 'does not exist')
            exit()

    modified_filenames = args.files[:]
    
    # process arguments in the order they are specified
    for i in sys.argv:
        if i == "-r":
            replace(modified_filenames, args.r[0], args.r[1], args)
        elif i == "-u" or i == "-l":
            set_case(args.u, modified_filenames, args)
        elif i == "-t":
            trimming(args.t, modified_filenames, args)
        elif i == "-n":
            count_string(modified_filenames, args.n, args)
        #else:
            #print("Invalid argument provided, " + i + " is not viable.\n")
            #call help function, quit also?

    if args.i:
        interactive(modified_filenames, args.files)

    for i in range(len(args.files)):
        os.rename(args.files[i], modified_filenames[i])

if __name__ == '__main__':
    main()
