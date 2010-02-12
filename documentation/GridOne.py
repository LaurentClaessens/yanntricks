from phystricks import *
def GridOne():
	pspict=pspicture("GridOne")
	fig = GenericFigure("GridOne")

	var('x')
	f = phyFunction( x**2-x-1 )
	F = Graph(f,-1.5,1.7)

	pspict.DrawGraph(F)

	pspict.DrawDefaultAxes()
	pspict.DrawDefaultGrid()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
