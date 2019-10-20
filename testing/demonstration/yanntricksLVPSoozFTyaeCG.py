# -*- coding: utf8 -*-
from yanntricks import *
def LVPSoozFTyaeCG():
    pspict,fig = SinglePicture("LVPSoozFTyaeCG")
    pspict.dilatation(1)

    Ra=1
    Rb=2

    x=var('x')
    curve1=ParametricCurve(Ra*cos(x),Ra*sin(x))
    curve2=ParametricCurve(Rb*cos(x),Rb*sin(x))

    # With an interval 0,2*pi this does not work.
    surface=SurfaceBetweenParametricCurves(curve1,curve2,interval=(0,2*pi-0.001))
    surface.parameters.filled()
    surface.parameters.fill.color="cyan"
    surface.Fsegment.parameters.style="none"
    surface.Isegment.parameters.style="none"
    surface.curve1.parameters.color="red"
    surface.curve2.parameters=surface.curve1.parameters

    pspict.DrawGraphs(surface)
    pspict.axes.no_graduation()
    pspict.comment="Une couronne"

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
