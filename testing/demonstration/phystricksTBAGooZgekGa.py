# -*- coding: utf8 -*-

from __future__ import division
from phystricks import *

def TBAGooZgekGa():
    pspict,fig = SinglePicture("TBAGooZgekGa")
    
    A=Point(0,0)
    O=Point(4,2)
    B=Point(5,0)

    s1=Segment(A,O)
    s2=Segment(B,O)

    angle=AngleAOB(A,O,B)
    angle.put_mark(text="\( c\)",pspict=pspict)


    pspict.DrawGraphs(s1,s2,angle)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
