from phystricks import *
def MarkOnPoint():
    pspict,fig = SinglePicture("MarkOnPoint")

    P = Point(0,0)
    P.parameters.color = "blue"
    P.put_mark(0.3,45,"$f_i$",automatic_place=(pspict,""))

    Q = Point(1,1)
    Q.put_mark(0.3,180,"$q$",automatic_place=(pspict,""))
    Q.parameters.symbol = "diamond"

    pspict.DrawGraphs(P)
    pspict.DrawGraphs(Q)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

