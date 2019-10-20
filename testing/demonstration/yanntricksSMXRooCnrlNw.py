# -*- coding: utf8 -*-
from yanntricks import *
def SMXRooCnrlNw():
    pspict,fig = SinglePicture("SMXRooCnrlNw")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(0.7)

    A=Point(0,0)
    B=Point(5,0)
    C=Point(B.x,-3)
    D=Point(A.x,C.y)

    rectangle=Polygon(A,B,C,D)

    F=rectangle.edges[1].midpoint()
    E=Point(   -F.y/tan(  35*pi/180  ),F.y  )

    prol=Segment(D,E)
    K=Intersection(prol,rectangle.edges[0])[0]

    s1=Segment(A,E)
    s2=Segment(D,E)
    s3=Segment(E,F)
    s4=Segment(E,K)
    rh=RightAngleAOB(B,F,E)

    rectangle.edges[1].divide_in_two(n=1,d=0.1,l=0.3,angle=45,pspict=pspict)
    put_equal_lengths_code(s1,s2,n=2,d=0.1,l=0.3,angle=45,pspict=pspict)

    no_symbol(rectangle.vertices,E,K,F)
    pspict.DrawGraphs(rectangle,K,E,F,s1,s2,s3,s4,rh)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
