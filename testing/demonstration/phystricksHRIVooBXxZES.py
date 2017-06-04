# -*- coding: utf8 -*-
from phystricks import *
def HRIVooBXxZES():
    pspict,fig = SinglePicture("HRIVooBXxZES")
    pspict.dilatation_X(7)
    pspict.dilatation_Y(2)

    A=Point(0,0)
    B=A+(-1,-2)
    C=A+(1,-2)

    trig=Polygon(A,B,C)

    a1=AngleAOB(B,A,C)
    a1.put_mark(text="\SI{40}{\degree}",pspict=pspict)

    pspict.DrawGraphs(trig,a1)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
