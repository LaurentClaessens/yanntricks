from phystricks import *
def Lines():
	pspict=pspicture("Lines")
	fig = GenericFigure("Lines")

	a = Point(1,1)
	b = Point(5,2)
	c = Point(2,5)
	A = Graph(a)
	B = Graph(b)
	C = Graph(c)
	A.mark(0.3,180,"$A$")
	B.mark(0.3,0,"$B$")
	C.mark(0.3,180,"$C$")
	pspict.DrawGraph(A)
	pspict.DrawGraph(B)
	pspict.DrawGraph(C)
	segment1 = Segment(A,B)
	segment2 = Segment(C,Point(3,-1))

	S1 = Graph(segment1)
	pspict.DrawGraph(S1)

	S2 = Graph(segment2)
	S2.parameters.color = "red"
	S2.parameters.style = "dotted"
	pspict.DrawGraph(S2)

	p = LineInterLine(segment1,segment2)
	P = Graph(p)
	P.mark(0.3,-45,"$P$")

	segment3 = Segment(A,C)
	S3 = Graph(segment3)
	S4 = Graph(segment3)
	S3.wave(0.2,0.1)
	S3.parameters.color = "cyan"
	S4.parameters.color = "blue"
	pspict.DrawGraph(S3)
	pspict.DrawGraph(S4)

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
