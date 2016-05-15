# -*- coding: utf8 -*-
from phystricks import *
def LWVXooPyIlOKNd():
    pspict,fig = SinglePicture("LWVXooPyIlOKNd")
    pspict.dilatation(1)

    matrix=phyMatrix(3,3)
    matrix.elements[1,1].text="A"
    matrix.elements[1,2].text="B"
    matrix.elements[1,3].text="C"
    #matrix.elements[2,1].text=""
    matrix.elements[2,2].text="\( \int_a^b \)"
    matrix.elements[2,3].text="\sin(x)"
    #matrix.elements[3,1].text=""
    matrix.elements[3,2].text="\Delta_k(A_m)"
    matrix.elements[3,3].text="\\vdots"

    print(matrix.getColumnWidth(1,pspict))

    pspict.DrawGraphs(matrix)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
