from yanntricks import *
from yanntricks.src.Utilities import point_to_box_intersection

def BOVAooIlzgFQpG():
    pspict,fig = SinglePicture("BOVAooIlzgFQpG")
    pspict.dilatation(1)


    P=Point(0,0)
    box=BoundingBox(xmin=-2.0719775,xmax=-0.8437425000000001,ymin=-0.1148125,ymax=0.1148125)
    inter=point_to_box_intersection(P,box,pspict) 

    for Q in inter:
        print(Q)

    pspict.DrawDefaultAxes()
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
