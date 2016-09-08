from phystricks import *
def GestionRepere():
    pspict,fig = SinglePicture("GestionRepere")

    P = Point(-2,-2)
    Q = Point(5,5)
    P.parameters.symbol = "none"
    Q.parameters.symbol = "none"

    pspict.DrawGraphs(P,Q)

    pspict.grid.num_subX = 0
    pspict.grid.num_subY = 0
    pspict.grid.main_vertical.parameters.style = "dotted"
    pspict.grid.main_horizontal.parameters.style = "dotted"

    pspict.axes.no_graduation()

    pspict.DrawDefaultGrid()
    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
