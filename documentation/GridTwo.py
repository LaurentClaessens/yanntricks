from phystricks import *
def GridTwo():
	pspict=pspicture("GridTwo")
	fig = GenericFigure("GridTwo")

	var('x')
	f = phyFunction( x**2-x-1 )
	F = Graph(f,-3,3)

	pspict.DrawGraph(F)

	pspict.grid.Dx = 2
	pspict.grid.Dy = 3
	pspict.grid.num_subX = 0
	pspict.grid.num_subY = 5

	pspict.DrawDefaultAxes()
	pspict.DrawDefaultGrid()

	# The following vertically contracts the figure with a factor 2.
	pspict.dilatation_Y(0.5)	

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
