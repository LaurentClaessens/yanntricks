from sage.all import sqrt
from yanntricks import *


def IllusionNHwEtp():
    pspict, fig = SinglePicture("IllusionNHwEtp")
    pspict.dilatation(0.7)

    perspective = ObliqueProjection(45, sqrt(2)/2)

    l = 2
    P = (0, 0)
    cubesP = []
    cubesL = []
    cubesH = []
    profondeur = 7
    longueur = 4
    hauteur = 4
    for i in range(0, profondeur):
        cubesP.append(perspective.cuboid(P, l, l, l))
        Q = cubesP[-1].c2[3]
        P = (Q.x, Q.y)
    P = (0, 0)
    for i in range(0, longueur):
        cubesL.append(perspective.cuboid(P, l, l, l))
        Q = cubesL[-1].c1[2]
        P = (Q.x, Q.y)
    for i in range(0, hauteur):
        cubesH.append(perspective.cuboid(P, l, l, l))
        Q = cubesH[-1].c1[0]
        P = (Q.x, Q.y)
    cubesP.reverse()    # Ainsi les plus éloignés sont tracés en premier.
    for i, cub in enumerate(cubesP):
        cub.make_opaque()
        pspict.DrawGraphs(cub)
    for i, cub in enumerate(cubesL):
        cub.make_opaque()
        pspict.DrawGraphs(cub)
    for i, cub in enumerate(cubesH):
        cub.make_opaque()
        pspict.DrawGraphs(cub)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
