from yanntricks import *
def YOWDooyeyOJyml():
    pspict,fig = SinglePicture("YOWDooyeyOJyml")
    pspict.dilatation(0.7)
    x=var('x')
    mx=-5
    Mx=5
    f=phyFunction(x*cos(x)).graph(mx,Mx)
    g=f.derivative().graph(mx,Mx)

    g.parameters.color="red"

    pspict.axes.single_axeX.axes_unit=AxesUnit(pi,r"\pi")
    pspict.axes.single_axeX.Dx=0.5

    pspict.DrawGraphs(f,g)
    pspict.DrawDefaultAxes()
    pspict.comment="The axe is graduated with multiples of \( \pi\)"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
