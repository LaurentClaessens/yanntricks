from yanntricks import *
def FunctionFive():
    pspict,fig = SinglePicture("FunctionFive")

    var('x')
    mx = -5
    Mx = 5
    f = phyFunction( x*sin(x) ).graph(mx,Mx)

    points = f.getRegularLengthPoints(mx,Mx,1.5)

    pspict.DrawGraphs(f)
    for i in range(0,len(points)):
        P = points[i]
        P.put_mark(0.2,None,"$P_{%s}$"%str(i),pspict=pspict)
        pspict.DrawGraphs(P)

    pspict.DrawDefaultAxes()
    pspict.comment=r"""
    \begin{itemize}
    \item 
            Points are regularly spaced with respect to the arc length
            \item 
            Marks are on the exterior normal.
    \end{itemize}"""

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
