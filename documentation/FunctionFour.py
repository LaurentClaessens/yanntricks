from phystricks import *
def FunctionFour():
	pspict=pspicture("FunctionFour")
	fig = GenericFigure("FunctionFour")

	var('x')
	f = phyFunction( x*sin(x) )
	mx = -5
	Mx = 5
	F = Graph(f,mx,Mx)
	points = []
	for i in range(mx,Mx) :
		points.append(Graph(f.get_point(i)))

	pspict.DrawGraph(F)
	for i in range(0,len(points)):
		points[i].mark(0.3,90,"$P_{%s}$"%str(i))
		pspict.DrawGraph(points[i])

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
