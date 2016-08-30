# -*- coding: utf8 -*-
from phystricks import *

def create_example(angleI,angleF,text,name,dist=None):
    pspict,fig = SinglePicture("AngleTest"+name)

    O=Point(0,0)
    Cer=Circle(O,2)
    A=Cer.get_point(angleI)
    B=Cer.get_point(angleF)
    seg1=Segment(O,A)
    seg2=Segment(O,B)

    angle=AngleAOB(A,O,B)

    angle.put_mark(dist=dist,text=text,pspict=pspict)

    pspict.DrawGraphs(seg1,seg2,angle)
    return pspict

def OMPAooMbyOIqeA():
    pspicts=[]
    #pspicts.append(create_example(angleI=0,angleF=55,text="55.0",name="One",dist=0.4))
    #pspicts.append(create_example(angleI=13,angleF=65,text="880",name="Two"))
    #pspicts.append(create_example(angleI=80,angleF=110,text="\( 30^o\)",name="Three",dist=0.7))
    #pspicts.append(create_example(angleI=123,angleF=170,text="\( 47\)",name="Four",dist=None))
    pspicts.append(create_example(angleI=160,angleF=200,text="\( \int_A40xx\)",name="Six",dist=None))
    pspicts.append(create_example(angleI=150,angleF=180,text="\( 333\)",name="Five",dist=0.5))

    psps,fig = MultiplePictures("OMPAooMbyOIqeA",pspicts=pspicts)

    for psp in pspicts :
        psp.mother.caption="The angle measure has to be placed correctly"

    fig.conclude()
    fig.write_the_file()
