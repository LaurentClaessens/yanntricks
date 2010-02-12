from phystricks import *
def exCircleTwo():
	pspict=pspicture("exCircleTwo")
	fig = GenericFigure("exCircleTwo")

	circle = Circle(Point(0,0),1.5)
	C = Graph(circle)
	C.style = "dotted"
	C.angleI = 20
	C.angleF = 100

	for angle in [10,20,50,130,300,350] :
		point = circle.get_point(angle)
		P = Graph(circle.get_point(angle))
		P.mark(0.5,angle,"$P_{%s}$"%str(angle))
		pspict.DrawGraph(P)

	pspict.DrawGraph(C)
	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
