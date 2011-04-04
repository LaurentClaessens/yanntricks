from phystricks import *

"""
This file contains only doctests with output too long or not sufficiently interesting to be included in the code itself.
"""



def Test_SurfaceBetweenParametricCurve():
    r"""
    sage: pspict,fig = SinglePicture("IntBoutCercle")
    The result is on figure \ref{LabelFigIntBoutCercle}.
    \newcommand{\CaptionFigIntBoutCercle}{<+Type your caption here+>}
    \input{Fig_IntBoutCercle.pstricks}
    sage: C=Point(0,1)
    sage: alpha=0
    sage: circle = Circle(C,1)
    sage: c1=circle.graph(-90,alpha)
    sage: c2=circle.graph(alpha,270)
    sage: c1.parameters.color="red"
    sage: c2.parameters.color="blue"
    sage: P=circle.get_point(alpha)
    sage: P.put_mark(0.3,-45,"$P$")
    sage: s1=Segment(Point(0,0),P)
    sage: segment=s1.dilatation(2)
    sage: segment.parameters.color="red"
    sage: surface=SurfaceBetweenParametricCurves(s1,circle,(0,s1.length()),(-pi/2,radian(alpha)))
    sage: surface.parameters.color="cyan"
    sage: surface.curve1.parameters.style="solid"
    sage: surface.curve1.parameters.color="red"
    sage: surface.curve2.parameters=surface.curve1.parameters
    sage: print surface.pstricks_code(pspict)
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){aabc}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){aabd}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,0){aaba}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,0){aabb}
    \pscustom[hatchcolor=cyan,linestyle=none,fillcolor=cyan,linecolor=cyan,fillstyle=vlines]{
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{0.000000000000000}{1.41421356237310}{1/2*sqrt(2)*t | 1/2*sqrt(2)*t }
    <BLANKLINE>
    \pstLineAB[linestyle=solid,linecolor=black]{aabc}{aabd}
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{-1.57079632679490}{0.000000000000000}{cos(-1/2*3.1415 - t) | sin(-1/2*3.1415 - t) + 1 }
    <BLANKLINE>
    \pstLineAB[linestyle=solid,linecolor=black]{aaba}{aabb}
    }
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=red]{0.000000000000000}{1.41421356237310}{1/2*sqrt(2)*t | 1/2*sqrt(2)*t }
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=red]{-1.57079632679490}{0.000000000000000}{cos(t) | sin(t) + 1 }
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,0){aaba}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,0){aabb}
    <BLANKLINE>
    \pstLineAB[linestyle=solid,linecolor=black]{aaba}{aabb}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){aabc}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){aabd}
    <BLANKLINE>
    \pstLineAB[linestyle=solid,linecolor=black]{aabc}{aabd}
    """


def Test_Segment():
    """
    sage: v = Segment(Point(0,0),Point(2,0)).get_normal_vector()
    sage: print v.arrow_type
    vector
    sage: s= Segment(Point(1,1),Point(2,2))
    sage: v=s.get_normal_vector()
    sage: print v.I
    Point(1.5,1.5)
    sage: print v.F
    Point(1/2*sqrt(2) + 1.5,-1/2*sqrt(2) + 1.5)
    sage: print v.length()
    1

    sage: l = Segment(Point(0,0),Point(0,1))
    sage: v = AffineVector(Point(-1,1),Point(-2,3))
    sage: print v.equation
    x + 1/2*y + 1/2 == 0
    """

def Test_VectorField():
    """"
    sage: x,y=var('x,y')
    sage: F=VectorField(x,y).graph(xvalues=(x,1,2,3),yvalues=(y,-2,2,3))
    sage: unify_point_name(F.pstricks_code())
    '\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,-2.00000000000000){Xaaaa}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,-4.00000000000000){Xaaab}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,0){Xaaac}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,0){Xaaad}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaac}{Xaaad}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,2.00000000000000){Xaaae}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,4.00000000000000){Xaaaf}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaae}{Xaaaf}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.50000000000000,-2.00000000000000){Xaaag}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,-4.00000000000000){Xaaah}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaag}{Xaaah}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.50000000000000,0){Xaaai}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,0){Xaaaj}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaai}{Xaaaj}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.50000000000000,2.00000000000000){Xaaak}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,4.00000000000000){Xaaal}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaak}{Xaaal}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,-2.00000000000000){Xaaam}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,-4.00000000000000){Xaaan}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaam}{Xaaan}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,0){Xaaao}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,0){Xaaap}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaao}{Xaaap}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,2.00000000000000){Xaaaq}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,4.00000000000000){Xaaar}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaq}{Xaaar}'

    sage: G=VectorField(x,y).graph(draw_points=[Point(1,2),Point(3,4)])
    sage: unify_point_name(G.pstricks_code())
    '\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,2.00000000000000){Xaaaa}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,4.00000000000000){Xaaab}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,4.00000000000000){Xaaac}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](6.00000000000000,8.00000000000000){Xaaad}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaac}{Xaaad}'
"""

