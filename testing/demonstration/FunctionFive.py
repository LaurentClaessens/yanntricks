from phystricks import *
def FunctionFive():
    pspict,fig = SinglePicture("FunctionFive")

    var('x')
    f = phyFunction( x*sin(x) )
    mx = -5
    Mx = 5
    F=f.graph(mx,Mx)

    points = f.get_regular_points(mx,Mx,1.5)

    pspict.DrawGraph(F)
    for i in range(0,len(points)):
        P = points[i]
        P.put_mark(0.3,90,"$P_{%s}$"%str(i),automatic_place=(pspict,""))
        pspict.DrawGraph(P)

    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
