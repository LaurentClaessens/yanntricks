from yanntricks import *
def Refraction():
    pspict,fig = SinglePicture("Refraction")
    O=Point(0,0)
    A=Point(1,1)    
    C=Point(0,2)

    s1=Segment(A,O)
    s2=Segment(O,C)
    theta1=AngleAOB(A,O,C)
    theta1.put_mark(text=r"$\theta_1$",pspict=pspict)

    pspict.DrawGraphs(theta1,s1,s2)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
