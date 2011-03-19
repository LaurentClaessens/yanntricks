#!/bin/bash
# -*- coding: utf8 -*-

sage -t BasicGeometricObjects.py &&
sage -t __init__.py &&
sage -t SmallComputations.py &&
sage -t unit_tests.py &&
sage -t unit_tests_long1.py
