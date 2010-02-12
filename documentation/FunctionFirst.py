from phystricks import *
def FunctionFirst():
	pspict=pspicture("FunctionFirst")
	fig = GenericFigure("FunctionFirst")

	var('x')
	f = phyFunction( sin(x) )
	mx = -2*pi
	Mx = 2*pi
	F = Graph(f,mx,Mx)
	pspict.DrawGraph(F)

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
