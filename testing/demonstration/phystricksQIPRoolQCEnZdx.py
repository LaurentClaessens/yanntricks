# -*- coding: utf8 -*-
from phystricks import *
def QIPRoolQCEnZdx():
    pspict,fig = SinglePicture("QIPRoolQCEnZdx")
    pspict.dilatation(1)

    A=Point(0,0)
    B=Point(-1,2)
    C=Point(3,0)

    trig=Polygon(A,B,C)

    angA=AngleAOB(C,A,B,r=0.3)
    angA.put_mark(0.1,None,"\SI{110}{\degree}",pspict=pspict)

    sAB=Segment(A,B)
    sAC=Segment(A,C)

    pspict.comment="The angle at A has a mark 110 degree."
    pspict.DrawGraphs(angA,trig,sAB,sAC)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
