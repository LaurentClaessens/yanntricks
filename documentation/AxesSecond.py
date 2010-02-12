from phystricks import *
def AxesSecond():
	pspict=pspicture("AxesSecond")
	fig = GenericFigure("AxesSecond")

	for i in range(-10,10):
		x = float(i)/5
		pspict.DrawPoint(Point(2*x,sinh(x)),"*","")

	pspict.axes.no_graduation()
	pspict.axes.add_label_X(0.3,-45,"$x$")
	pspict.axes.add_label_Y(1.3,0,"$y=\sinh(x)$")

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