def Test_SingleAxe():
    r"""
    sage: axe = SingleAxe(Point(1,1),Vector(0,1),-2,2)
    sage: pspict=pspicture("MyTest")
    sage: unify_point_name(axe.pstricks_code(pspict))
    '\\pstGeonode[](0.400000000000000,-2.00000000000000){Xaaaa}\n\\rput(Xaaaa){\\rput(0;0){$-2$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,-2.00000000000000){ForTheBar}\n\\pstGeonode[](0.400000000000000,-1.00000000000000){Xaaab}\n\\rput(Xaaab){\\rput(0;0){$-1$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,-1.00000000000000){ForTheBar}\n\\pstGeonode[](0.400000000000000,0){Xaaac}\n\\rput(Xaaac){\\rput(0;0){$0$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,0){ForTheBar}\n\\pstGeonode[](0.400000000000000,1.00000000000000){Xaaad}\n\\rput(Xaaad){\\rput(0;0){$1$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,1.00000000000000){ForTheBar}\n\\pstGeonode[](0.400000000000000,2.00000000000000){Xaaae}\n\\rput(Xaaae){\\rput(0;0){$2$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,2.00000000000000){ForTheBar}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,-1.00000000000000){Xaaaf}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,3.00000000000000){Xaaag}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaf}{Xaaag}'

    sage: pspict=pspicture("MyTestAxe")
    sage: base=Vector(1,2).normalize()
    sage: print unify_point_name(base.pstricks_code())
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,0){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.447213595499958,0.894427190999916){Xaaab}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}

    sage: C=Point(0,0)
    sage: axe=SingleAxe(C,base,-1,1.5)
    sage: print unify_point_name(axe.pstricks_code(pspict))
    \pstGeonode[](-0.0894427190999917,-1.07331262919990){Xaaaa}
    \rput(Xaaaa){\rput(0;0){$-1$}}
    \pstGeonode[PointSymbol=|,dotangle=423.4349,linestyle=solid,linecolor=black](-0.447213595499958,-0.894427190999916){ForTheBar}
    \pstGeonode[](0.357770876399966,-0.178885438199983){Xaaab}
    \rput(Xaaab){\rput(0;0){$0$}}
    \pstGeonode[PointSymbol=|,dotangle=423.4349,linestyle=solid,linecolor=black](0,0){ForTheBar}
    \pstGeonode[](0.804984471899924,0.715541752799933){Xaaac}
    \rput(Xaaac){\rput(0;0){$1$}}
    \pstGeonode[PointSymbol=|,dotangle=423.4349,linestyle=solid,linecolor=black](0.447213595499958,0.894427190999916){ForTheBar}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-0.447213595499958,-0.894427190999916){Xaaad}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.670820393249937,1.34164078649987){Xaaae}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaad}{Xaaae}

    sage: pspict=pspicture("AnOtherAxTest")
    sage: pspict.axes.single_axeY.axes_unit=AxesUnit(2.34,"\\sigma")
    sage: pspict.axes.single_axeY.Dx=0.5
    sage: print unify_point_name(pspict.axes.pstricks_code(pspict))
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1000.01000000000,0){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-1000.00000000000,0){Xaaab}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,1000.01000000000){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,-1000.00000000000){Xaaad}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaac}{Xaaad}
    """

