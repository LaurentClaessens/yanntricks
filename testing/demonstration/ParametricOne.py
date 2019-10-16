from yanntricks import *
def ParametricOne():
    pspict,fig = SinglePicture("ParametricOne")

    var('x')
    f1 = phyFunction( 3*cos(x) )
    f2 = phyFunction( 2.3*cos(4.7*x))
    G = ParametricCurve(f1,f2,interval=(0,5))
    G.parameters.style = "dashed"

    pspict.DrawGraphs(G)
    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

