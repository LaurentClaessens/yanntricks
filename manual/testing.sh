#!/bin/bash
# -*- coding: utf8 -*-

# You should not launch directly this script, but let
# phystricks/testing/testing.sh
# launch for you.
# The reason is a manipulation of $SAGE_PATH : you want the tests to be launched
# with the version of phystricks which is present in *this* directory; not the
# one which is already in your system's $SAGE_PATH.

compile_manual ()
{
SAGE_PATH=$SAGE_PATH  ./figures_manual.py --all --pass-number=$1 &&
pytex lst_manual.py --no-external --all
}


# Remove the garbage files
rm *.dpth >> /dev/null
rm *.log >> /dev/null
rm *.md5 >> /dev/null
rm *.pdf >> /dev/null
rm *.pstricks >> /dev/null
rm *.comment >> /dev/null
rm *.aux >> /dev/null
rm *.pyc >> /dev/null

# Compile three times the demo pictures 
# (yes, some pictures need three passes)

compile_manual 1 &&
compile_manual 2 &&
compile_manual 3 

# Then compare with the "recall" ones
./test_recall.py