def Test_Dilatation():
    r"""
    sage: A = Point(1,1)
    sage: B = Point(-4,-1)
    sage: v=AffineVector(A,B)
    sage: w=v.dilatation(0.5)
    sage: v.parameters.color="blue"
    sage: w.parameters.color="red"

    sage: print unify_point_name(v.pstricks_code())
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-4.00000000000000,-1.00000000000000){Xaaab}
    \ncline[linestyle=solid,linecolor=blue]{->}{Xaaaa}{Xaaab}

    sage: print unify_point_name(w.pstricks_code())
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-1.50000000000000,0){Xaaab}
    \ncline[linestyle=solid,linecolor=red]{->}{Xaaaa}{Xaaab}
    """

def Test_Measure():
    r"""
    sage: O=Point(0,0)
    sage: A=Point(0.3,0)
    sage: U=Point(1,0)

    sage: measureOA=MeasureLength(Segment(O,A),0.1)
    sage: measureOA.put_mark(0.3,measureOA.advised_mark_angle,"$a$")
    sage: print unify_point_name(measureOA.pstricks_code())
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.150000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,-0.100000000000000){Xaaab}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.150000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.300000000000000,-0.100000000000000){Xaaac}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaac}

    sage: measureAU=MeasureLength(Segment(A,U),0.1)
    sage: measureAU.put_mark(0.3,measureAU.advised_mark_angle,"$1-a$")
    sage: print unify_point_name(measureAU.pstricks_code())
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.650000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.300000000000000,-0.100000000000000){Xaaab}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.650000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,-0.100000000000000){Xaaac}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaac}
    """

    
def Test_SurfaceBetweenFunctions_second():
    r"""
    sage: pspict,fig = SinglePicture("TesTSurfaceBetweenFunctionsecond")
    The result is on figure \ref{LabelFigTesTSurfaceBetweenFunctionsecond}.
    \newcommand{\CaptionFigTesTSurfaceBetweenFunctionsecond}{<+Type your caption here+>}
    \input{Fig_TesTSurfaceBetweenFunctionsecond.pstricks}
    sage: surf=SurfaceBetweenFunctions(sin(x)+3,cos(x),0,2*pi)
    sage: surf.parameters.color="green"
    sage: print unify_point_name(surf.pstricks_code(pspict))
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](6.28318530717959,3.00000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](6.28318530717959,1.00000000000000){Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,3.00000000000000){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,1.00000000000000){Xaaad}
    \pscustom[hatchcolor=green,linestyle=none,fillcolor=green,linecolor=green,fillstyle=vlines]{
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{0.000000000000000}{6.28318530717959}{t | sin(t) + 3 }
    <BLANKLINE>
    \pstLineAB[linestyle=none,linecolor=black]{Xaaaa}{Xaaab}
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{0.000000000000000}{6.28318530717959}{2*3.1415 - t | cos(2*3.1415 - t) }
    <BLANKLINE>
    \pstLineAB[linestyle=none,linecolor=black]{Xaaac}{Xaaad}
    }
    """

def Test_SurfaceBetweenFunctions_third():
    r"""
    sage: pspict,fig = SinglePicture("TesTSurfaceBetweenFunctionthird")
    The result is on figure \ref{LabelFigTesTSurfaceBetweenFunctionthird}.
    \newcommand{\CaptionFigTesTSurfaceBetweenFunctionthird}{<+Type your caption here+>}
    \input{Fig_TesTSurfaceBetweenFunctionthird.pstricks}
    sage: surf=SurfaceBetweenFunctions(sin(x)+3,cos(x),0,2*pi)
    sage: surf.parameters.color="green"
    sage: surf.f1.parameters.color="red"
    sage: surf.f1.parameters.style="solid"
    sage: surf.vertical_left.parameters.style="dashed"
    sage: surf.vertical_left.parameters.color="brown"
    sage: print unify_point_name(surf.pstricks_code(pspict))
       \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](6.28318530717959,3.00000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](6.28318530717959,1.00000000000000){Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,3.00000000000000){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,1.00000000000000){Xaaad}
    \pscustom[hatchcolor=green,linestyle=none,fillcolor=green,linecolor=green,fillstyle=vlines]{
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{0.000000000000000}{6.28318530717959}{t | sin(t) + 3 }
    <BLANKLINE>
    \pstLineAB[linestyle=none,linecolor=black]{Xaaaa}{Xaaab}
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{0.000000000000000}{6.28318530717959}{2*3.1415 - t | cos(2*3.1415 - t) }
    <BLANKLINE>
    \pstLineAB[linestyle=dashed,linecolor=brown]{Xaaac}{Xaaad}
    }
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{0.000000000000000}{6.28318530717959}{t | sin(t) + 3 }
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,3.00000000000000){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,1.00000000000000){Xaaad}
    <BLANKLINE>
    \pstLineAB[linestyle=dashed,linecolor=brown]{Xaaac}{Xaaad}
    \psplot[linestyle=solid,plotpoints=100,linecolor=red]{0.000000000000000}{6.28318530717959}{sin(x) + 3}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,3.00000000000000){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,1.00000000000000){Xaaad}
    <BLANKLINE>
    \pstLineAB[linestyle=dashed,linecolor=brown]{Xaaac}{Xaaad}
    """

