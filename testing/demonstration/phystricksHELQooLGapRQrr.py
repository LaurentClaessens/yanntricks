# -*- coding: utf8 -*-
from phystricks import *

def fun(b):
    x=var('x')
    f=sin(x)/x
    s=numerical_integral(f,0.1,b)[0]
    return s

def HELQooLGapRQrr():
    pspict,fig = SinglePicture("HELQooLGapRQrr")
    pspict.dilatation(1)

    x=var('x')
    f=NonAnalyticFunction(fun,0,10)
    f.parameters.plotpoints=300

    pspict.DrawGraphs(f)
    pspict.DrawDefaultAxes()
    pspict.comment=r"This is the graph of the function $ x\mapsto  \int_{0.1}^x\frac{ \sin(t) }{ t } dt$."
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
