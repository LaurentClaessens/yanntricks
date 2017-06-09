from phystricks import *
def Refraction():
    pspict,fig = SinglePicture("Refraction")
<<<<<<< HEAD
    pspict.dilatation(1)

    O=Point(0,0)
    plan=Segment(Point(-3,0),Point(3,0))
    N=AffineVector(Point(0,-2),Point(0,2))  # N est le vecteur vertical, de bas en haut

    A=Point(1,1)    
    B=Point(-2,-1)    
    a=AffineVector(A,O)
    b=AffineVector(O,B).normalize(a.length)
    a.parameters.color="red"
    b.parameters.color="blue"

    theta1=AngleAOB(a.I,O,N.F)
    theta2=AngleAOB(B,O,N.I)
    theta1.put_mark(text=r"$\theta_1$",pspict=pspict)
    theta2.put_mark(text=r"$\theta_2$",pspict=pspict)

    pspict.DrawGraphs(plan,N,theta1,theta2,a,b)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

=======

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
>>>>>>> 3d5862b035ec1a486a1cd78c2d776a68feb46039
