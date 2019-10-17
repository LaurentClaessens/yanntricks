# -*- coding: utf8 -*-
from yanntricks import *
def GKMEooBcNxcWBt():
    pspict,fig = SinglePicture("GKMEooBcNxcWBt")
    var('x')
    f1 = phyFunction( x*sin(x) )
    f3 = phyFunction( x*cos(x) )

    llI = 0
    llF = 5
    F2 = ParametricCurve(f1,f3,interval=(llI,llF))

    for ll in F2.getRegularLengthParameters(llI,llF,2):
        v1 = F2.get_tangent_vector(ll)
        v2 = F2.get_normal_vector(ll)
        pspict.DrawGraphs(v1,v2)

    pspict.DrawGraphs(F2)
    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