def Test_SurfaceBetweenFunctions():
    r"""
    sage: pspict,fig = SinglePicture("TesTSurfaceBetweenFunction")
    The result is on figure \ref{LabelFigTesTSurfaceBetweenFunction}.
    \newcommand{\CaptionFigTesTSurfaceBetweenFunction}{<+Type your caption here+>}
    \input{Fig_TesTSurfaceBetweenFunction.pstricks}
    sage: a=1
    sage: b=4
    sage: m=float(b+a)/2
    sage: x=var('x')
    sage: f=phyFunction(sin(x+1)+2)
    sage: g=phyFunction(-(x-2)**(2)+6)                                                                                                             
    sage: reg=SurfaceBetweenFunctions(f,g,a,b)                                                                                                      
    sage: reg.parameters.hatched()                                                                                                                  
    sage: reg.parameters.hatch.color="red"                                                                                                          
    sage: reg.vertical_left.parameters.style="dashed"                                                                                               
    sage: reg.vertical_right.parameters.style="solid"                       
    sage: reg.f1.parameters.style="solid"  
    sage: reg.f1.parameters.color="blue"       
    sage: reg.f2.parameters.style="dotted"         
    sage: reg.f2.parameters.color="blue"                                                                                                          
    sage: print unify_point_name(reg.pstricks_code(pspict))
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,1.04107572533686){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,2.00000000000000){Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,2.90929742682568){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,5.00000000000000){Xaaad}
    \pscustom[hatchcolor=red,linestyle=none,hatchangle=-45,linecolor=black,fillstyle=vlines]{
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{1.00000000000000}{4.00000000000000}{t | sin(t + 1) + 2 }
    <BLANKLINE>
    \pstLineAB[linestyle=solid,linecolor=black]{Xaaaa}{Xaaab}
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{1.00000000000000}{4.00000000000000}{-t + 5 | -(t - 3)^2 + 6 }
    <BLANKLINE>
    \pstLineAB[linestyle=dashed,linecolor=black]{Xaaac}{Xaaad}
    }
    \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{1.00000000000000}{4.00000000000000}{t | sin(t + 1) + 2 }
    \parametricplot[plotstyle=curve,linestyle=dotted,plotpoints=1000,linecolor=blue]{1.00000000000000}{4.00000000000000}{t | -(t - 2)^2 + 6 }
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,2.90929742682568){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,5.00000000000000){Xaaad}
    <BLANKLINE>
    \pstLineAB[linestyle=dashed,linecolor=black]{Xaaac}{Xaaad}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,1.04107572533686){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,2.00000000000000){Xaaab}
    <BLANKLINE>
    \pstLineAB[linestyle=solid,linecolor=black]{Xaaaa}{Xaaab}
    \psplot[linestyle=solid,plotpoints=100,linecolor=blue]{1.00000000000000}{4.00000000000000}{sin(x + 1) + 2}
    \psplot[linestyle=dotted,plotpoints=100,linecolor=blue]{1.00000000000000}{4.00000000000000}{-(x - 2)^2 + 6}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,2.90929742682568){Xaaac}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,5.00000000000000){Xaaad}
    <BLANKLINE>
    \pstLineAB[linestyle=dashed,linecolor=black]{Xaaac}{Xaaad}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,1.04107572533686){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,2.00000000000000){Xaaab}
    <BLANKLINE>
    \pstLineAB[linestyle=solid,linecolor=black]{Xaaaa}{Xaaab}
    """
