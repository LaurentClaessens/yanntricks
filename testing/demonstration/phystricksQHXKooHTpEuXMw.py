# -*- coding: utf8 -*-
from phystricks import *
def QHXKooHTpEuXMw():
    pspict,fig = SinglePicture("QHXKooHTpEuXMw")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(1)

    P=Point(0,0)
    P.put_mark(0.2,45,"P",pspict=pspict)
    l1=Segment( Point(0,0.5),Point(0.35,0)  )
    l1.parameters.color="red"
    l2=Segment( Point(0.5,0.5),Point(0,0)  )
    l2.parameters.color="cyan"

    pspict.DrawGraphs(l1,P,l2)
    pspict.comment="The mark P is over the red line and under the cyan line."
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()


    # Une marque au dessus et en dessous de lignes.
