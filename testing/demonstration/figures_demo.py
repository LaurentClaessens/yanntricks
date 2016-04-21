#! /usr/bin/sage -python
# -*- coding: utf8 -*-

"""
This is the skeleton of figures_all.py that will be automatically generated by 'create_all.py'
"""

import sys
from phystricks import *


from phystricksCUZFooGqZLaAEp import CUZFooGqZLaAEp
from phystricksPJKBooOhGVPkeR import PJKBooOhGVPkeR
from phystricksLVPSoozFTyaeCG import LVPSoozFTyaeCG
from AxesSecond import AxesSecond
from phystricksYOWDooyeyOJyml import YOWDooyeyOJyml
from exCircle import exCircle
from exCircleThree import exCircleThree
from exCircleTwo import exCircleTwo
from phystricksOnePoint import OnePoint
from FunctionFirst import FunctionFirst
from FunctionFive import FunctionFive
from FunctionFour import FunctionFour
from FunctionSecond import FunctionSecond
from GestionRepere import GestionRepere
from GridOne import GridOne
from GridThree import GridThree
from GridTwo import GridTwo
from Lines import Lines
from MarkOnPoint import MarkOnPoint
from ParametricOne import ParametricOne
from ParametricTwo import ParametricTwo
from VectorOne import VectorOne
from phystricksTRJEooPRoLnEiG import TRJEooPRoLnEiG
from phystricksQRXCooUmnlhkvh import QRXCooUmnlhkvh
from phystricksUREIooqNGBXtHg import UREIooqNGBXtHg
from phystricksQIXEooejrojKjo import QIXEooejrojKjo
from phystricksDEIToomZFknFmn import DEIToomZFknFmn
from phystricksQNHAooSYgkWVhJ import QNHAooSYgkWVhJ
from phystricksUARHooLMWqvyaI import UARHooLMWqvyaI
from phystricksHELQooLGapRQrr import HELQooLGapRQrr
from phystricksYJEDoojDtSeKHQ import YJEDoojDtSeKHQ
from phystricksQRJOooKZPUoLlF import QRJOooKZPUoLlF
from phystricksRVKFooDxrqYXAX import RVKFooDxrqYXAX
from phystricksPFCUoorQhitKoJ import PFCUoorQhitKoJ
from phystricksEXIIooJzzoJeai import EXIIooJzzoJeai

figures_list=[]
figures_list.append(YOWDooyeyOJyml)
figures_list.append(PFCUoorQhitKoJ)
figures_list.append(QIXEooejrojKjo)
figures_list.append(AxesSecond)
figures_list.append(exCircle)
figures_list.append(exCircleThree)
figures_list.append(exCircleTwo)
figures_list.append(OnePoint)
figures_list.append(FunctionFirst)
figures_list.append(FunctionFive)
figures_list.append(FunctionFour)
figures_list.append(FunctionSecond)
figures_list.append(GestionRepere)
figures_list.append(GridOne)
figures_list.append(GridThree)
figures_list.append(GridTwo)
figures_list.append(Lines)
figures_list.append(MarkOnPoint)
figures_list.append(ParametricOne)
figures_list.append(ParametricTwo)
figures_list.append(VectorOne)
figures_list.append(TRJEooPRoLnEiG)
figures_list.append(QRXCooUmnlhkvh)
figures_list.append(UREIooqNGBXtHg)
figures_list.append(DEIToomZFknFmn)
figures_list.append(QNHAooSYgkWVhJ)
figures_list.append(UARHooLMWqvyaI)
figures_list.append(HELQooLGapRQrr)
figures_list.append(YJEDoojDtSeKHQ)
figures_list.append(QRJOooKZPUoLlF)
figures_list.append(RVKFooDxrqYXAX)
figures_list.append(EXIIooJzzoJeai)
figures_list.append(PJKBooOhGVPkeR)
figures_list.append(LVPSoozFTyaeCG)
figures_list.append(CUZFooGqZLaAEp)
"""
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
figures_list.append(<++>)
"""

def AllFigures():
    tests=main.FigureGenerationSuite(figures_list,first=0,title=u"demonstration pictures")
    tests.generate()
    tests.summary()

if __name__=="__main__":
    if "--all" in sys.argv :
        AllFigures()
    else:
        ProjPoly()
