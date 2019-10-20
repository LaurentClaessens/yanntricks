# -*- coding: utf8 -*-
from yanntricks import *
def UREIooqNGBXtHg():
    pspict,fig = SinglePicture("UREIooqNGBXtHg")
    pspict.dilatation(0.8)

    A=Point(1,2)
    B=Point(-1,2)
    C=Point(3,0)
    O=Point(0,0)

    A.put_mark(0.2,angle=None,text="\( A\)",pspict=pspict)
    B.put_mark(0.2,angle=None,text="\( B\)",pspict=pspict)
    C.put_mark(0.2,angle=-90,text="\( C\)",pspict=pspict)
    O.put_mark(0.2,angle=225,text="\( O\)",pspict=pspict)

    pspict.math_BB.append( Point(4,4),pspict=pspict )

    pspict.DrawGraphs(A,B,C,O)
    pspict.DrawDefaultGrid()
    pspict.comment=r"""
    \begin{enumerate}
    \item
    The mark of the point \( A\)  is on the line \( OA\),
    \item
    the mark on $B$ on the line $OB$, 
    \item
    the mark on $C$ is at angle $-90$ degree
    \item
    and the one of \( O\) is at angle \( 225\) degree
    \end{enumerate}
    """
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
