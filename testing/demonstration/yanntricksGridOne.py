from yanntricks import *
def GridOne():
    pspict,fig = SinglePicture("GridOne")

    x=var('x')
    f = phyFunction( x**2-x-1 )
    F=f.graph(-1.5,1.7)

    pspict.DrawGraphs(F)

    pspict.DrawDefaultAxes()
    pspict.DrawDefaultGrid()

    fig.conclude()
    fig.write_the_file()
