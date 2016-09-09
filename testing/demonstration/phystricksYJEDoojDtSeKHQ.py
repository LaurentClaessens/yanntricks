# -*- coding: utf8 -*-
from phystricks import *
def YJEDoojDtSeKHQ():
    """
    Copied from examssepti from mazhe
    """
    pspict,fig = SinglePicture("YJEDoojDtSeKHQ")
    pspict.dilatation(3)

    a=-1
    b=0.5
    x=var('x')
    f1=phyFunction(x**2).graph(a,b)
    f2=phyFunction(sqrt(1-x**2)).graph(a,b)

    f1.parameters.color="red"

    x0=sqrt(sqrt(5)-1)/2*sqrt(2)
    I=f1.get_point(-x0)
    J=Point(-x0,0)
    J.put_mark(0.1,-90,"\( -x_0\)",pspict=pspict,position="N")

    vert=Segment(I,J)
    vert.parameters.style="dotted"

    surface=SurfaceBetweenFunctions(f1,f2,mx=-x0,Mx=b)
    surface.parameters.hatched()
    surface.Fsegment.parameters.style="dotted"
    surface.Fsegment.parameters.color="green"
    surface.parameters.hatch.color="cyan"

    pspict.DrawGraphs(vert,surface,f1,f2,I,J)
    pspict.DrawDefaultAxes()
    pspict.comment=r"""\begin{itemize}
    \item one line in blue, one in red
    \item at the right : dotted green 
    \item the surface is hatched in cyan
    \end{itemize}
    """
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
