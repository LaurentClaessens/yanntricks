# -*- coding: utf8 -*-
from phystricks import *
def TRJEooPRoLnEiG():
    pspict,fig = SinglePicture("TRJEooPRoLnEiG")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(1)

    O=Point(0,0)

    circle=Circle( O,2  )
    tg=circle.get_tangent_vector(30)
    A=circle.get_point(130)

    text="$ \lim_{s} (F\circ\gamma')  $"
    A.put_mark(dist=0.3,angle=None,text=text,automatic_place=(pspict,""))

    print(A.bounding_box(pspict))
    print(A.mark.bounding_box(pspict))
    bb=A.mark.bounding_box(pspict)
    pspict.DrawGraphs(circle,A,tg,bb)

    pspict.comment="A circle with a point and a mark : "+text

    #pspict.DrawDefaultAxes()
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
