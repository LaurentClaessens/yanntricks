#!/bin/bash
# -*- coding: utf8 -*-

compile_demo ()
{
SAGE_PATH=$SAGE_PATH  ./figures_demo.py --all
#pytex lst_demo.py --no-external --all
}


# Remove the garbage files
rm *.dpth
rm *.log
rm *.md5
rm *.pdf
rm *.pstricks
rm *.comment
rm *.aux
rm *.pyc

# Compile three times the demo pictures 
# (yes, some pictures need three passes)

compile_demo
compile_demo
compile_demo

# Then compare with the "recall" ones
./test_recall.py

