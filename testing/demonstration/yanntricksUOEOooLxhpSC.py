# -*- coding: utf8 -*-
from yanntricks import *
def UOEOooLxhpSC():
    pspict,fig = SinglePicture("UOEOooLxhpSC")
    pspict.dilatation(1)

    cot=3
    A=Point(0,0)
    B=A+(cot,0)
    C=B+(0,-cot)
    D=A+(0,-cot)

    carre=Polygon(A,B,C,D)

    dig2=Segment(B,D)
    d2=AngleAOB(B,D,A)
    d2.put_mark(text="\( d_2\)",pspict=pspict)

    pspict.DrawGraphs(carre,d2,dig2)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
