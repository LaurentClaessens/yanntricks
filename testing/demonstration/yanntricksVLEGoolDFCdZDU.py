# -*- coding: utf8 -*-
from yanntricks import *
def VLEGoolDFCdZDU():
    pspict,fig = SinglePicture("VLEGoolDFCdZDU")

    pspict.dilatation_X(1)
    pspict.dilatation_Y(1)

    K=Point(0,0)
    M=Point(2.5,0)
    L=Point(M.x,-2)

    trig=Polygon(K,L,M)
    trig.edges_parameters.color="brown"

    rh=RightAngleAOB(L,M,K)

    no_symbol(trig.vertices)
    pspict.comment="A right angle is coded. And a brown triangle is drawn"
    pspict.DrawGraphs(trig,rh)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
