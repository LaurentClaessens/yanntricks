from phystricks import *
def FunctionFirst():
    pspict,fig = SinglePicture("FunctionFirst")

    var('x')
    f = phyFunction( sin(x) )
    mx = -2*pi
    Mx = 2*pi
    F = f.graph(mx,Mx)
    F.linear_plotpoints=234
    pspict.DrawGraph(F)

    #pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
