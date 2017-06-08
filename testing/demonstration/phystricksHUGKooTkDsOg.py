# -*- coding: utf8 -*-
from phystricks import *
def HUGKooTkDsOg():
    pspict,fig = SinglePicture("HUGKooTkDsOg")
    pspict.dilatation(1)

    A=Point(2,3)
    O=Point(6,-1)
    B=Point(0,0)
    s1=Segment(A,O)
    s2=Segment(B,O)

    a1=AngleAOB(A,O,B,r=0.8)
    a1.put_mark(text="\SI{30}{\degree}",pspict=pspict)

    pspict.DrawGraphs(s1,s2,a1)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
