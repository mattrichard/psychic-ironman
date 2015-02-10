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
 Input:  Command line arguments and filenames to be operated upon
 Output: Changes file names based on parameters specified
 Usage:  Renaming files based on specified arguments of:
         -h -v -i -l -u -t n -r "oldstring" "newstring" -n "countstring"
         files[]
 Date        Comment
 ----        ------------------------------------------------
 01-30-2015  Programming Partners Assigned
 02-01-2015  Began working on Python files
 02-05-2015  Functions set_case, replace, count_string, interactive, and
             trimming completed
 02-10-2015  Program Submitted
============================================================================='''

'''===========================Imported Modules==============================='''
import sys
import os
import os.path
import argparse
import glob
import re
'''=========================================================================='''

def count_string(modified_filenames, count_str, verbose):
    '''Replaces the specified string of # symbols with incrementing values.

    Description:
      Replaces the # symbols in the original file name with incrementing values.
      Count_str is the specified file name to be altered and modified_filenames
      is a list of filenames with alterations made. Verbose is an indicator
      for if verbose output is specified, used to detail the operations being
      performed to the user.

    Arguments:
      modified_filenames: list of altered filenames
      count_str: filename to be operated upon
      verbose: value signaling if verbose output is specified

    Return Values:
      None
    '''
    groups = re.findall( "#+", count_str )
    for i in range(len(modified_filenames)):
        new_filename = count_str
        for j in groups:
            numbers = len(j) # number of pound signs in string
            new_filename = new_filename.replace(j,
                ("%0"+str(numbers)+"d") %i, 1 )
        if verbose:
            print("Changing " + count_str + " to " + new_filename + "\n")
        modified_filenames[i] = new_filename


def rename_files(modified_filenames, original_filenames, interactive):
    '''Renames all files and requests user confirmation of actions if in interactive mode.

    Description:
      Interactive mode will request the user to confirm or deny all changes
      to the specified list of file names. Modified_filenames contains the
      list of file names that have been altered, and original_filenames
      consists of the unaltered filenames.

    Arguments:
      modified_filenames: list of altered filenames
      original_filenames: list of original filenames

    Return Values:
      None
    '''
    for item in range(len(modified_filenames)):
        if interactive:
            direct = input("Do you want to rename " + original_filenames[item] +
                           " to " + modified_filenames[item] + "?\nYes or No: ").lower()
            while not direct == "yes" and not direct == "no":
                direct = input("Please enter a valid option of Yes or No\n").lower()
            if direct == "yes":
                os.rename(original_filenames[item], modified_filenames[item])
        else:
            os.rename(original_filenames[item], modified_filenames[item])
                

def replace(filenames, oldstring, newstring, verbose):
    '''Replaces filenames with specified altered versions.

    Description:
      Replace will commit all of the changes 

    Arguments:
      filenames: list of filenames
      oldstring: original filename
      newstring: new filename
      verbose: trigger for if verbose output is to be provided to the user

    Return Values:
      None
    '''
    for i in range(len(filenames)):
        if verbose:
            print("Replacing " + oldstring + " with " + newstring + "\n")
        filenames[i] = re.sub(oldstring, newstring, filenames[i])

def set_case(to_upper, filenames, verbose):
    '''Changes the case of the filename.

    Description:
      Set_case will alter the filename specified to all upper or lower
      case. to_upper acts as a trigger for if the case is to be made
      all upper or all lower, filenames is a list containing all
      current filenames, and verbose acts as a trigger for if verbose
      output is to be detailed to the user.

    Arguments:
      to_upper:  signals if the case is to be upper or lower
      filenames: a list of all current filenames
      verbose:   signals if verbose output is to occur

    Return Values:
      None
    '''
    for i in range(len(filenames)):
        if to_upper:
            if verbose:
                print("Changing " + filenames[i] + " to " +
                      filenames[i].upper() + "\n")
            filenames[i] = filenames[i].upper()
        else:
            if verbose:
                print("Changing " + filenames[i] + " to " +
                      filenames[i].lower() + "\n")
            filenames[i] = filenames[i].lower()

def trimming(n, modified_filenames, verbose):
    '''Trims characters from file names.

    Description:
      Trimming will trim a set number of characters from the start
      or end of each filename. The number of characters is specified
      by n, with modified_filenames storing the alterations and
      verbose triggering descriptive output to the user. If n is
      positive the characters are trimmed from the start of the file
      names, if n is negative the characters are trimmed from the end
      of the file names.

    Arguments:
      n: the number of characters to be trimmed
      modified_filenames: list of altered filenames
      verbose: value signaling if verbose output is specified

    Return Values:
      None
    '''
    if n > 0:
        for i in range(len(modified_filenames)):
            if verbose:
                print("Trimming " + modified_filenames[i] + " to " +
                      modified_filenames[i][n:])
            modified_filenames[i] = modified_filenames[i][n:]
    else:
        for i in range(len(modified_filenames)):
            if verbose:
                print("Trimming " + modified_filenames[i] + " to " +
                      modified_filenames[i][:n])
            modified_filenames[i] = modified_filenames[i][:n]

def main():
    '''Replaces the specified string of # symbols with incrementing values.

    Description:
      Processes the command line arguments and utilizes all options specified.

    Arguments:
      None
    Return Values:
      None
    '''
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
    # expand any wild cards in filenames
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
            replace(modified_filenames, args.r[0], args.r[1], args.v)
        elif i == "-u" or i == "-l":
            set_case(args.u, modified_filenames, args.v)
        elif i == "-t":
            trimming(args.t, modified_filenames, args.v)
        elif i == "-n":
            count_string(modified_filenames, args.n, args.v)

    rename_files(modified_filenames, args.files, args.i)

if __name__ == '__main__':
    main()
