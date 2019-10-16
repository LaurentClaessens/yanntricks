# -*- coding: utf8 -*-
from yanntricks import *
def AMDUooZZUOqa():
    pspict,fig = SinglePicture("AMDUooZZUOqa")

    R=2
    theta=-10
    sigma=60
    O=Point(0,0)
    
    P=Point(1.96961550602442, -0.347296355333861)
    Q=Point(1.00000000000000, 1.73205080756888)

    angle=AngleAOB(P,O,Q,r=0.5)
    angle.put_mark(0.2,None,r"$\theta$",pspict=pspict)
    seg_theta=Segment(O,P)
    seg_sigma=Segment(O,Q)
    
    pspict.DrawGraphs(angle,seg_theta,seg_sigma)
    fig.conclude()
    fig.write_the_file()
