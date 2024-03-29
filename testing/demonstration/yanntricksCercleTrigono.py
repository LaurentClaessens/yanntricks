from yanntricks import *
def CercleTrigono():
    pspict,fig = SinglePicture("CercleTrigono")
    
    O=Point(0,0)
    Cercle=Circle(O,2)
    alpha=30
    P=Cercle.get_point(alpha)
    P.put_mark(0.3,P.advised_mark_angle(pspict),"$P$",pspict=pspict)
    P.parameters.symbol=""
    vecteur=AffineVector(O,P)

    #vecteur.parameters.color="blue"
    vecteur.parameters.color="brown"

    C=P.projection(pspict.axes.single_axeX)
    S=P.projection(pspict.axes.single_axeY)
    pc=Segment(P,C)
    ps=Segment(P,S)
    pc.parameters.color="brown"
    pc.parameters.style="dotted"
    ps.parameters=pc.parameters

    angle=AngleAOB(C,O,P,0.4)
    angle.put_mark(text=r"$\theta$",pspict=pspict)

    pspict.DrawGraphs(Cercle,pc,ps,S,C,vecteur,angle,P)
    pspict.axes.no_graduation()
    pspict.DrawDefaultAxes()
    fig.conclude()
    fig.write_the_file()

