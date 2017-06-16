#! /usr/bin/python3
# -*- coding: utf8 -*-


# This script compares the files "*.pstricks" with the corresponding one 
# "*.pstricks.recall" and prints a warning if they are not equal.

# - arguments : the name of the directory to be tested
#              Assumed to be absolute path, but could also work with
#               relative path.

import os
import sys

from TestRecall import wrong_file_list
from TestRecall import FileDecomposition
from TestRecall import comparison

pstricks_directory=sys.argv[1]
recall_directory=sys.argv[1]
try:
    recall_directory=sys.argv[2]
except IndexError:
    pass

mfl,wfl=wrong_file_list(pstricks_directory,recall_directory)

for f in mfl:
    print("Missing recall file for ",f)
for f in wfl:
    print("Wrong : ")
    g=f.replace(pstricks_directory,recall_directory)+".recall"
    print(f)
    print(g)
    p_dec=FileDecomposition(f)
    r_dec=FileDecomposition(g)
    comparison(p_dec,r_dec,epsilon=0.001)
