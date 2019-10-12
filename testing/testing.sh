#!/bin/bash

# This script launches the tests.


# We append this version of 'phystricks' to $SAGE_PATH because 
# we want to test what is here.

BASE_DIR=$(pwd)
SAGE_PATH=$BASE_DIR/../..:$PYTHONPATH
RECALLTEST_DIR=$BASE_DIR/recall_tests/
DEMO_DIR=$BASE_DIR/demonstration
MANUAL_DIR=$BASE_DIR/../manual/
UNIT_TESTS_DIR=$BASE_DIR/unit_tests

LOGFILE=$BASE_DIR/testing.log
rm $LOGFILE
touch $LOGFILE

demonstration_testing ()
{
    cd $DEMO_DIR
    SAGE_PATH=$SAGE_PATH ./testing.sh&&
    cd $RECALLTEST_DIR
    ./test_recall.py $DEMO_DIR  >> $LOGFILE
}

manual_testing ()
{
    cd $MANUAL_DIR
    SAGE_PATH=$SAGE_PATH ./testing.sh&&
    cd $RECALLTEST_DIR
    ./test_recall.py $MANUAL_DIR >> $LOGFILE
}

unit_testing ()
{
    cd $UNIT_TESTS_DIR
    SAGE_PATH=$SAGE_PATH ./testing.sh
}

unit_testing &&
manual_testing&&
demonstration_testing

echo "---- Results : "
cat $LOGFILE
echo "---------- "
