from phystricks import *
def GridTwo():
    pspict,fig = SinglePicture("GridTwo")
    # The following vertically contracts the figure with a factor 2.
    pspict.dilatation_Y(0.5)    

    var('x')
    F = phyFunction( x**2-x-1 ).graph(-3,3)

    pspict.DrawGraphs(F)

    pspict.grid.Dx = 2
    pspict.grid.Dy = 3
    pspict.grid.num_subX = 0
    pspict.grid.num_subY = 5

    pspict.DrawDefaultGrid()

    pspict.axes.no_numbering()
    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
