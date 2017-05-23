from phystricks import *
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
    pspict.dilatation(1)
    fig.conclude()
    fig.write_the_file()
