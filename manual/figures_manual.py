#! /usr/bin/sage -python
# -*- coding: utf8 -*-

import sys
from phystricks import *

from phystricksOnePoint import OnePoint
from phystricksRJDEoobOibtkfv import RJDEoobOibtkfv
from phystricksLARGooSLxQTdPC import LARGooSLxQTdPC
from phystricksPBFCooVlPiRBpt import PBFCooVlPiRBpt
from phystricksGKMEooBcNxcWBt import GKMEooBcNxcWBt
from FunctionThird import FunctionThird
from phystricksVSJOooJXAwbVEt import VSJOooJXAwbVEt

figures_list=[]
figures_list.append(RJDEoobOibtkfv)
figures_list.append(OnePoint)
figures_list.append(FunctionThird)
figures_list.append(GKMEooBcNxcWBt)
figures_list.append(LARGooSLxQTdPC)
figures_list.append(PBFCooVlPiRBpt)
figures_list.append(VSJOooJXAwbVEt)
"""
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
"""

def AllFigures():
    tests=FigureGenerationSuite(figures_list,first=0,title=u"phystricks's manual")
    tests.generate()
    tests.summary()

if __name__=="__main__":
    AllFigures()
