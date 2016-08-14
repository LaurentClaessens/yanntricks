# -*- coding: utf8 -*-
from phystricks import *
def OMZOoowEtRUuMi():
    pspict,fig = SinglePicture("OMZOoowEtRUuMi")
    pspict.dilatation(0.5)

    cone_height=7
    cylinder_radius=2
    cone_radius=3
    left_height=(cone_height*cylinder_radius)/cone_radius   # WW Thalès !           this is the height left for the flower.
    cylinder_height=cone_height-left_height

    perspective=ObliqueProjection(30,0.5)
    base_circle=Circle3D(perspective, (0,0,0),(cylinder_radius,0,0),(0,0,cylinder_radius) )
    up_circle=Circle3D(perspective, (0,cylinder_height,0),(cylinder_radius,cylinder_height,0),(0,cylinder_height,cylinder_radius) )
    base_circle.parameters.style="dashed"
    up_circle.divide=True


    S=base_circle.xmin()
    T=base_circle.xmax()
    U=up_circle.xmin()
    V=up_circle.xmax()
    h1=Segment(U,S)
    h2=Segment(V,T)

    A=Point(0,0)
    B=Point(cone_radius,0)
    C=Point(0,cone_height)
    D=Point(0,cylinder_height)
    E=Point(cylinder_radius,cylinder_height)

    F=perspective.point(0,cylinder_height,0)

    pspict.comment=r"""A cylinder is drawn. The above circle is half-dashed while the one on the basis is dashed."""
    pspict.DrawGraphs(base_circle,up_circle,h1,h2,F)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
