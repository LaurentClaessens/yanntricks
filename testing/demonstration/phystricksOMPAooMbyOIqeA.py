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
    pspicts.append(create_example(angleI=0,angleF=55,text="55.0",name="One",dist=None))
    pspicts.append(create_example(angleI=13,angleF=65,text="880",name="Two"))
    pspicts.append(create_example(angleI=80,angleF=110,text="\( 30^o\)",name="Three",dist=None))
    pspicts.append(create_example(angleI=90,angleF=110,text="\( mMó\)",name="15",dist=None))
    pspicts.append(create_example(angleI=123,angleF=170,text="\( 47\)",name="Four",dist=None))
    pspicts.append(create_example(angleI=150,angleF=180,text="\( 333\)",name="Five",dist=None))
    pspicts.append(create_example(angleI=160,angleF=223,text="\( \int_A40mmmm\)",name="Six",dist=None))
    pspicts.append(create_example(angleI=180,angleF=250,text="\(who\)",name="Seven",dist=None))
    pspicts.append(create_example(angleI=200,angleF=255,text="$\sigma$",name="Eight",dist=None))
    pspicts.append(create_example(angleI=200,angleF=270,text="FloO",name="16",dist=None))
    pspicts.append(create_example(angleI=250,angleF=350,text="\(100\)",name="Nine",dist=None))
    pspicts.append(create_example(angleI=270,angleF=290,text="\(20\)",name="Eleven",dist=None))
    pspicts.append(create_example(angleI=300,angleF=360,text="60",name="14",dist=None))
    pspicts.append(create_example(angleI=320,angleF=10,text="\(60\)",name="Ten",dist=None))
    pspicts.append(create_example(angleI=290,angleF=331,text="\( 12\)",name="Twelve",dist=None))
    pspicts.append(create_example(angleI=360,angleF=25,text="ÈÉç",name="13",dist=None))

    psps,fig = MultiplePictures("OMPAooMbyOIqeA",pspicts=pspicts)

    for psp in pspicts :
        psp.mother.caption="The angle measure has to be placed correctly"

    fig.conclude()
    fig.write_the_file()
