# -*- coding: utf8 -*-
from phystricks import *
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

    print("UN")
    mes1=Segment(D,S).get_measure(-0.3,0.1,None,"\( 6\)",pspict=pspict,position="corner")
    #mes3=Segment(E,T).get_measure(0.3,-0.1,None,"\( 3\)",pspict=pspict,position="corner")
    print("QUATRE")
    mes4=Segment(T,F).get_measure(0.3,-0.1,None,"\( 7\)",pspict=pspict,position="corner")

    #pspict.DrawGraphs(mes1,mes3,mes4,triangle)
    pspict.DrawGraphs(mes1,mes4,triangle)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
