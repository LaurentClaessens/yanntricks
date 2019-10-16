from yanntricks import *
def exCircleThree():
    pspict,fig = SinglePicture("exCircleThree")

    circle = Circle(Point(0,0),1.5)

    circle.angleI = 45
    circle.angleF = 380
    circle.wave(0.1,0.1)
    circle.parameters.color = "green"

    circleB = Circle(Point(0,0),1.5)
    circleB.angleI = circle.angleF-360
    circleB.angleF = circle.angleI
    circleB.wave(circle.waviness.dx,circle.waviness.dy)
    circleB.parameters.color = "red"

    pspict.DrawGraphs(circle,circleB)
    pspict.DrawDefaultAxes()
    pspict.comment="A large green wavy part and a small red wavy part."

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
