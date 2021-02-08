#!/usr/bin/python

import sys

args = sys.argv[1:]

def printHelp():
    print('Here\'s a help menu\n'
          'with multiple lines in it')

if len(args) == 0:
    printHelp()
    exit()