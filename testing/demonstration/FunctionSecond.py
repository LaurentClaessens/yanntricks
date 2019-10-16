from yanntricks import *
def FunctionSecond():
    pspict,fig = SinglePicture("FunctionSecond")

    var('x')
    f = phyFunction( log(x) )
    mx = 0.1
    Mx = 10
    F = f.graph(mx,Mx)
    G = f.graph(mx,Mx)
    F.parameters.color = "red"
    F.wave(0.3,0.1)
    F.parameters.style = "dashed"
    pspict.DrawGraphs(F)
    pspict.DrawGraphs(G)

    pspict.axes.no_numbering()
    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
