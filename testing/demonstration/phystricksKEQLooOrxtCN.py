# -*- coding: utf8 -*-
from phystricks import *
def KEQLooOrxtCN():
    pspict,fig = SinglePicture("KEQLooOrxtCN")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(0.8)
    pspict.rotation(-25)

    l=3
    alpha=50

    M=Point(0,0)
    K=Point(l,0)
    C=Point(K.x+1,0)
    A=Point(C.x+l,0)

    L=CircleAB(M,K).get_point(alpha)
    B=CircleAB(C,A).get_point(alpha)

    trig1=Polygon(A,B,C)
    trig2=Polygon(K,L,M)
    trig1.put_mark(0.2,points_names=" B ",pspict=pspict)
    trig2.put_mark(0.2,points_names=" L ",pspict=pspict)

    A.put_mark(0.2,angle=-90,added_angle=0,text="\( A\)",pspict=pspict)
    C.put_mark(0.2,angle=-90,added_angle=0,text="\( C\)",pspict=pspict)
    K.put_mark(0.2,angle=-90,added_angle=0,text="\( K\)",pspict=pspict)
    M.put_mark(0.2,angle=-90,added_angle=0,text="\( M\)",pspict=pspict)

    rh1=RightAngleAOB(A,B,C)
    rh2=RightAngleAOB(K,L,M)

    a1=AngleAOB(B,A,C,r=0.3)
    a2=AngleAOB(L,K,M,r=0.3)

    S=a1.mark_point(pspict=pspict)
    T=a2.mark_point(pspict=pspict)
    S.put_mark(0.2,angle=None,added_angle=0,text="",pspict=pspict)
    T.put_mark(0.2,angle=None,added_angle=0,text="",pspict=pspict)


    droite=Segment(M,A).dilatation(1.2)
    droite.F.put_mark(0.2,angle=None,added_angle=0,text="\( (d)\)",pspict=pspict)

    no_symbol(  [ tr.vertices for tr in [trig1,trig2] ] ,droite.F )

    pspict.DrawGraphs(trig1,trig2,droite,rh1,rh2,a1,a2,S,T,droite.F)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
