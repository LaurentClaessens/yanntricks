from phystricks import *
def FunctionFour():
    pspict,fig = SinglePicture("FunctionFour")

    var('x')
    f = phyFunction( x*sin(x) )
    mx = -5
    Mx = 5
    F=f.graph(mx,Mx)
    points = []
    for i in range(mx,Mx) :
        points.append(f.get_point(i))

    pspict.DrawGraph(F)
    for i in range(0,len(points)):
        points[i].put_mark(0.3,90,"$P_{%s}$"%str(i),automatic_place=(pspict,""))
        pspict.DrawGraph(points[i])

    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
