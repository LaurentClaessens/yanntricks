from phystricks import *
def MarkOnPoint():
	pspict=pspicture("MarkOnPoint")
	fig = GenericFigure("MarkOnPoint")

	p = Point(0,0)
	P = Graph(p)
	P.parameters.color = "blue"
	P.mark(0.3,45,"$f_i$")

	q = Point(1,1)
	Q = Graph(q)
	Q.mark(0.3,180,"$q$")
	Q.parameters.symbol = "diamond"

	pspict.DrawGraph(P)
	pspict.DrawGraph(Q)

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()

