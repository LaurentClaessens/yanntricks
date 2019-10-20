# -*- coding: utf8 -*-
from yanntricks import *
def PVRFoobvAzpZTq():
    pspict,fig = SinglePicture("PVRFoobvAzpZTq")
    pspict.dilatation(0.5)

    D=Point(0,0)
    E=Point(8,0)
    c1=Circle(D,12)
    c2=Circle(E,6)
    F=Intersection(c1,c2)[1]

    triangle=Polygon(D,E,F)

    S=triangle.edges[2].midpoint()
    T=triangle.edges[1].midpoint()

    mes1=Segment(D,S).get_measure(-0.3,0.1,None,"\( 6\)",pspict=pspict,position="corner")
    mes4=Segment(T,F).get_measure(0.3,-0.1,None,"\( 7\)",pspict=pspict,position="corner")

    pspict.DrawGraphs(mes1,mes4,triangle)
    pspict.comment="The marks 6 and 7 are well positioned"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
