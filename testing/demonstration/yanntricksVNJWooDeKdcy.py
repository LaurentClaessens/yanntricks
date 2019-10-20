# -*- coding: utf8 -*-

from __future__ import division
from yanntricks import *

def VNJWooDeKdcy():
    pspict,fig = SinglePicture("VNJWooDeKdcy")
    pspict.dilatation(0.8)

    A=Point(0,0)
    O=Point(3,2)
    B=Point(1.9266624057974,-0.751559074504527)
    s1=Segment(A,O)
    s2=Segment(B,O)

    angle=AngleAOB(A,O,B)
    angle.put_mark(text="\SI{33}{\degree}",pspict=pspict)


    pspict.DrawGraphs(s1,s2,angle)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
