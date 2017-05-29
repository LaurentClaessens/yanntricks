# -*- coding: utf8 -*-
from phystricks import *
def KEQLooOrxtCN():
    pspict,fig = SinglePicture("KEQLooOrxtCN")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.rotation(-25)

    A=Point(0,0)
    B=Point(3,0)
    C=Point(3,-1)

    trig1=Polygon(A,B,C)
    trig1.put_mark(0.2,points_names=" B ",pspict=pspict)

    pspict.DrawGraphs(trig1)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
