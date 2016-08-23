# -*- coding: utf8 -*-
from phystricks import *

def rotation(angle,pts):
    ptsp=[  x.rotation(angle) for x in pts  ]
    return tuple(ptsp)

def truc(A,B,C,D,points_names,angle,pspict):
    A,B,C,D=rotation(angle,[A,B,C,D])

    quadri=Polygon(A,B,C,D)
    quadri.put_mark(0.2,points_names=points_names,pspict=pspict)

    no_symbol(A,B,C,D)
    return quadri
    
def FMLCooxHtqRzUz():
    pspict,fig = SinglePicture("FMLCooxHtqRzUz")

    pspict.dilatation(1)

    O=Point(0,0)
    L=O+(1,1)
    N=O+O-L
    K=O+(-4,1)
    M=O+O-K
    quadri=truc(K,L,M,N,points_names="KLMN",angle=-27,pspict=pspict)

    dig1=Segment(quadri.vertices[0],quadri.vertices[2])
    dig2=Segment(quadri.vertices[1],quadri.vertices[3])

    dig1.divide_in_two(n=2,d=0.1,l=0.2,angle=45,pspict=pspict)
    dig2.divide_in_two(n=1,d=0.1,l=0.2,angle=45,pspict=pspict)
    pspict.DrawGraphs(dig1,dig2,quadri)
    pspict.comment="The segments KM is divided by // and the segment NL by a simple /."

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
