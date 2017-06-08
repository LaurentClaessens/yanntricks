# -*- coding: utf8 -*-
from phystricks import *

def situation(P,text,pspict):
    A=P+(3,-2)
    O=P+(1.7999999999999998,-1.6)
    B=P+(0.585000000000000,0.155000000000000)
    a1=AngleAOB(A,O,B,r=0.3)
    a1.put_mark(text=text,pspict=pspict)

    s1=Segment(A,O)
    s2=Segment(B,O)

    pspict.DrawGraphs(a1,s1,s2)


def VAAYooXndWQq():
    pspict,fig = SinglePicture("VAAYooXndWQq")
    pspict.dilatation_X(1)
    pspict.dilatation_Y(1)

    situation(Point(0,0),"\( a^2\)",pspict)
    situation(Point(3,3),"\( mmmmmm\int_{\Omega}^{\mu}\)",pspict)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
