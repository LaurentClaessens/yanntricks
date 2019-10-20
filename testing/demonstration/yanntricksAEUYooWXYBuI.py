# -*- coding: utf8 -*-

from __future__ import division
from yanntricks import *

def AEUYooWXYBuI():
    pspict,fig = SinglePicture("AEUYooWXYBuI")
    
    A=Point(-2*cos(1/9*pi),2*sin(1/9*pi))
    O=Point(0,0)
    B=Point(-2*cos(43/180*pi),-2*sin(43/180*pi))

    s1=Segment(A,O)
    s2=Segment(B,O)

    angle=AngleAOB(A,O,B)
    angle.put_mark(text="\( \int_A40mmmm\)",pspict=pspict)

    pspict.DrawGraphs(s1,s2,angle)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
