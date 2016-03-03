# -*- coding: utf8 -*-
from phystricks import *
def QRXCooUmnlhkvh():
    pspict,fig = SinglePicture("QRXCooUmnlhkvh")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(1)

    x=var('x')
    P=Point(1,3)

    P.put_mark(0.2,angle=45,added_angle=0,text="\(  e^{\int_{\Omega}\gamma}  \)",automatic_place=(pspict,"corner"))
    bb=P.mark.bounding_box(pspict)
    pspict.DrawGraphs(P,bb)

    pspict.comment="The bounding box of the text is drawn and its corner almost touch the point"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
