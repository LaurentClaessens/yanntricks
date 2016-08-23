from phystricks import *

def OnePoint():
    pspict,fig = SinglePicture("OnePoint")

    P = Point(1,1)
    P.parameters.color = "red"
    P.put_mark(dist=0.2,angle=30,text="\(P\)",pspict=pspict)
    P.put_mark(dist=0.2,angle=-90,text="\(Q\)",pspict=pspict)

    pspict.DrawGraphs(P)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
