from phystricks import *
def exCircle():
	pspict=pspicture("exCircle")
	fig = GenericFigure("exCircle")

	circle = Circle(Point(1,1),2)
	C = Graph(circle)
	C.parameters.color = "magenta"

	pspict.DrawGraph(C)

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
