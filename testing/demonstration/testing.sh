#!/bin/bash
# -*- coding: utf8 -*-

compile_demo ()
{
SAGE_PATH=$SAGE_PATH  ./figures_demo.py --all
#pytex lst_demo.py --no-external --all
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

compile_demo
#compile_demo
#compile_demo

# Then compare with the "recall" ones
./test_recall.py

