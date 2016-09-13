# -*- coding: utf8 -*-
from phystricks import *
def OGGDooIvakwNlL():
    pspicts,figs = IndependentPictures("OGGDooIvakwNlL",2)

    for psp in pspicts :
        psp.dilatation(1)

    A=Point(0,0)
    B=A+(4,0)
    C=A+(1,2)
    D=A+C-B

    parall=Polygon(A,B,C,D)
    parall.put_mark(0.2,pspicts=pspicts)
    diag1=Segment(A,C)

    no_symbol(parall.vertices)

    a1=AngleAOB(C,A,D,r=0.3)
    a2=AngleAOB(B,A,C)
    c1=AngleAOB(D,C,A,)
    c2=AngleAOB(A,C,B,r=0.3)

    a1.put_mark(0.2,angle=None,text="\( a_1\)",pspict=pspicts[0])
    a2.put_mark(0.2,angle=None,text="\( a_2\)",pspict=pspicts[0])
    c1.put_mark(0.2,angle=None,text="\( c_1\)",pspict=pspicts[0])
    c2.put_mark(0.2,angle=None,text="\( c_2\)",pspict=pspicts[0])

    a1.put_mark(0.2,angle=None,text="\( b\)",pspict=pspicts[1])
    a2.put_mark(0.2,angle=None,text="\( a\)",pspict=pspicts[1])
    c1.put_mark(0.2,angle=None,text="\( a\)",pspict=pspicts[1])
    c2.put_mark(0.2,angle=None,text="\( b\)",pspict=pspicts[1])

    pspicts[0].DrawGraphs(parall,diag1,a1,a2,c1,c2)
    pspicts[1].DrawGraphs(parall,diag1,a1,a2,c1,c2)

    pspicts[0].comment="The marks are $a_1,a_2,c_1,c_2$"
    pspicts[1].comment="The marks are $b,a,a,b$"

    for fig in figs:
        fig.no_figure()
        fig.conclude()
        fig.write_the_file()

