# -*- coding: utf8 -*-
from yanntricks import *
def SFdgHdO():
    pspict,fig = SinglePicture("SFdgHdO")
    pspict.dilatation(1)

    A = Point(1,0)
    B = Point(-1,0)
    C = Point(0,1)
    D = Point(0,-1)

    A.parameters.color = "red"
    B.parameters.color = A.parameters.color
    C.parameters.color = "brown"
    D.parameters.color = C.parameters.color

    A.add_option("dotscale=1.3")
    B.add_option("dotscale=1.3")
    C.add_option("dotscale=1.3")
    D.add_option("dotscale=1.3")

    pspict.DrawGraphs(A,B,C,D)

    pspict.axes.no_graduation()
    pspict.axes.single_axeX.put_mark(dist=0.2,angle=-45,text="$K_H$",pspict=pspict)

    pspict.DrawDefaultAxes()
    fig.conclude()
    fig.write_the_file()
