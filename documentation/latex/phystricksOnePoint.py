from phystricks import *

def OnePoint():
    pspict,fig = SinglePicture("OnePoint")

    P = Point(1,1)
    P.parameters.color = "red"
    P.put_mark(dist=0.2,angle=30,text="\(P\)",automatic_place=(pspict,""))
    P.put_mark(dist=0.2,angle=-90,text="\(Q\)",automatic_place=(pspict,""))

    pspict.DrawGraph(P)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
