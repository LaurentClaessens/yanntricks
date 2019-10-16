# -*- coding: utf8 -*-
from yanntricks import *
def HYVFooTHaDDQ():
    pspicts,figs = IndependentPictures("HYVFooTHaDDQ",4)
    for psp in pspicts:
        psp.dilatation(1)

    Ap=Point(0,0)
    Bp=Point(3,0)
    Cp=Segment(Ap,Bp).midpoint()+(0,2)
    trig=Polygon(Ap,Bp,Cp).rotation(25)
    A=trig.vertices[0]
    B=trig.vertices[1]
    C=trig.vertices[2]
    trig.put_mark(0.2,pspicts=pspicts)
    M=trig.edges[0].midpoint()
    M.put_mark(0.2,angle=None,added_angle=180,text="\( M\)",pspicts=pspicts)
    trig.edges[0].divide_in_two(n=2,d=0.1,l=0.3,angle=45,pspicts=pspicts)

    ang=AngleAOB(A,C,B)
    ang.put_mark(0.4,angle=None,added_angle=0,text="\SI{34}{\degree}",pspicts=pspicts)
    no_symbol(trig.vertices)
    pspicts[0].DrawGraphs(trig,M,ang)

    
    Cpp=Segment(A,B).midpoint()+(0,2)
    trig=Polygon(Ap,Bp,Cpp).rotation(47)
    trig.put_mark(0.2,pspicts=pspicts)
    A=trig.vertices[0]
    B=trig.vertices[1]
    C=trig.vertices[2]
    M=trig.edges[0].midpoint()
    M.put_mark(0.2,angle=None,added_angle=180,text="\( M\)",pspicts=pspicts)
    cod1=trig.edges[1].get_code(n=2,d=0.1,l=0.3,pspicts=pspicts)
    cod2=trig.edges[2].get_code(n=2,d=0.1,l=0.3,pspicts=pspicts)
    CM=Segment(C,M)
    rh=RightAngleAOB(C,M,B)
    no_symbol(trig.vertices)
    pspicts[1].DrawGraphs(trig,M,CM,rh,cod1,cod2)

    trig=Polygon(Ap,Bp,Cpp).rotation(-20)
    print(Ap)
    print(Bp)
    print(Cpp)
    trig.put_mark(0.2,pspicts=pspicts)
    A=trig.vertices[0]
    B=trig.vertices[1]
    C=trig.vertices[2]
    M=trig.edges[0].midpoint()
    M.put_mark(0.2,angle=None,added_angle=180,text="\( M\)",pspicts=pspicts)
    CM=Segment(C,M)
    rh=RightAngleAOB(C,M,B)
    ang=AngleAOB(M,A,C)
    ang.put_mark(0.3,angle=None,added_angle=0,text="\SI{45}{\degree}",pspicts=pspicts)
    no_symbol(trig.vertices)
    pspicts[2].DrawGraphs(trig,M,CM,rh,ang)


    Cp=CircleOA(  Segment(Ap,Bp).midpoint(),Ap    ).get_point(50)
    trig=Polygon(Ap,Bp,Cp)
    A=trig.vertices[0]
    B=trig.vertices[1]
    C=trig.vertices[2]
    trig.put_mark(0.2,pspicts=pspicts)
    M=trig.edges[0].midpoint()
    M.put_mark(0.2,angle=None,added_angle=180,text="\( M\)",pspicts=pspicts)
    rh=RightAngleAOB(A,C,B)
    trig.edges[0].divide_in_two(n=2,d=0.1,l=0.3,angle=45,pspicts=pspicts)

    no_symbol(trig.vertices)
    pspicts[3].DrawGraphs(trig,M,rh)


    for fig in figs:
        fig.no_figure()
        fig.conclude()
        fig.write_the_file()
