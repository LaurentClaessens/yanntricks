from phystricks import *
def exCircleTwo():
    pspict,fig = SinglePicture("exCircleTwo")

    circle = Circle(Point(0,0),1.5)
    circle.style = "dotted"
    circle.angleI = 20
    circle.angleF = 100

    for angle in [10,20,50,130,300,350] :
        P = circle.get_point(angle)
        P.put_mark(0.2,angle=None,text="$P_{%s}$"%str(angle),automatic_place=(pspict,""))
        pspict.DrawGraphs(P)

    pspict.DrawGraphs(circle)
    pspict.DrawDefaultAxes()

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
