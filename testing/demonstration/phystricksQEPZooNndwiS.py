# -*- coding: utf8 -*-
from phystricks import *
def QEPZooNndwiS():
    pspict,fig = SinglePicture("QEPZooNndwiS")
    pspict.dilatation_X(1)
    pspict.dilatation_Y(1)

    h=2
    A=Point(0,0)
    B=Point(4,0)
    C=Point(1,-h)
    D=Point(6,-h)

    d1=Segment(A,B).dilatation(1.5)
    d2=Segment(D,C).dilatation(1.5)

    I=d1.midpoint()
    J=d2.midpoint()
    seg=Segment(I,J).dilatation(1.3)

    a1=AngleAOB(A,I,J)
    a2=AngleAOB(D,J,I)

    a1.put_mark(0.2,angle=None,text="\( a\)",pspict=pspict)
    a2.put_mark(0.2,angle=None,text="\( q\)",pspict=pspict)

    pspict.DrawGraphs(d1,d2,seg,a1,a2)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
