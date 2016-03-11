from phystricks import *
def FunctionFour():
    pspict,fig = SinglePicture("FunctionFour")

    var('x')
    mx = -5
    Mx = 5
    f = phyFunction( x*sin(x) ).graph(mx,Mx)
    points = []
    for i in range(mx,Mx) :
        points.append(f.get_point(i))

    pspict.DrawGraph(f)
    for i in range(0,len(points)):
        points[i].put_mark(0.2,None,"$P_{%s}$"%str(i),automatic_place=(pspict,""))
        pspict.DrawGraph(points[i])

    pspict.DrawDefaultAxes()
    pspict.comment="Points are regularly spaced with respect to abscisses."

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()