# -*- coding: utf8 -*-
from yanntricks import *
def NWAEooQBLYYrpS():
    pspict,fig = SinglePicture("NWAEooQBLYYrpS")
    pspict.dilatation(2)

    D=Point(0,0)
    B=Circle(D,6).get_point(25)
    C=Point(B.x,D.y)
    A=Point(D.x,B.y)

    rect=Polygon(A,B,C,D)
    rect.put_mark(0.2,pspict=pspict)
    rect.make_edges_independent()

    ai1=AngleAOB(D,B,C)
    ai2=AngleAOB(B,D,A)
    ai1.put_mark(text="?",pspict=pspict)
    ai2.put_mark(text="?",pspict=pspict)

    diag=Segment(D,B)

    no_symbol(rect.vertices)
    pspict.comment="The angles are well circular"
    pspict.DrawGraphs(rect,ai1,ai2,diag)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
