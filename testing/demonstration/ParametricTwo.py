from phystricks import *
def ParametricTwo():
    pspict,fig = SinglePicture("ParametricTwo")

    var('x')
    f1 = phyFunction( x*sin(x) )
    f2 = phyFunction( x )
    f3 = phyFunction( x*cos(x) )

    llI = 0
    llF = 5
    wl = 0.1
    amplitude = 0.1
    F1 = ParametricCurve(f1,f2,interval=(llI,llF))
    G1 = ParametricCurve(f1,f2,interval=(llI,llF))
    F2 = ParametricCurve(f1,f3,interval=(llI,llF))

    F1.parameters.color = "brown"
    G1.parameters.color = "magenta"
    G1.wave(wl,amplitude)

    for ll in F2.get_regular_parameter(llI,llF,2):
        v1 = F2.get_tangent_vector(ll)
        v2 = F2.get_normal_vector(ll)
        pspict.DrawGraphs(v1,v2)

    pspict.DrawGraphs(F1,G1,F2)
    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

