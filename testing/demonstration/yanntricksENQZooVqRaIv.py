# -*- coding: utf8 -*-
from yanntricks import *

def rotation(angle,pts):
    ptsp=[  x.rotation(angle) for x in pts  ]
    return tuple(ptsp)

def truc(A,B,C,D,points_names,angle,pspicts,n):
    A,B,C,D=rotation(angle,[A,B,C,D])

    quadri=Polygon(A,B,C,D)
    quadri.put_mark(0.2,points_names=points_names,pspicts=pspicts)

    no_symbol(A,B,C,D)
    pspicts[n].DrawGraphs(quadri)
    

def ENQZooVqRaIv():
    pspicts,figs = IndependentPictures("ENQZooVqRaIv",4)

    for psp in pspicts:
        psp.dilatation(0.7)

    A=Point(0,0)
    B=Point(2,0)
    C=Point(3,-2)
    D=Point(-3,-2)
    truc(A,B,C,D,points_names="ABCD",angle=30,pspicts=pspicts,n=0)


    E=Point(0,0)
    F=Point(3,0)
    G=F+(-2,-2)
    H=E+G-F
    truc(E,F,G,H,points_names="EFGH",angle=64,pspicts=pspicts,n=1)


    I=Point(0,0)
    J=Point(2,0)
    K=J+(0,-3)
    L=I+K-J
    truc(I,J,K,L,points_names="IJKL",angle=-12,pspicts=pspicts,n=2)


    M=Point(0,0)
    N=M+(-1,-2)
    O=M+(1,-2)
    P=M+N+O
    truc(M,N,P,O,points_names="MNPO",angle=45,pspicts=pspicts,n=3)


    for fig in figs :
        fig.no_figure()
        fig.conclude()
        fig.write_the_file()

