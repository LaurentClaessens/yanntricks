
def fun(b):
    x=var('x')
    f=sin(x)/x
    s=numerical_integral(f,0.1,b)[0]
    return s

def MyPictureName():
    pspict,fig = SinglePicture("MyPictureName")
    f=phyFunction(fun).graph(0,10)

    pspict.DrawGraphs(f)
