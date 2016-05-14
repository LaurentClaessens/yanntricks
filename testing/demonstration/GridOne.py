from phystricks import *
def GridOne():
    pspict,fig = SinglePicture("GridOne")

    var('x')
    F = phyFunction( x**2-x-1 ).graph(-1.5,1.7)

    pspict.DrawGraphs(F)

    pspict.DrawDefaultAxes()
    pspict.DrawDefaultGrid()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
