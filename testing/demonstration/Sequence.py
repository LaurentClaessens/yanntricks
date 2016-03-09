from phystricks import *
def Sequence():
    pspict,fig = SinglePicture("Sequence")

    nmax = 10
    for i in range(1,nmax):
        x = i
        y = ((-1)**i)/float(i)
        P = Point(x,y)
        P.put_mark(0.3,90*(-1)**i,"$P_{%s}$"%(str(i)),automatic_place=(pspict,""))
        pspict.DrawGraph(P)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
