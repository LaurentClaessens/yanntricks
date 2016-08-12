from phystricks import *
def Lines():
    pspict,fig = SinglePicture("Lines")

    A = Point(1,1)
    B = Point(5,2)
    C = Point(2,5)
    A.put_mark(0.3,180,"$A$",pspict=pspict)
    B.put_mark(0.3,0,"$B$",pspict=pspict)
    C.put_mark(0.3,180,"$C$",pspict=pspict)
    pspict.DrawGraphs(A,B,C)

    S1 = Segment(A,B)
    S2 = Segment(C,Point(3,-1))

    S2.parameters.color = "red"
    S2.parameters.style = "dotted"
    pspict.DrawGraphs(S1,S2)

    P = Intersection(S1,S2)[0]
    P.put_mark(0.3,-45,"$P$",pspict=pspict)

    S3 = Segment(A,C)
    S4 = Segment(A,C)
    S3.wave(0.2,0.1)
    S3.parameters.color = "cyan"
    S4.parameters.color = "blue"
    pspict.DrawGraphs(S3,S4)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
