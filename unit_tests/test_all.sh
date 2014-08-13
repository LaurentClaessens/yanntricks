#!/bin/bash
# -*- coding: utf8 -*-

# Ceux-ci sont mes tests

sage -t unit_test_unicode_litterals.py &&
sage -t BasicGeometricObjects.py &&
sage -t __init__.py &&
sage -t SmallComputations.py &&
sage -t unit_tests.py &&
sage -t unit_tests_long1.py

echo ceci est la fin de ton script de tests.
