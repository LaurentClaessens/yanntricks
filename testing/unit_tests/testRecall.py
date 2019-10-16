# -*- coding: utf8 -*-

###########################################################################
#   This is part of the module yanntricks
#
#   yanntricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   yanntricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with yanntricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2017
# email: laurent@claessens-donadello.eu

from __future__ import division

from yanntricks import *

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test
from Testing import SilentOutput


import os
import sys
import importlib

cwd=os.getcwd()
testrecall_dirname=os.path.join(cwd,"../recall_tests/")

sys.path.append(testrecall_dirname)
TestRecall = importlib.import_module("TestRecall")

from TestRecall import comparison
from TestRecall import check_pictures

def test_math():
    echo_function("test_math")
    text="#\setlength{\lengthOf}{\total{$f(x)$}}% (1,1)"

    fd=TestRecall.TikzDecomposition(text)
    fdp=[str(p) for p in fd.points_list]

    ans_texts=['#\\setlength{\\lengthOf}{\total{$f', 'x)$}}% ',')']
    ans_points=["(1.0,1.0)"]

    assert_equal(fdp,ans_points)
    assert_equal(fd.texts_list,ans_texts)

def test_OMZO():
    echo_function("test_OMZO")

    f="Fig_OMZOoowEtRUuMi.pstricks"
    g="Fig_OMZOoowEtRUuMi.pstricks.recall"

    comparison(f,g,0.001)


def test_zero():
    echo_function("test_zero")
    text="\draw [e=d] plot [s,t=1] coordinates {(1.00,0)(1.05,0.0320))};"

    fd=TestRecall.TikzDecomposition(text)
    fdp=[str(p) for p in fd.points_list]

    ans_points=["(1.0,0.0)","(1.05,0.032)"]
    assert_equal(fdp,ans_points)

def test_split():
    echo_function("test_split")
    text="aaaZbbZcc"
    
    echo_single_test("only internal")
    it = TestRecall.split_for_positions(text,[3,6])
    lit=list(it)
    ans=['aaa','bb','cc']
    assert_equal(lit,ans)

    echo_single_test("left border")
    text="stuZbbZcc"
    it = TestRecall.split_for_positions(text,[0,3,6])
    lit=list(it)
    ans=['','stu','bb','cc']
    assert_equal(lit,ans)

    echo_single_test("right border")
    text="stuZbbZccZ"
    it = TestRecall.split_for_positions(text,[0,3,6,9])
    lit=list(it)
    ans=['','stu','bb','cc','']
    assert_equal(lit,ans)

def test_text_parenthesis():
    echo_function("test_text_parenthesis")
    text="\subfigure[more points (5000)]{%"

    fd=TestRecall.TikzDecomposition(text)
    assert_true(fd.points_list==[])
    assert_true(len(fd.texts_list)==2)
    assert_equal(fd.texts_list[0],"\subfigure[more points ")
    assert_equal(fd.texts_list[1],"5000)]{%")

def testRecall():
    test_split()
    test_zero()
    test_math()
    test_OMZO()
    test_text_parenthesis()
