from yanntricks import *

def OnePoint():
    pspict,fig = SinglePicture("OnePoint")

    ##################### The main lines are here
    P = Point(1,1)
    P.parameters.color = "red"
    pspict.DrawGraphs(P)
    ########################

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
