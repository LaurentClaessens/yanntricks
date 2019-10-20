# -*- coding: utf8 -*-

from __future__ import division
from sage.all import ceil
from yanntricks import *

def BHESoofmkTbbZR():
    pspict,fig = SinglePicture("BHESoofmkTbbZR")
    pspict.dilatation_X(15)
    pspict.dilatation_Y(4)

    x=var('x')
    eps=0.02/pspict.xunit  # We start drawing at visual 0.02

    f=phyFunction(sin(1/x)).graph(eps,1)
    f.linear_plotpoints=500     # 500 points linearly spaced on the domain

    # We ask to compute some more points, but chosen ones.
    # These are the values of 'x' for which f(x)=1,-1,0.
    k_max=ceil(2/(eps*pi))
    f.added_plotpoints=[ 2/(k*pi) for k in range(1,k_max)  ]

    pspict.DrawGraphs(f)
    pspict.DrawDefaultAxes()
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
