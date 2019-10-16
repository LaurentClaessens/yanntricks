# -*- coding: utf8 -*-
from __future__ import division
from yanntricks import *


def ERPMooZibfNOiU():
    pspict,fig = SinglePicture("ERPMooZibfNOiU")
    pspict.dilatation(1)

    t0=40
    a=2.3
    b=1.3
    O=Point(0,0)
    lp=Segment( O,Circle(O,5).getPoint(t0)    )
    P=lp.midpoint()

    fun = lambda t:Point(a*cos(t),b*sin(t)).rotation(t0)+P 
    decal=fun(pi/2)-P
    Gamma = NonAnalyticPointParametricCurve( lambda x:fun(x)+decal  ,0,2*pi  )
    Gamma.parameters.plotpoints=20

    pt=Gamma(3*pi/2-0.15)
    xx=pt.x
    v=AffineVector(P,pt).normalize(2)
    v.parameters.color="blue"
    pspict.DrawGraphs(v)
    F=v.F
    Fx=F.x

    a=7.73542889062775*cos(11/9*pi + 1.30951587282752) - 7.55775391156456*cos(5/18*pi) + 2.5*cos(2/9*pi)
    print(numerical_approx(a))
    print(numerical_approx(a,digits=5))

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
