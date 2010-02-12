from phystricks import *
def GestionRepere():
	pspict=pspicture("GestionRepere")
	fig = GenericFigure("GestionRepere")

	P = Graph(Point(-2,-2))
	Q = Graph(Point(5,5))
	P.parameters.symbol = "none"
	Q.parameters.symbol = "none"

	pspict.DrawGraph(P)
	pspict.DrawGraph(Q)

	pspict.grid.num_subX = 0
	pspict.grid.num_subY = 0
	pspict.grid.main_vertical.parameters.style = "dotted"
	pspict.grid.main_horizontal.parameters.style = "dotted"

	pspict.axes.no_graduation()

	pspict.DrawDefaultAxes()
	pspict.DrawDefaultGrid()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
