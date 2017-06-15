# -*- coding: utf8 -*-
from phystricks import *
def LWVXooPyIlOKNd():
    pspict,fig = SinglePicture("LWVXooPyIlOKNd")
    pspict.dilatation(1)

    matrix=phyMatrix(3,3)
    matrix.elements[1,1].text="$\lim_{x\\to \infty}f(x)$"
    matrix.elements[1,2].text="$B$"
    matrix.elements[1,3].text="$C$"
    #matrix.elements[2,1].text=""
    matrix.elements[2,2].text="\( \int_a^b \)"
    matrix.elements[2,3].text="$\sin(x)$"
    #matrix.elements[3,1].text=""
    matrix.elements[3,2].text="$\Delta_k(A_m)$"
    matrix.elements[3,3].text="$\\vdots$"

    square=matrix.square(   (1,1) , (2,2),pspict )
    square.edges_parameters.color="red"
    h=square.edges[0].midpoint()
    h.parameters.symbol=""
    h.put_mark(0.1,angle=90,text="\( \Delta_2(A)\)",pspict=pspict)
    pspict.DrawGraphs(matrix,square,h)
    
    for el in matrix.getElements() :
        pspict.DrawGraphs(el.getTextBox(pspict))

    pspict.comment=r"""The matrix\\
\begin{equation}
    \begin{pmatrix}
        \lim_{x\to \infty}f(x)    &   B    &   C    \\
        (2,1)    &   \int_a^b    &   \sin(x)    \\
        (3,1)    &   \Delta_k(A_m)    &   \vdots
    \end{pmatrix}
\end{equation}
with \begin{enumerate}
\item a box around each element
\item a red square around the 2x2 upper left square
\item $\Delta_2(A)$ over the latter red square
\end{enumerate}
"""

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
