from phystricks import *
def FunctionSecond():
	pspict=pspicture("FunctionSecond")
	fig = GenericFigure("FunctionSecond")

	var('x')
	f = phyFunction( log(x) )
	mx = 0.1
	Mx = 10
	F = Graph(f,mx,Mx)
	G = Graph(f,mx,Mx)
	F.parameters.color = "red"
	F.wave(0.3,0.1)
	F.parameters.style = "dashed"
	pspict.DrawGraph(F)
	pspict.DrawGraph(G)

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
