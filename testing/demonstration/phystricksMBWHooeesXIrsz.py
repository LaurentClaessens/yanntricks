# -*- coding: utf8 -*-
from phystricks import *
def MBWHooeesXIrsz():
    pspict,fig = SinglePicture("MBWHooeesXIrsz")
    pspict.dilatation(0.3)

    l=4
    A=Point(0,0)
    B=Point(l,0)
    C=Point(l,l)

    trig=Polygon(A,B,C)
    trig.put_mark(0.2,pspict=pspict)
    trig.edges[0].put_code(n=2,d=0.1,l=0.2,pspict=pspict)
    trig.edges[1].put_code(n=2,d=0.1,l=0.2,pspict=pspict)

    no_symbol(trig.vertices)
    pspict.DrawGraphs(trig)
    pspict.comment="Vérifier la longueur des codages."
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

