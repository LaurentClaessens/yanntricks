#! /usr/bin/python3
# -*- coding: utf8 -*-


# This script compares the files "*.pstricks" with the corresponding one 
# "*.pstricks.recall" and prints a warning if they are not equal.

# - arguments : the name of the directory to be tested
#              Assumed to be absolute path, but could also work with
#               relative path.

import os
import sys

from TestRecall import check_pictures
from TestRecall import comparison

pstricks_directory=sys.argv[1]
recall_directory=sys.argv[1]
try:
    recall_directory=sys.argv[2]
except IndexError:
    pass

check_pictures(pstricks_directory,recall_directory)
