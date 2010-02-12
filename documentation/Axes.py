from phystricks import *
def Axes():
	pspict=pspicture("Axes")
	fig = GenericFigure("Axes")

	p = Point(-4,-2)
	L = Segment( Point(0,0),Point(1.6,3) )

	P = Graph(p)
	P.mark(0.3,135,"$P$")
	pspict.DrawGraph(P)
	S = Graph(L)
	S.parameters.color = "brown"
	pspict.DrawGraph(S)

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()


