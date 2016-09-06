# -*- coding: utf8 -*-

from __future__ import division
from phystricks import *

def RJDEoobOibtkfv():
    pspict,fig = SinglePicture("RJDEoobOibtkfv")

    # Taking the value of the LaTeX's counters "section" and "page"
    section=pspict.auxiliary_file.get_counter_value("section",default_value=1)
    page=pspict.auxiliary_file.get_counter_value("page")

    # You compute with is as normal Python float
    xmax=5/section
    pspict.dilatation_X(10/xmax)

    # Create the picture itself using the computed numbers :
    x=var('x')
    f=phyFunction(section*x).graph(0,xmax)
    f.put_mark(0.2,angle=None,added_angle=0,text="\( {} \)".format(page),pspict=pspict)


    pspict.DrawGraphs(f)
    pspict.DrawDefaultAxes()
    pspict.DrawDefaultGrid()
    pspict.comment=r"""
    \begin{enumerate}
    \item
    slope of the line is equal to the section number 
    \item
    the page number is written.
    \item
    the X dilatation makes the real picture measure 10cm
    \end{enumerate}
    """
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
