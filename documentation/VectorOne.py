from phystricks import *
def VectorOne():
	pspict=pspicture("VectorOne")
	fig = GenericFigure("VectorOne")

	O = Point(0,0)
	A = Point(1,1)
	B = Point(-4,-1)
	C = Point(-2,3)

	v = []
	v.append(Vector(O,A).fix_size(3))
	v.append(Vector(A,C))
	v.append(Vector(B,C))
	v.append( v[1].rotation(30).dilatation(0.5) )
	v.append( v[1].rotation(-30) )
	v.append( v[1].orthogonal() )

	V = [Graph(vect) for vect in v]

	V[1].mark(0.3,45,"$v$")
	V[1].parameters.color="brown"
	V[2].parameters.color="red"
	V[2].parameters.style = "dotted"
	V[3].parameters.color=V[1].parameters.color	
	V[4].parameters.style = "dashed"
	V[4].parameters.color=V[1].parameters.color
	V[5].parameters.color=V[1].parameters.color

	for i in range(0,len(V)):
		pspict.DrawGraph(V[i])

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()
