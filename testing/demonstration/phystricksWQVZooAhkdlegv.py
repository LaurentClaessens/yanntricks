# -*- coding: utf8 -*-
from phystricks import *
def WQVZooAhkdlegv():
    pspict,fig = SinglePicture("WQVZooAhkdlegv")
    pspict.dilatation(1)

    A=Point(0,0)
    B=Point(5,0)
    O=Segment(A,B).midpoint()+(0,3)

    trig=Polygon(A,B,O)

    aA=AngleAOB(B,A,O)
    aA.parameters.color="red"
    aA.put_arrow(pspict=pspict)

    aO=AngleAOB(A,O,B)
    aO.parameters.color="red"
    aO.put_arrow(pspict=pspict)

    aB=AngleAOB(O,B,A)
    aB.parameters.color="red"
    aB.put_arrow(pspict=pspict)

    pspict.DrawGraphs(trig,aA,aO,aB)

    pspict.comment="The angles are red and an arrow is drawn in the trigonometric sense."

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
