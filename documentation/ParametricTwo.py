from phystricks import *
def ParametricTwo():
	pspict=pspicture("ParametricTwo")
	fig = GenericFigure("ParametricTwo")

	var('x')
	f1 = phyFunction( x*sin(x) )
	f2 = phyFunction( x )
	f3 = phyFunction( x*cos(x) )

	llI = 0
	llF = 5
	wl = 0.1
	amplitude = 0.1
	curve1 = ParametricCurve(f1,f2)
	F1 = Graph(curve1,llI,llF)
	G1 = Graph(curve1,llI,llF)
	curve2 = ParametricCurve(f1,f3)
	F2 = Graph(curve2,llI,llF)

	F1.parameters.color = "brown"
	G1.parameters.color = "magenta"
	G1.wave(wl,amplitude)

	for ll in curve2.get_regular_parameter(llI,llF,2):
		v1 = curve2.tangent_vector(ll)
		v2 = curve2.normal_vector(ll)
		V1 = Graph(v1)
		V2 = Graph(v2)
		pspict.DrawGraph(V1)
		pspict.DrawGraph(V2)

	pspict.DrawGraph(F1)
	pspict.DrawGraph(G1)
	pspict.DrawGraph(F2)

	pspict.DrawDefaultAxes()

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()

