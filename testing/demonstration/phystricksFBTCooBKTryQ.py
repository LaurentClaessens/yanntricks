# -*- coding: utf8 -*-
from phystricks import *
def FBTCooBKTryQ():
    pspict,fig = SinglePicture("FBTCooBKTryQ")
    pspict.dilatation_X(1)
    pspict.dilatation_Y(1)

    O=Point(0,0)
    A=O+(2,1)
    C=O+(-2,-1)

    s1=Segment(C,A).dilatation(1.5)
    P=O+(3,-1)
    s2=Segment(O,P)

    a1=AngleAOB(P,O,A)
    a2=AngleAOB(C,O,P,r=0.3)

    #a1.put_mark(0.2,None,"\( 24\)",pspict=pspict)
    #a2.put_mark(0.2,None,"\( 130 \)",pspict=pspict)
    a1.put_mark(0.35,None,"\( 24\)",pspict=pspict)
    a2.put_mark(0.35,None,"\( 130 \)",pspict=pspict)

    no_symbol(A,O,C)

    pspict.DrawGraphs(s1,s2,a1,a2,A,O,C)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
