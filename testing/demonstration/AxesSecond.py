from phystricks import *
def AxesSecond():
    pspict,fig = SinglePicture("AxesSecond")

    for i in range(-10,10):
        x = float(i)/5
        P=Point(2*x,sinh(x))
        pspict.DrawGraph(P)

    pspict.axes.no_graduation()
    pspict.axes.single_axeX.put_mark(0.3,angle=-45,text="\( x\)",automatic_place=(pspict,""))
    pspict.axes.single_axeY.put_mark(0.3,angle=0,text="\( y=\sinh(x)\)",automatic_place=(pspict,""))

    pspict.DrawDefaultAxes()
    pspict.comment="The marks on the axes : \( x\) and \( y=\sinh(x)\)."

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
