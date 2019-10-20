# -*- coding: utf8 -*-

from __future__ import division
from __future__ import unicode_literals
from yanntricks import *

def mark_point(s,pspict=None):
    return s.midpoint()

def EDEYRhQ():
    pspict,fig = SinglePicture("EDEYRhQ")
    pspict.dilatation_X(1/6)
    pspict.dilatation_Y(1)

    from yanntricks.src.SegmentGraph import SegmentGraph
    SegmentGraph.mark_point=mark_point

    l1=10
    l2=15
    l3=9
    l4=9
    l5=12

    x=var('x')
    A=Point(-4,0)
    B=Point(6,0)
    C=Point(21,0)
    D=Point(30,0)
    E=Point(39,0)
    F=Point(51,0)

    A.put_mark(0.2,text="Besançon",pspict=pspict,position="N")
    B.put_mark(0.2,text="St-Vit",pspict=pspict,position="N")
    C.put_mark(0.2,text="Dole",pspict=pspict,position="N")
    D.put_mark(0.2,text="Auxonne",pspict=pspict,position="N")
    E.put_mark(0.2,text="Genlis",pspict=pspict,position="N")
    F.put_mark(0.2,text="Dijon",pspict=pspict,position="N")

    AB=AffineVector(A,B)
    BC=AffineVector(B,C)
    CD=AffineVector(C,D)
    EF=AffineVector(E,F)
    DE=AffineVector(D,E)

    AB.mark_point=AB.midpoint
    BC.mark_point=BC.midpoint
    CD.mark_point=CD.midpoint
    EF.mark_point=EF.midpoint
    DE.mark_point=DE.midpoint

    AB.put_mark(0.2,text="\( {}\)".format(B.x-A.x),pspict=pspict,position="S")
    BC.put_mark(0.2,text="\( {}\)".format(C.x-B.x),pspict=pspict,position="S")
    CD.put_mark(0.2,text="\( {}\)".format(D.x-C.x),pspict=pspict,position="S")
    DE.put_mark(0.2,text="\( {}\)".format(E.x-D.x),pspict=pspict,position="S")
    EF.put_mark(0.2,text="\( {}\)".format(F.x-E.x),pspict=pspict,position="S")

    AB.parameters.color="brown"
    BC.parameters.color="brown"
    CD.parameters.color="brown"
    DE.parameters.color="brown"
    EF.parameters.color="brown"

    pspict.comment="Les nombres arrivent au centre des vecteurs, et non au bout."
    pspict.DrawGraphs(A,B,C,D,E,F,AB,BC,CD,DE,EF)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
