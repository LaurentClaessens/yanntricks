#! /usr/bin/sage -python
# -*- coding: utf8 -*-

"""
This is the skeleton of figures_all.py that will be automatically generated by 'create_all.py'
"""

import sys
from phystricks import *

from phystricksOnePoint import OnePoint
from phystricksRJDEoobOibtkfv import RJDEoobOibtkfv
from phystricksLARGooSLxQTdPC import LARGooSLxQTdPC
from phystricksPBFCooVlPiRBpt import PBFCooVlPiRBpt
from phystricksGKMEooBcNxcWBt import GKMEooBcNxcWBt
from FunctionThird import FunctionThird

figures_list=[]
figures_list.append(OnePoint)
figures_list.append(FunctionThird)
figures_list.append(GKMEooBcNxcWBt)
figures_list.append(RJDEoobOibtkfv)
figures_list.append(LARGooSLxQTdPC)
figures_list.append(PBFCooVlPiRBpt)

def AllFigures():
    tests=main.FigureGenerationSuite(figures_list,first=0,title=u"phystricks's manual")
    tests.generate()
    tests.summary()

if __name__=="__main__":
    AllFigures()