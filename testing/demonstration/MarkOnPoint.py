# -*- coding: utf8 -*-

from phystricks import *
def MarkOnPoint():
    pspict,fig = SinglePicture("MarkOnPoint")

    P = Point(0,0)
    P.parameters.color = "blue"
    P.put_mark(0.3,45,"çà",pspict=pspict)

    Q = Point(1,1)
    Q.put_mark(0.3,180,"$q$",pspict=pspict)
    Q.parameters.symbol = "diamond"

    pspict.DrawGraphs(P)
    pspict.DrawGraphs(Q)

    pspict.comment=u"unicode in the mark : çà"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

