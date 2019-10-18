from yanntricks import *
def FunctionThird():
    pspict,fig = SinglePicture("FunctionThird")
    pspict.dilatation(0.7)

    x=var('x')
    f = phyFunction( x*cos(x) )
    mx = -5
    Mx = 5
    F = f.graph(mx,Mx)
    G = f.derivative().graph(mx,Mx)
    G.parameters.color = "red"
    pspict.DrawGraphs(F,G)

    pspict.DrawDefaultAxes()
    pspict.comment="The function \( x\cos(x)\) (blue) and its derivative (red)."

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
