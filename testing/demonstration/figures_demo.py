#! /usr/bin/sage -python
# -*- coding: utf8 -*-

import sys
from phystricks import *


from phystricksSFdgHdO import SFdgHdO
from phystricksNWAEooQBLYYrpS import NWAEooQBLYYrpS
from phystricksProjPoly import ProjPoly
from phystricksEDEYRhQ import EDEYRhQ
from phystricksSMXRooCnrlNw import SMXRooCnrlNw
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
from phystricksTKXZooLwXzjS import TKXZooLwXzjS

figures_list_1=[]
figures_list_1.append(UARHooLMWqvyaI)
figures_list_1.append(SMXRooCnrlNw)
figures_list_1.append(EDEYRhQ)
figures_list_1.append(TKXZooLwXzjS)
figures_list_1.append(DYJNooLVVFHEfN)
figures_list_1.append(OGGDooIvakwNlL)
figures_list_1.append(PFCUoorQhitKoJ)
figures_list_1.append(QIXEooejrojKjo)
figures_list_1.append(AxesSecond)
figures_list_1.append(exCircle)
figures_list_1.append(exCircleThree)
figures_list_1.append(exCircleTwo)
figures_list_1.append(OnePoint)
figures_list_1.append(FunctionFirst)
figures_list_1.append(FunctionFive)
figures_list_1.append(FunctionSecond)
figures_list_1.append(QIPRoolQCEnZdx)
figures_list_1.append(GridThree)
figures_list_1.append(GridTwo)
figures_list_1.append(MarkOnPoint)
figures_list_1.append(ParametricOne)
figures_list_1.append(ParametricTwo)
figures_list_1.append(TRJEooPRoLnEiG)
figures_list_1.append(UREIooqNGBXtHg)
figures_list_1.append(DEIToomZFknFmn)
figures_list_1.append(HELQooLGapRQrr)
figures_list_1.append(YJEDoojDtSeKHQ)
figures_list_1.append(QRJOooKZPUoLlF)
figures_list_1.append(RVKFooDxrqYXAX)
figures_list_1.append(PJKBooOhGVPkeR)
figures_list_1.append(LVPSoozFTyaeCG)
figures_list_1.append(CUZFooGqZLaAEp)
figures_list_1.append(JSYWooQYduLVLS)
figures_list_1.append(YOWDooyeyOJyml)
figures_list_1.append(QRXCooUmnlhkvh)
figures_list_1.append(VLEGoolDFCdZDU)
figures_list_1.append(MXKAoozETwoiTe)
figures_list_1.append(XBAUooFtMWukKr)
figures_list_1.append(OMZOoowEtRUuMi)
figures_list_1.append(QHXKooHTpEuXMw)
figures_list_1.append(QEFQoomlfmOQTM)
figures_list_1.append(GGHOookMhIxqIK)
figures_list_1.append(CNVAooybLqXmVS)
figures_list_1.append(HUBEoofsPjXOQx)
figures_list_1.append(BHESoofmkTbbZR)
figures_list_1.append(OYBTooNUcJLzDH)
figures_list_1.append(ASZLoocnIGlRHf)
figures_list_1.append(MBWHooeesXIrsz)
figures_list_1.append(ALAYooKKrRTkCG)
figures_list_1.append(PVRFoobvAzpZTq)
figures_list_1.append(WQVZooAhkdlegv)
figures_list_1.append(NWAEooQBLYYrpS)
figures_list_1.append(AESIooxXxRYQdT)
figures_list_1.append(LWVXooPyIlOKNd)
figures_list_1.append(FunctionFour)
figures_list_1.append(ProjPoly)
figures_list_1.append(OMPAooMbyOIqeA)
figures_list_1.append(FMLCooxHtqRzUz)
figures_list_1.append(EXIIooJzzoJeai)
figures_list_1.append(SFdgHdO)
"""
figures_list_1.append(<++>)
figures_list_1.append(<++>)
"""

figures_list_2=[]
figures_list_2.append(SFdgHdO)
figures_list_2.append(PJKBooOhGVPkeR)
figures_list_2.append(TRJEooPRoLnEiG)
figures_list_2.append(CUZFooGqZLaAEp)
figures_list_2.append(QHXKooHTpEuXMw)
figures_list_2.append(YJEDoojDtSeKHQ)
figures_list_2.append(FunctionFirst)
figures_list_2.append(exCircleTwo)
figures_list_2.append(MXKAoozETwoiTe)
figures_list_2.append(ASZLoocnIGlRHf)
figures_list_2.append(AESIooxXxRYQdT)
figures_list_2.append(GGHOookMhIxqIK)
figures_list_2.append(PVRFoobvAzpZTq)
figures_list_2.append(MarkOnPoint)
figures_list_2.append(UREIooqNGBXtHg)
figures_list_2.append(QIPRoolQCEnZdx)
figures_list_2.append(QRXCooUmnlhkvh)
figures_list_2.append(DYJNooLVVFHEfN)
figures_list_2.append(ParametricOne)
figures_list_2.append(exCircleThree)
figures_list_2.append(EDEYRhQ)
figures_list_2.append(UARHooLMWqvyaI)
figures_list_2.append(FunctionFour)
figures_list_2.append(ALAYooKKrRTkCG)
figures_list_2.append(QIXEooejrojKjo)
figures_list_2.append(LWVXooPyIlOKNd)
figures_list_2.append(QEFQoomlfmOQTM)
figures_list_2.append(BHESoofmkTbbZR)
figures_list_2.append(NWAEooQBLYYrpS)
figures_list_2.append(YOWDooyeyOJyml)
figures_list_2.append(HUBEoofsPjXOQx)
figures_list_2.append(AxesSecond)
figures_list_2.append(PFCUoorQhitKoJ)
figures_list_2.append(RVKFooDxrqYXAX)
figures_list_2.append(FunctionFive)
figures_list_2.append(OYBTooNUcJLzDH)
figures_list_2.append(OGGDooIvakwNlL)
figures_list_2.append(OMPAooMbyOIqeA)


figures_list_3=[]
figures_list_3.append(AESIooxXxRYQdT)
figures_list_3.append(FunctionFour)

def AllFigures():

    figures_list=figures_list_1
    if "--pass-number=2" in sys.argv :
        figures_list=figures_list_2
    if "--pass-number=3" in sys.argv :
        figures_list=figures_list_3


    tests=FigureGenerationSuite(figures_list,first=0,title=u"demonstration pictures")
    tests.generate()
    tests.summary()

if __name__=="__main__":
    if "--all" in sys.argv :
        AllFigures()
    else:
        pass
