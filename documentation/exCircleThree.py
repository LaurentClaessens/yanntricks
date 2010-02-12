from phystricks import *
def exCircleThree():
	pspict=pspicture("exCircleThree")
	fig = GenericFigure("exCircleThree")

	circle = Circle(Point(0,0),1.5)
	C = Graph(circle)
	C.angleI = 45
	C.angleF = 380
	C.wave(0.1,0.1)
	C.color = "green"
	D = Graph(circle)
	D.angleI = C.angleF-360
	D.angleF = C.angleI
	D.wave(C.waviness.dx,C.waviness.dy)
	D.color = "red"

	pspict.DrawGraph(C)
	pspict.DrawGraph(D)
	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
