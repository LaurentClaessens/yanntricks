#!/bin/bash
# -*- coding: utf8 -*-

# This script launches the tests.


# We append this version of 'phystricks' to $SAGE_PATH because 
# we want to test what is here.

BASEDIR=$(pwd)
SAGE_PATH=$PYTHONPATH:$BASEDIR/../..

demonstration_testing ()
{
    cd $BASEDIR/demonstration
    SAGE_PATH=$SAGE_PATH ./testing.sh
}

unit_testing ()
{
    cd $BASEDIR/unit_tests
    SAGE_PATH=$SAGE_PATH ./testing.sh
}

unit_testing &&
demonstration_testing
