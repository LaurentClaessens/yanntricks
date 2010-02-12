from phystricks import *
def GridThree():
	pspict=pspicture("GridThree")
	fig = GenericFigure("GridThree")

	var('x')
	f = phyFunction(2*x*sin(x))
	F = Graph(f,-pi-0.5,pi+0.5)
	pspict.DrawGraph(F)

	pspict.grid.num_subX = 2
	pspict.grid.num_subY = 3
	pspict.grid.sub_vertical.parameters.color = "green"
	pspict.grid.sub_horizontal.parameters.color = "magenta"
	pspict.grid.main_horizontal.parameters.style = "dashed"

	pspict.DrawDefaultAxes()
	pspict.DrawDefaultGrid()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
