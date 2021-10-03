from yanntricks import Point
from yanntricks.src.segment import Segment
from yanntricks import SinglePicture


def FIPLooZoxgfT():
    pspict, fig = SinglePicture("FIPLooZoxgfT")

    origin = Point(0, 0)
    uX = Point(1, 0)
    uY = Point(0, 1)
    A = Point(1, 1)
    B = Point(1, -2)
    C = Point(-3, -5)
    D = Point(-7, 2)

    segments = [Segment(origin, A),
                Segment(origin, B),
                Segment(origin, C),
                Segment(origin, D),
                Segment(origin, uX),
                Segment(origin, uY),
                Segment(A, B)
                ]


    rectangles = [seg.thicker_rectangle(thickness=0.1, pspict=pspict)
                  for seg in segments]

    for seg in segments:
        pspict.DrawGraphs(seg)
    for rect in rectangles:
        pspict.DrawGraphs(rect)

    pspict.comment = "Thin rectangles around segments."
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
