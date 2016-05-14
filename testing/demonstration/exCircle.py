from phystricks import *
def exCircle():
    pspict,fig = SinglePicture("exCircle")

    circle = Circle(Point(1,1),2)
    circle.parameters.color = "magenta"

    pspict.DrawGraphs(circle)

    pspict.comment="A magenta circle of radius 2"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
