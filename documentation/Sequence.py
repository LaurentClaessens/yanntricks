from phystricks import *
def Sequence():
	pspict=pspicture("sequence")
	fig = GenericFigure("sequence")

	nmax = 10
	P = []
	for i in range(1,nmax):
		x = i
		y = ((-1)**i)/float(i)
		p = Point(x,y)

		P = Graph(p)
		P.mark(0.3,90*(-1)**i,"$P_{%s}$"%(str(i)))
		
		pspict.DrawGraph(P)

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
