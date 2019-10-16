# -*- coding: utf8 -*-
from yanntricks import *
def QEFQoomlfmOQTM():
    pspicts,figs = IndependentPictures("QEFQoomlfmOQTM",3)

    for psp in pspicts:
        psp.dilatation(1)

    P=Point(0,0)
    P.put_mark(0.2,45,"P",pspicts=[pspicts[0],pspicts[2]])

    for psp in pspicts:
        psp.DrawGraphs(P)

    pspicts[0].comment="With the mark."
    pspicts[1].comment="Without the mark."
    pspicts[2].comment="With the mark."

    for fig in figs:
        fig.no_figure()
        fig.conclude()
        fig.write_the_file()

# Une marque qui est sur deux figures, mais pas sur la troisième.
