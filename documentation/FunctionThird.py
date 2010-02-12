from phystricks import *
def FunctionThird():
	pspict=pspicture("FunctionThird")
	fig = GenericFigure("FunctionThird")

	var('x')
	f = phyFunction( x*cos(x) )
	mx = -5
	Mx = 5
	F = Graph(f,mx,Mx)
	G = Graph(f.derive(),mx,Mx)
	G.parameters.color = "red"
	pspict.DrawGraph(F)
	pspict.DrawGraph(G)

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
