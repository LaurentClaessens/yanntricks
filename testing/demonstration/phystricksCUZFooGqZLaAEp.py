# -*- coding: utf8 -*-
from phystricks import *
def CUZFooGqZLaAEp():
    pspict,fig = SinglePicture("CUZFooGqZLaAEp")
    pspict.dilatation(1)

    t0=40
    a=1.3
    b=2.3
    O=Point(0,0)
    lp=Segment( O,Circle(O,5).getPoint(t0) )
    P=lp.midpoint()
    P.put_mark(0.3,angle=None,added_angle=0,text="\( P\)",automatic_place=(pspict,""))

    Gamma = NonAnalyticPointParametricCurve(  lambda t:Point(a*cos(t),b*sin(t)).rotation(t0)+P  ,0,pi  )
    Gamma.parameters.plotpoints=50

    pspict.DrawGraphs(lp,P,Gamma)

    pspict.comment="A half-ellips is posed on the line and centered on the point P"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
