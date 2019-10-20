# -*- coding: utf8 -*-
from yanntricks import *
def JRCJooPHFcKn():
    pspict,fig = SinglePicture("JRCJooPHFcKn")
    pspict.dilatation(1)

    A=Point(0,0)
    B=Point(5,0)
    C=Point(2,3)


    ptriangle=Polygon(A,B,C)

    ptriangle.put_mark(0.3,text_list=["","\( F\)","\( E\)"],pspict=pspict)

    pspict.DrawGraphs(ptriangle)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
