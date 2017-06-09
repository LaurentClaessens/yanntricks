# -*- coding: utf8 -*-
from phystricks import *
def VRQCooOchjJA():
    pspict,fig = SinglePicture("VRQCooOchjJA")
    pspict.dilatation(1)

    A=Point(1.5,2.5)
    O=Point(0.75,1.25)
    B=Point(0.000000000000000,0.750000000000000)

    s1=Segment(O,A)
    s2=Segment(O,B)

    ang=AngleAOB(A,O,B,r=0.3)
    ang.put_mark(0.35,None,"\SI{140}{\degree}",pspict=pspict)

    pspict.DrawGraphs(s1,s2,ang)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

