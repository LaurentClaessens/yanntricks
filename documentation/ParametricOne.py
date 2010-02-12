from phystricks import *
def ParametricOne():
	pspict=pspicture("ParametricOne")
	fig = GenericFigure("ParametricOne")

	var('x')
	f1 = phyFunction( 3*cos(x) )
	f2 = phyFunction( 2.3*cos(4.7*x))
	curve = ParametricCurve(f1,f2)
	G = Graph(curve,0,5)
	G.parameters.style = "dashed"

	pspict.DrawGraph(G)

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()

