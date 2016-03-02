#!/bin/bash
# -*- coding: utf8 -*-

sage minitest.py
sage -t unicode_litterals_test.py &&
sage -t ../BasicGeometricObjects.py &&
sage -t ../__init__.py &&
sage -t ../SmallComputations.py &&
sage -t for_unit_tests.py &&
sage -t unit_tests.py &&
sage -t unit_tests_long1.py
sage -t unit_tests_long1.py
sage -t lll.py
