# -*- coding: utf8 -*-
from yanntricks import *
def XBAUooFtMWukKr():
    pspicts,figs = IndependentPictures("XBAUooFtMWukKr",3)

    for psp in pspicts:
        psp.dilatation(1)

    O=Point(0,0)
    r=1

    tartes=[]
    tartes.append(FractionPieDiagram(O,r,4,7))
    tartes.append(FractionPieDiagram(O,r,4,28))
    tartes.append(FractionPieDiagram(O,r,1,7))

    for i in range(0,len(pspicts)):
        pspicts[i].DrawGraphs(tartes[i])

    pspicts[0].comment="A pie for 4/7"
    pspicts[1].comment="A pie for 4/28"
    pspicts[2].comment="A pie for 1/7"

    for fig in figs:
        fig.no_figure()
        fig.conclude()
        fig.write_the_file()
