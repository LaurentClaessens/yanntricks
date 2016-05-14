from phystricks import *
def GridThree():
    pspict,fig = SinglePicture("GridThree")

    var('x')
    F = phyFunction(2*x*sin(x)).graph(-pi-0.5,pi+0.5)
    pspict.DrawGraphs(F)

    pspict.grid.num_subX = 2
    pspict.grid.num_subY = 3
    pspict.grid.sub_vertical.parameters.color = "green"
    pspict.grid.sub_horizontal.parameters.color = "magenta"
    pspict.grid.main_horizontal.parameters.style = "dashed"

    pspict.DrawDefaultAxes()
    pspict.DrawDefaultGrid()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
