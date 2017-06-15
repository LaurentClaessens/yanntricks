# -*- coding: utf8 -*-
from phystricks import *

def Phi(f):
    prim=f.integrate(x)
    return 1+prim(x)-prim(0)


def XOLBooGcrjiwoU():
    pspict,fig = SinglePicture("XOLBooGcrjiwoU")
    pspict.dilatation_X(0.6)
    pspict.dilatation_Y(300)

    x=var('x')
    f=sin(x)

    for i in range(1,30):
        f=Phi(f)

    g=phyFunction(f(x)-exp(x)).graph(-10,10)

    a=10
    na=numerical_approx(a)

    def foo(x):
        return f(x)-exp(x)
    print(numerical_approx(f(na)))
    print(numerical_approx(exp(na)))
    print(numerical_approx(f(na)-exp(na),prec=30))


    pspict.DrawGraphs(g)
    pspict.axes.single_axeX.Dx=2
    pspict.axes.single_axeY.Dx=0.005
    pspict.DrawDefaultAxes()
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

