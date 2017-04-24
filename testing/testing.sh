#!/bin/bash
# -*- coding: utf8 -*-

# This script launches the tests.

compile_demo ()
{
./figures_demo.py --all
pytex lst_demo.py --no-external --all
}


################" DEMONSTRATION FILE ############

cd demonstration

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

############### UNIT TESTING ###############

cd ..

cd unit_tests
./unit_tests.sh

