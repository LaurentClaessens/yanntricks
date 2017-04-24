#!/bin/bash
# -*- coding: utf8 -*-

# This script launches the tests.

compile_demo ()
{
./figures_demo.py --all
pytex lst_demo.py --no-external --all
}


cd unit_tests
./unit_tests.sh
cd ../demonstration

# Compile twice the demo pictures
compile_demo
compile_demo

# Then compare with the "recall" ones
./test_recall.py
