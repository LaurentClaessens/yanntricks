# -*- coding: utf8 -*-

# This is the example you also have in the README.md

from phystricks import *
def VSJOooJXAwbVEt():
    pspict,fig = SinglePicture("VSJOooJXAwbVEt")
    pspict.dilatation(1)

    O=Point(0,0)

    # center, radius
    circle=Circle( O,2 ) 

    # Points are parametrized by their angle (degree)
    A=circle.get_point(130)
    B=circle.get_point(220)
    tg=circle.get_tangent_vector(30)  

    # dist : the distance between the circle and the mark.
    # text : the LaTeX code that will be placed there.
    A.put_mark(dist=0.3,text="$\lim_{s}(F\circ\gamma')$",pspict=pspict)
    B.put_mark(dist=0.3,text="$K$",pspict=pspict)

    pspict.DrawGraphs(circle,A,tg,B)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
