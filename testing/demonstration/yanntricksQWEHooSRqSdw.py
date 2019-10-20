from yanntricks import *
def QWEHooSRqSdw():
    pspict,fig = SinglePicture("QWEHooSRqSdw")
    pspict.dilatation(3)

    A=Point(0,0)
    O=Point(0,2)
    B=Point(3,0)

    s1=Segment(A,O)
    s2=Segment(O,B)
    angle=AngleAOB(A,O,B,r=0.7)
    angle.put_mark(text="\( c\)",pspict=pspict)

    pspict.DrawGraphs(angle,s1,s2)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
