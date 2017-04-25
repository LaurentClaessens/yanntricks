#!/bin/bash
# -*- coding: utf8 -*-

# This script launches the tests.


BASEDIR=$(pwd)
SAGE_PATH=$BASEDIR/../..

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

unit_testing
demonstration_testing
