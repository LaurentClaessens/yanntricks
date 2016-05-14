from phystricks import *
def VectorOne():
    pspict,fig = SinglePicture("VectorOne")

    O = Point(0,0)
    A = Point(1,1)
    B = Point(-4,-1)
    C = Point(-2,3)

    v = []
    v.append(AffineVector(O,A).fix_size(3))
    v.append(AffineVector(A,C))
    v.append(AffineVector(B,C))
    v.append( v[1].rotation(30).dilatation(0.5) )
    v.append( v[1].rotation(-30) )
    v.append( v[1].orthogonal() )

    v[1].put_mark(0.3,45,"$v$",automatic_place=(pspict,""))
    v[1].parameters.color="brown"
    v[2].parameters.color="red"
    v[2].parameters.style = "dotted"
    v[3].parameters.color=v[1].parameters.color    
    v[4].parameters.style = "dashed"
    v[4].parameters.color=v[1].parameters.color
    v[5].parameters.color=v[1].parameters.color

    for vect in v:
        pspict.DrawGraphs(vect)

    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
