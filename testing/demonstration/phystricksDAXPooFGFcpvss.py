# -*- coding: utf8 -*-
from phystricks import *
def DAXPooFGFcpvss():
    pspicts,fig = MultiplePictures("DAXPooFGFcpvss",3)
    pspicts[0].mother.caption="<+caption1+>"
    pspicts[1].mother.caption="<+caption2+>"
    pspicts[2].mother.caption="<+caption3+>"

    for psp in pspicts:
        psp.dilatation_X(1)
        psp.dilatation_Y(1)

    <+Définition des objets+>

    for psp in pspicts:
        psp.DrawDefaultAxes()

    fig.conclude()
    fig.write_the_file()

