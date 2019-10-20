# -*- coding: utf8 -*-
from yanntricks import *
def GGHOookMhIxqIK():
    pspict,fig = SinglePicture("GGHOookMhIxqIK")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(1)

    x=var('x')
    f=phyFunction(2.7*sin(x)).graph(-5,5)
    pspict.DrawGraphs(f)

    # The grid must be drawn before the axes because we want the axes to take
    # the grid into account
    pspict.DrawDefaultGrid()
    pspict.DrawDefaultAxes()
    pspict.comment="\( x\mapsto 2.7\sin(x)\), the axes and the grid"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
