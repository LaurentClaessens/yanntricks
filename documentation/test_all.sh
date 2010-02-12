#!/bin/bash
# This script recreates all the pictures of the documentation. This is the perfect way to perform automatic tests.

./examples.py --all
./first_example.py
./grading.py
