#!/bin/bash
# -*- coding: utf8 -*-

# This script launches the tests.


# We append this version of 'phystricks' to $SAGE_PATH because 
# we want to test what is here.

BASEDIR=$(pwd)
SAGE_PATH=$PYTHONPATH:$BASEDIR/../..

LOGFILE=$BASEDIR/testing.log
rm $LOGFILE
touch $LOGFILE

demonstration_testing ()
{
    cd $BASEDIR/demonstration
    SAGE_PATH=$SAGE_PATH ./testing.sh&&
    cd $BASEDIR
    echo BASEDIR est : $BASEDIR
    ./test_recall.py $BASEDIR/demonstration >> $LOGFILE
}

manual_testing ()
{
    cd $BASEDIR/../manual
    SAGE_PATH=$SAGE_PATH ./testing.sh&&
    cd $BASEDIR
    ./test_recall.py $BASEDIR/../manual >> $LOGFILE
}

unit_testing ()
{
    cd $BASEDIR/unit_tests
    SAGE_PATH=$SAGE_PATH ./testing.sh
}


unit_testing &&
manual_testing&&
demonstration_testing

echo "---- Results : "
cat $LOGFILE
echo "---------- "
