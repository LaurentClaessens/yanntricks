# -*- coding: utf8 -*-

from __future__ import division
from phystricks import *

def AAPMooHEcnzW():
    pspict,fig = SinglePicture("AAPMooHEcnzW")
    

    A=Point(3,0)
    O=Point(0,0)
    B=Point(-605873621538960/459316041022793,1664624094221487/459316041022793)

    s1=Segment(A,O)
    s2=Segment(B,O)

    angle=AngleAOB(A,O,B,r=0.3)
    aA=110
    angle.put_mark(text="\SI{"+str(aA)+"}{\degree}",pspict=pspict)

    pspict.DrawGraphs(s1,s2,angle)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
