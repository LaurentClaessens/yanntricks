# -*- coding: utf8 -*-
from yanntricks import *
def QLXFooBDalHMaT():
    pspict,fig = SinglePicture("QLXFooBDalHMaT")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(1)

    ################################
    # The important lines are here
    # Define here your objects
    # example :
    P=Point(1,3)

    pspict.DrawGraphs(P)
    pspict.DrawDefaultAxes()
    
    ##############################

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
