from phystricks import *
def FunctionFive():
	pspict=pspicture("FunctionFive")
	fig = GenericFigure("FunctionFive")

	var('x')
	f = phyFunction( x*sin(x) )
	mx = -5
	Mx = 5
	F = Graph(f,mx,Mx)

	points = f.get_regular_points(mx,Mx,1.5)

	pspict.DrawGraph(F)
	for i in range(0,len(points)):
		P = Graph(points[i])
		P.mark(0.3,90,"$P_{%s}$"%str(i))
		pspict.DrawGraph(P)

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
