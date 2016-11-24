#! /usr/bin/sage -python
# -*- coding: utf8 -*-

import sys
from phystricks import *

from phystricksNWAEooQBLYYrpS import NWAEooQBLYYrpS
from phystricksWQVZooAhkdlegv import WQVZooAhkdlegv
from phystricksMBWHooeesXIrsz import MBWHooeesXIrsz
from phystricksASZLoocnIGlRHf import ASZLoocnIGlRHf
from phystricksOYBTooNUcJLzDH import OYBTooNUcJLzDH
from phystricksOMPAooMbyOIqeA import OMPAooMbyOIqeA
from phystricksBHESoofmkTbbZR import BHESoofmkTbbZR
from phystricksCNVAooybLqXmVS import CNVAooybLqXmVS
from phystricksHUBEoofsPjXOQx import HUBEoofsPjXOQx
from phystricksGGHOookMhIxqIK import GGHOookMhIxqIK
from phystricksDYJNooLVVFHEfN import DYJNooLVVFHEfN
from phystricksFMLCooxHtqRzUz import FMLCooxHtqRzUz
from phystricksOGGDooIvakwNlL import OGGDooIvakwNlL
from phystricksQEFQoomlfmOQTM import QEFQoomlfmOQTM
from phystricksQHXKooHTpEuXMw import QHXKooHTpEuXMw
from phystricksOMZOoowEtRUuMi import OMZOoowEtRUuMi
from phystricksXBAUooFtMWukKr import XBAUooFtMWukKr
from phystricksMXKAoozETwoiTe import MXKAoozETwoiTe
from phystricksAESIooxXxRYQdT import AESIooxXxRYQdT
from phystricksLWVXooPyIlOKNd import LWVXooPyIlOKNd
from phystricksVLEGoolDFCdZDU import VLEGoolDFCdZDU
from phystricksCUZFooGqZLaAEp import CUZFooGqZLaAEp
from phystricksPJKBooOhGVPkeR import PJKBooOhGVPkeR
from phystricksLVPSoozFTyaeCG import LVPSoozFTyaeCG
from phystricksPVRFoobvAzpZTq import PVRFoobvAzpZTq
from AxesSecond import AxesSecond
from phystricksYOWDooyeyOJyml import YOWDooyeyOJyml
from exCircle import exCircle
from exCircleThree import exCircleThree
from exCircleTwo import exCircleTwo
from phystricksOnePoint import OnePoint
from FunctionFirst import FunctionFirst
from FunctionFive import FunctionFive
from phystricksFunctionFour import FunctionFour
from FunctionSecond import FunctionSecond
from GridThree import GridThree
from GridTwo import GridTwo
from MarkOnPoint import MarkOnPoint
from ParametricOne import ParametricOne
from ParametricTwo import ParametricTwo
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
from phystricksJSYWooQYduLVLS import JSYWooQYduLVLS
from phystricksQIPRoolQCEnZdx import QIPRoolQCEnZdx
from phystricksALAYooKKrRTkCG import ALAYooKKrRTkCG

figures_list=[]
figures_list.append(DYJNooLVVFHEfN)
figures_list.append(OGGDooIvakwNlL)
figures_list.append(PFCUoorQhitKoJ)
figures_list.append(QIXEooejrojKjo)
figures_list.append(AxesSecond)
figures_list.append(exCircle)
figures_list.append(exCircleThree)
figures_list.append(exCircleTwo)
figures_list.append(OnePoint)
figures_list.append(FunctionFirst)
figures_list.append(FunctionFive)
figures_list.append(FunctionSecond)
figures_list.append(QIPRoolQCEnZdx)
figures_list.append(FMLCooxHtqRzUz)
figures_list.append(GridThree)
figures_list.append(GridTwo)
figures_list.append(MarkOnPoint)
figures_list.append(ParametricOne)
figures_list.append(ParametricTwo)
figures_list.append(TRJEooPRoLnEiG)
figures_list.append(UREIooqNGBXtHg)
figures_list.append(DEIToomZFknFmn)
figures_list.append(UARHooLMWqvyaI)
figures_list.append(HELQooLGapRQrr)
figures_list.append(YJEDoojDtSeKHQ)
figures_list.append(QRJOooKZPUoLlF)
figures_list.append(RVKFooDxrqYXAX)
figures_list.append(EXIIooJzzoJeai)
figures_list.append(PJKBooOhGVPkeR)
figures_list.append(LVPSoozFTyaeCG)
figures_list.append(CUZFooGqZLaAEp)
figures_list.append(JSYWooQYduLVLS)
figures_list.append(YOWDooyeyOJyml)
figures_list.append(QRXCooUmnlhkvh)
figures_list.append(VLEGoolDFCdZDU)
figures_list.append(MXKAoozETwoiTe)
figures_list.append(XBAUooFtMWukKr)
figures_list.append(OMZOoowEtRUuMi)
figures_list.append(QHXKooHTpEuXMw)
figures_list.append(QEFQoomlfmOQTM)
figures_list.append(OMPAooMbyOIqeA)
figures_list.append(GGHOookMhIxqIK)
figures_list.append(CNVAooybLqXmVS)
figures_list.append(QNHAooSYgkWVhJ)
figures_list.append(HUBEoofsPjXOQx)
figures_list.append(BHESoofmkTbbZR)
figures_list.append(OYBTooNUcJLzDH)
figures_list.append(ASZLoocnIGlRHf)
figures_list.append(MBWHooeesXIrsz)
figures_list.append(ALAYooKKrRTkCG)
figures_list.append(PVRFoobvAzpZTq)
figures_list.append(WQVZooAhkdlegv)
figures_list.append(AESIooxXxRYQdT)
figures_list.append(LWVXooPyIlOKNd)
figures_list.append(FunctionFour)
figures_list.append(NWAEooQBLYYrpS)
"""
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
        pass
