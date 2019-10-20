from yanntricks import *
def FunctionFour():
    pspict,fig = SinglePicture("FunctionFour")

    var('x')
    mx = -5
    Mx = 5
    f = phyFunction( x*sin(x) ).graph(mx,Mx)
    points = []
    for i in range(mx,Mx) :
        points.append(f.get_point(i))

    pspict.DrawGraphs(f)
    for P in points :
        P.put_mark(0.2,text="$P_{{{}}}$".format(P.x),pspict=pspict)
        pspict.DrawGraphs(P)

    pspict.DrawDefaultAxes()
    pspict.comment="Points are regularly spaced with respect to abscisses."

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
