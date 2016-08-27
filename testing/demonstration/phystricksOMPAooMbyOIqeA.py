# -*- coding: utf8 -*-
from phystricks import *

def create_example(angleI,angleF,text,name):
    pspict,fig = SinglePicture("AngleTest"+name)

    pspict.dilatation_X(2)
    pspict.dilatation_Y(2)

    O=Point(0,0)
    Cer=Circle(O,2)
    A=Cer.get_point(angleI)
    B=Cer.get_point(angleF)
    seg1=Segment(O,A)
    seg2=Segment(O,B)

    angle=AngleAOB(A,O,B)

    angle.put_mark(text=text,pspict=pspict)

    pspict.DrawGraphs(seg1,seg2,angle)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

def OMPAooMbyOIqeA():
    create_example(0,55,"55.0","One")
    create_example(13,65,"52","Two")
