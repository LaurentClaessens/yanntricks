#!/bin/bash

MAIN_DIR=$PWD
VENV_DIR=$MAIN_DIR/venv
BIN_DIR=$VENV_DIR/bin
PYTHON=$BIN_DIR/python3

python_lint()
{
    cd $BIN_DIR
    ./pylint $FILEPATH
}


lint_one_file()
{
    FILENAME=$1
    FILEPATH=$MAIN_DIR/$FILENAME
    echo $FILEPATH
    if [[ "$FILEPATH" == *\.py ]]; then
        python_lint $FILEPATH
    fi
}


if [ $# -eq 0 ]; then
    for f in $(git ls-tree -r HEAD --name-only); do lint_one_file $f;done
else
    lint_one_file $1
fi

