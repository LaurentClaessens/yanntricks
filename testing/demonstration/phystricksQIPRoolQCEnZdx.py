# -*- coding: utf8 -*-
from phystricks import *
def QIPRoolQCEnZdx():
    pspict,fig = SinglePicture("QIPRoolQCEnZdx")
    pspict.dilatation(1)

    A=Point(0,0)
    C=Point(3,0)
    aC=40
    aA=110
    interm1=Circle(A,2).get_point(aA)
    interm2=Circle(C,2).get_point(180-aC)

    B=Intersection( Segment(A,interm1), Segment(  C,interm2 ))[0]

    trig=Polygon(A,B,C)
    trig.put_mark(0.2,pspict=pspict)

    for P in trig.vertices:
        P.parameters.symbol=""

    angA=Angle(C,A,B,r=0.3)
    angB=Angle(A,B,C,r=0.3)
    angC=Angle(B,C,A,r=0.3)

    angA.put_mark(0.1,None,"\SI{"+str(aA)+"}{\degree}",automatic_place=(pspict,"center"))
    #angB.put_mark(0.2,None,"\SI{120}{\degree}",automatic_place=(pspict,""))
    angC.put_mark(0.2,None,"\SI{"+str(aC)+"}{\degree}",automatic_place=(pspict,""))

    pspict.comment="Les 110 et 40 sur les angles sont à peu près bien placés. Sauf le 'degré' du 40 qui frôle un peu [BC]."
    pspict.DrawGraphs(trig,angA,angB,angC)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
