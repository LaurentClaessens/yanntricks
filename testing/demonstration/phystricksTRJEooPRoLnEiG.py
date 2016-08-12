# -*- coding: utf8 -*-
from phystricks import *
def TRJEooPRoLnEiG():
    pspict,fig = SinglePicture("TRJEooPRoLnEiG")
    pspict.dilatation(1)

    O=Point(0,0)

    circle=Circle( O,2  )
    tg=circle.get_tangent_vector(30)
    A=circle.get_point(130)
    B=circle.get_point(220)

    textA="$ \lim_{s} (F\circ\gamma')  $"
    textB="$ K $"
    A.put_mark(dist=0.3,angle=None,text=textA,pspict=pspict)
    B.put_mark(dist=0.3,angle=None,text=textB,pspict=pspict)

    pspict.DrawGraphs(circle,A,tg,B)

    pspict.comment="A circle with a point and a mark : "+textA+" and on other point with the mark "+textB

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
