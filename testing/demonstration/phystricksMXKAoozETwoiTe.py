# -*- coding: utf8 -*-
from phystricks import *
def MXKAoozETwoiTe():
    pspict,fig = SinglePicture("MXKAoozETwoiTe")
    pspict.dilatation(1)

    H=Histogram([(0,15,20),(15,65,65),(65,110,15)])

    pspict.DrawGraphs(H)
    pspict.DrawDefaultAxes()
    fig.conclude()
    fig.write_the_file()
