# -*- coding: utf8 -*-

from __future__ import division

from phystricks import *
def BQFUooTuMfnj():
    pspict,fig = SinglePicture("BQFUooTuMfnj")
    pspict.dilatation(0.5)

    A=Point(10,0)
    O=Point(0,0)
    B=Point(12*cos(2/9*pi),12*sin(2/9*pi))

    s1=Segment(O,A)
    s2=Segment(O,B)

    ang=AngleAOB(A,O,B)
    ang.put_mark(text="\( 40\)",pspict=pspict)

    pspict.DrawGraphs(s1,s2,ang)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

