# -*- coding: utf8 -*-
from yanntricks import *
def OYBTooNUcJLzDH():
    pspict,fig = SinglePicture("OYBTooNUcJLzDH")
    pspict.dilatation_X(2)
    pspict.dilatation_Y(0.3)

    x=var('x')
    mx=0.5
    Mx=3.5
    f = phyFunction(3*(x-2)**2+3).graph(mx,Mx)
    f.put_mark(0.3,text="f(x)=foo",pspict=pspict)

    A=Point(1.08712907082472,0)
    B=Point(2.91287,0)

    A.put_mark(0.3,-90,"$a$",pspict=pspict)
    B.put_mark(0.3,-90,"$b$",pspict=pspict)

    pspict.DrawGraphs(f,A,B)
    pspict.axes.no_graduation()
    pspict.DrawDefaultAxes()
    pspict.comment="""
    \\begin{itemize}
    \item Axes do not intersect because point (0,0) is not on the picture.
    \item Marks on points \( a\) and \( b\) well positioned.
    \item It is written «f(x)=foo» on the function.
    \\end{itemize}
    """
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

