# -*- coding: utf8 -*-

###########################################################################
#	This is part of the module phystricks
#
#   phystricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   phystricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with phystricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2010
# email: moky.math@gmai.com

"""
This module contains the basic graphics elements like points, segments and vectors.

These elements are not supposed to depend on others. They include new LaTeX commands. Objects that are not here do not 
imply new LaTeX concepts and only make an automated use of the objects that are here.

This module also contains some specific "constructors" for some classes, like PolarVector for example.
"""

import math
from sage.all import *
from SmallComputations import *
#from BasicGraphObjects import *
import phystricks

class ListeNomsPoints(object):
	"""
	This class serves to give a psname to my points. 

	TODO : use a real iterator.
	"""
	def __init__(self):
		self.donne = 1000
	def suivant(self):
		self.donne = self.donne + 1
		#a = ["AutoPt"]
		s = str(self.donne)
		return "".join( [chr(int(c)+97) for c in s] )

def Point(x,y):
	return GraphOfAPoint(GeometricPoint(x,y))
def Segment(A,B):
	return GraphOfASegment(GeometricSegment(A,B))
def Vector(a,b):
	return GraphOfAVector(GeometricVector(a,b))
def Circle(center,radius):
	return GraphOfACircle(GeometricCircle(center,radius))
def Rectangle(NW,SE):
	return GraphOfARectangle(GeometricRectangle(NW,SE))

class GeometricPoint(object):
	"""
	This is a point. Each point comes with a name given by a class attribute.
	"""
	NomPointLibre = ListeNomsPoints()

	def __init__(self,x,y):
		if type(x) == str : print "Attention : x est du type str"
		if type(y) == str : print "Attention : y est du type str"
		self.x = float(x)
		self.y = float(y)
		self.psNom = GeometricPoint.NomPointLibre.suivant()

	# La méthode EntierPlus place le point sur les coordonnées entières plus grandes (ou égales) à les siennes.
	#def EntierPlus(self):
	#	Px = self.x
	#	Py = self.y
	#	self.x = CalculEntierPlus(Px)
	#	self.y = CalculEntierPlus(Py)

	# La méthode EntierMoins place le point sur les coordonnées entières plus petites (ou égales) à les siennes.
	#def EntierMoins(self):
	#	Px = self.x
	#	Py = self.y
	#	self.x = CalculEntierMoins(Px)
	#	self.y = CalculEntierMoins(Py)

	# Donne la projection du point sur la ligne du segment donné
	def projection(self,seg):
		if seg.vertical :
			return Point(seg.I.x,self.y)
		if seg.horizontal :
			return Point(self.x,seg.I.y)
		else :
			Rx = (self.y*seg.coefficient - seg.coefficient*seg.independant + self.x)/(seg.coefficient**2 + 1)
			Ry = (self.y*seg.coefficient**2 + self.x*seg.coefficient + seg.independant)/(seg.coefficient**2 + 1)
			return Point(Rx,Ry)
	def translate(self,v):
		"""Do a translation of the point with the vector v"""
		return self+v
	def lie(self,p):
		return Vector(p,Point(p.x+self.x,p.y+self.y))
	def Vector(self):
		return Vector(Point(0,0),self)

	def norme(self):
		return Segment(Point(0,0),self).longueur
	# La méthode normalize voit le point comme un vecteur partant de zéro, et en donne le vecteur de taille 1
	def normalize(self):
		return self*(1/self.norme())
	def default_graph(self,opt):
		"""
		Return a default Graph
		
		If p is a Point, you can use pspict.DrawObject(p,symbol,arguments) in order to draw it in a default way.
		<opt> is a tuple. The first is the symbol to the point (like "*" or "none").
		The second is a string to be passed to pstricks, like "linecolor=blue,linestyle=dashed".
		"""
		P=self.default_associated_graph_class()(self)
		P.parameters.symbol=opt[0]
		P.add_option(opt[1])
		return P
	def default_associated_graph_class(self):
		"""Return the class which is the Graph associated type"""
		return phystricks.GraphOfAPoint				# Graph is also a method of Sage

	def code(self,params="PointSymbol=none,PointName=none"):
		"""
		Return the code if one wants to put the point with the options params (string).
		It is typically used with PointSymbol=none,PointName=none in order to create the code of
		more complex objects.
		"""
		print "This method is depreciated. Use Graph instead. Please, RTFM before to ask me silly thinks !"		
		print "If you really want to draw the point without creating a Graph, you should use DrawObject"
		return "\pstGeonode["+params+"]"+self.coordinates()+"{"+self.psNom+"}"
	def create_PSpoint(self):
		"""Return the code of creating a pstgeonode. The argument is a Point of GraphOfAPoint"""
		P = Point(self.x,self.y)
		P.psNom = self.psNom
		P.parameters.symbol="none"
		return P.pstricks_code()+"\n"
	def coordinates(self):
		x = self.x
		y = self.y
		# Ces petites précautions pour éviter d'avoir des 0.125547e-6, parce que pstricks n'aime pas cette notation.
		if abs(x) < 0.0001 : x=0
		if abs(y) < 0.0001 : y=0
		return "("+str(x)+","+str(y)+")"
	def coordinatesBr(self):
		return self.coordinates.replace("(","{").replace(")","}")
	def Affiche(self):
		return self.coordinates()
	def graph_object(self):
		return phystricks.GraphOfAPoint(self)
	def copy(self):
		return Point(self.x,self.y)
	# Surcharger quelque opérateurs
	def __add__(self,v):
		"""
		Addition of a point with a vector is the parallel translation, while addition of a point with an other point is simply
		the addition of coordinates.
		"""
		try :
			dx = v.Dx
			dy = v.Dy
		except AttributeError :
			try :
				dx = v.x
				dy = v.y
			except AttributeError :
				print "You seem to add myself with something which is not a Point neither a Vector. Sorry, but I'm going to crash."
				raise
		return Point(self.x+dx,self.y+dy)
	def __mul__(self,r):
		return Point(r*self.x,r*self.y)
	def __str__(self):
		return "Point (%s,%s)"%(str(self.x),str(self.y))

class GeometricSegment(object):
	def __init__(self,A,B):
		self.I = A
		self.F = B
		self.vertical = 0
		self.horizontal = 0
		if A.x == B.x : self.vertical = 1
		if A.y == B.y : self.horizontal = 1
		if self.vertical == 1:
			self.coefficient = None
			self.independant = None
		else :
			self.coefficient = (self.F.y-self.I.y)/(self.F.x-self.I.x)
			self.independant = (self.F.x*self.I.y-self.F.y*self.I.x)/(self.F.x-self.I.x)
		if self.vertical :
			self.equation = [1,0,-A.x]
		if self.horizontal :
			self.equation = [0,1,-A.y]
		if not (self.vertical or self.horizontal) :
			"""
			self.equation is a list [a,b,c] which corresponds to the Cartesian equation
			ax+by+c=0
			"""
			self.equation = [1,-(A.x-B.x)/(A.y-B.y),-(A.y*B.x-A.x*B.y)/(A.y-B.y)]
		self.longueur = Distance(self.I,self.F)
		self.maxima = str(self.equation[0])+"*x+"+str(self.equation[1])+"*y+"+str(self.equation[2])+"=0"
	def phyFunction(self):
		if self.horizontal:
			# The trick to define a constant function is explained here:
			# http://groups.google.fr/group/sage-support/browse_thread/thread/e5e8775dd79459e8?hl=fr?hl=fr
			var('x')
			fi = SR(A.y).function(x)
			return phyFunction(fi)
		if not (self.vertical or self.horizontal) :
			parms = [self.coefficient,(A.y*B.x-A.x*B.y)/(A.x-B.x)]
			var('x')
			return phyFunction( self.coefficient*x+self.independant )
	def sage_equation(self):
		"""
		returns the Cartesian equation of the line as a instance of the sage's class
		sage.symbolic.expression.Expression
		"""
		var('x,y')
		return self.equation[0]*x+self.equation[1]*y+self.equation[2] == 0
	def get_regular_points(self,dx):
		"""
		Notice that it does not return the last point of the segment, unless the length is a multiple of dx.
		   this is why we add by hand the last point in GetWavyPoint
		"""
		n = floor(self.longueur/dx)
		return [self.proportion(float(i)/n) for i in range(0,n)]
	def get_wavy_points(self,dx,dy):
		"""
		Return a list of points that make a wave around the segment.
		The wavelength is dx and the amplitude is dy.
		The first and the last points are self.I and self.F and are then *on* the segment. Thus the wave begins and ends on the segment.
		"""
		normal = self.normal_vector().fix_size(dy)
		PI = self.get_regular_points(dx)
		PIs = [self.I]
		PIs.extend( [  PI[i]+normal*(-1)**i for i in range(1,len(PI))  ] )
		PIs.append(self.F)
		return PIs
	def proportion(self,p):
		"""
		returns a point on the segment which is at the position
		(p-1)*I+p*F
		if I and F denote the initial and final point of the segment.
		"""
		return self.I*(1-p) + self.F*p
	def milieu(self):
		print "This method is depreciated. Use Segment.center() instead"
		raise
		return self.center()
	def center(self):
		return self.proportion(0.5)
	def Vector(self):
		return Vector(self.I,self.F)
	def normal_vector(self):
		"""
		returns a normalized normal vector at the center of the segment
		"""
		if self.vertical :
			return Point(-1,0).Vector().lie(self.center())
		else :
			P = Point(-self.coefficient,1)
			return P.Vector().normalize().lie(self.center())
	def norme(self):
		print "The method norme of Segment is depreciated. Use length instead."
		return Distance(self.I,self.F)
	def length(self):
		return Distance(self.I,self.F)
	def dilate(self,coef):
		""" return a Segment which is dilated by the coefficient coef """
		return self.fix_size(self.length()*coef)
	# La méthode suivante retourne un nouveau segment qui est allongé de lI du côté de self.I et de lF du côté de self.F
	def add_size(self,lI,lF):
		vI = Vector(self.center(),self.I)
		vF = Vector(self.center(),self.F)
		I = vI.add_size(lI).F
		F = vI.add_size(lF).F
		return Segment(I,F)
	def fix_size(self,l):
		vI = Vector(self.center(),self.I)
		vF = Vector(self.center(),self.F)
		I = vI.fix_size(l/2).F
		F = vF.fix_size(l/2).F
		return Segment(I,F)

	def Affiche(self):
		return str(self.equation[0])+" x + "+str(self.equation[1])+" y + "+str(self.equation[2])
	def Rotation(self,angle):
		x = self.I.x+self.longueur*math.cos(angle)
		y = self.I.y+self.longueur*math.sin(angle)
		return Segment(self.I,Point(x,y))
	def translate(self,vecteur):
		return Segment(self.I.translate(vecteur),self.F.translate(vecteur))
	#def code(self,params):
	#	raise AttributeError,"Pas de code à un segment seul"
	def graph(self):
		return phystricks.GraphOfASegment(self)
	def default_associated_graph_class(self):
		"""Return the class which is the Graph associated type"""
		return phystricks.GraphOfASegment

class GeometricCircle(object):
	def __init__(self,center,radius):
		self.center = center
		self.radius = radius
	def parametric_curve(self):
		var('x')
		f1 = phyFunction(self.center.x+self.radius*cos(x))
		f2 = phyFunction(self.center.y+self.radius*sin(x))
		return ParametricCurve(f1,f2)
	def get_point(self,theta):
		return Point(self.center.x+self.radius*math.cos(radian(theta)), self.center.y+self.radius*math.sin(radian(theta)) )
	# Donne le vecteur normal de norme 1 au cercle au point d'angle theta
	def VectorTangent(self,theta):
		return PolarPoint(1,theta+90).lie(self.get_point(theta))
	def normal_vector(self,theta):
		return PolarPoint(1,theta).lie(self.get_point(theta))
	# Donne les x et y min et max du cercle entre deux angles.
	# Here, angleI and angleF are given in degree while parametric_plot uses radian.
	def get_minmax_data(self,angleI,angleF):
		deb = radian(angleI)
		fin = radian(angleF)
		return self.parametric_curve().get_minmax_data(deb,fin)
	def xmax(self,angleI,angleF):
		return self.get_minmax_data(angleI,angleF)['xmax']
	def xmin(self,angleI,angleF):
		return self.get_minmax_data(angleI,angleF)['xmin']
	def ymax(self,angleI,angleF):
		return self.get_minmax_data(angleI,angleF)['ymax']
	def ymin(self,angleI,angleF):
		return self.get_minmax_data(angleI,angleF)['ymin']
	def graph(self):
		return phystricks.GraphOfACircle(self)
	def __str__(self):
		return "Circle, center=%s, radius=%s"%(self.center.__str__(),str(self.radius))

class GeometricVector(object):
	"""
	If two points are given to the constructor, return the vector 
	"""
	def __init__(self,a,b):
		self.segment = GeometricSegment(a,b)
		self.I = self.segment.I
		self.F = self.segment.F
		self.Point = Point(self.F.x-self.I.x,self.F.y-self.I.y)		# Le point qui serait le vecteur lié à (0,0).
		self.Dx = self.F.x-self.I.x
		self.Dy = self.F.y-self.I.y
	def inverse(self):
		return Vector(self.I,Point(self.I.x-self.Dx,self.I.y-self.Dy))
	def rotation(self,angle):
		return PolarVector(self.I,self.polaires().r,degree(self.polaires().theta)+angle)
	def orthogonal(self):
		return self.rotation(90)
	def dilatation(self,coef):
		return self*coef
	def polaires(self):
		return PointToPolaire(self.Point)
	def norme(self):
		print "The method norme on Vector is depreciated use length instead"
		return self.polaires().r
	def length(self):
		return self.polaires().r
	def angle(self):
		"""return the angle of the vector (gradient)"""
		return self.polaires().theta
	def lie(self,p):
		return Vector(p,Point(p.x+self.Dx,p.y+self.Dy))
	def fix_size(self,l):
		return self.dilatation(l/self.length())
	def add_size(self,l):
		""" return a Vector with added length on its extremity """
		return self*((self.length()+l) / self.length())	
	def normalize(self):
		return self.fix_size(1)
	def default_associated_graph_class(self):
		return phystricks.GraphOfAVector
	def __mul__(self,coef):
		return Vector(self.I,Point(self.I.x+self.Dx*coef,self.I.y+self.Dy*coef))
	def __div__(self,coef):
		return self * (1/coef)
class GeometricRectangle(object):
	"""
	The four points of the square are designated by NW,NE,SW and SE.
	"""
	def __init__(self,NW,SE):
		self.NW = NW
		self.SE = SE
		self.SW = Point(self.NW.x,self.SE.y)
		self.NE = Point(self.SE.x,self.NW.y)
	def first_diagonal(self):
		return Segment(self.NW,self.SE)
	def second_diagonal(self):
		return Segment(self.SW,self.NE)
	def segment_N(self):
		return Segment(self.NW,self.NE)
	def segment_S(self):
		return Segment(self.SW,self.SE)
	def segment_E(self):
		return Segment(self.NE,self.SE)
	def segment_W(self):
		return Segment(self.NW,self.SW)
	def center(self):
		return self.first_diagonal().center()
	def default_associated_graph_class(self):
		"""Return the class which is the Graph associated type"""
		return phystricks.GraphOfARectangle

def OptionsStyleLigne():
	return ["linecolor","linestyle"]

class Options(object):
	"""
	Describe the drawing options of pstricks objects.

	ATTRIBUTES :
		self.DicoOptions : dictionnary which contains the options
	METHODS :
		self.merge_options(opt) : opt is an other object of the class Options. The method merges the two in the sense that opt is not
						changed, but 
						1. if opt contains a key more, it is added to self
						2. if a key of opt is different of the one of self, self is changed
	"""
	def __init__(self):
		self.DicoOptions = {}

	# On ajoute une des options en donnant genre
	# LineColor=blue,LineStyle=dashed
	# Ou alors en donnant un dictionnaire genre
	# {"Dx":1,"Dy":3}
	def add_option(self,opt):
		if opt :			# If the argument is empty.
			try:
				for op in opt.split(","):
					s = op.split("=")
					self.DicoOptions[s[0]] = s[1]
			except AttributeError :
				for op in opt.keys():
					self.DicoOptions[op] = opt[op]

	def remove_option(self,opt):
		del(self.DicoOptions[opt])
	def merge_options(self,opt):
		for op in opt.DicoOptions.keys():
			self.add_option({op:opt[op]})
	def extend_options(self,Opt):
		for opt in Opt.DicoOptions.keys():
			self.add_option(opt+"="+Opt.DicoOptions[opt])
	# Afiter est une liste de noms d'options, et cette méthode retourne une instance de Options qui a juste ces options-là, 
	# avec les valeurs de self.
	def sousOptions(self,AFiter):
		O = Options()
		for op in self.DicoOptions.keys() :
			if op in AFiter : O.add_option(op+"="+self.DicoOptions[op])
		return O
	def style_ligne(self):
		return self.sousOptions(OptionsStyleLigne())

	def __getitem__(self,opt):
		return self.DicoOptions[opt]

	def code(self):
		a = []
		for op in self.DicoOptions.keys():
			a.append(op+"="+self.DicoOptions[op])
			a.append(",")
		del a[-1:]
		return "".join(a)
class Waviness(object):
	"""
	This class contains the informations about the waviness of a curve. It takes as argument a GraphOfAphyFunction and the parameters dx, dy of the wave.
	Waviness.get_wavy_points		returns a list of points which are disposed around the graph of the curve. These are the points to be linked
					   by a bezier or something in order to get the wavy graph of the function.
	"""
	def __init__(self,graphe,dx,dy):
		self.graphe = graphe
		self.dx = dx
		self.dy = dy
		self.obj = self.graphe.obj
		if type(self.obj) == phyFunction :
			self.Mx = self.graphe.Mx
			self.mx = self.graphe.mx
	def get_wavy_points(self):
		if type(self.obj) == phyFunction :
			return self.obj.get_wavy_points(self.mx,self.Mx,self.dx,self.dy)
		if type(self.obj) == Segment :
			return self.obj.get_wavy_points(self.dx,self.dy)

class Mark(object):
	def __init__(self,graphe,dist,angle,text):
		self.graphe = graphe
		self.dist = dist
		self.angle = angle
		self.text = text
	def central_point(self):
		"""return the central point of the mark, that is the point where the mark arrives"""
		return self.graphe.translate(PolarVector(self.graphe,self.dist,self.angle))

class FillParameters(object):
	"""The filling parameters"""
	def __init__(self):
		self.color= None
		self.style= "solid"
	def add_to_options(self,opt):
		if self.color :
			opt.add_option("fillcolor=%s"%str(self.color))
		if self.style :
			opt.add_option("fillstyle=%s"%str(self.style))

class HatchParameters(object):
	"""Same as FillParameters, but when one speaks about atched"""
	def __init__(self):
		self.color = None
		self._crossed = False
		self.angle = -45
	def crossed(self):
		self._crossed=True
	def add_to_options(self,opt):
		opt.add_option("hatchangle=%s"%str(self.angle))
		if self._crossed:
			opt.add_option("fillstyle=crosshatch")
		else:
			opt.add_option("fillstyle=vlines")
		if self.color :
			opt.add_option("hatchcolor=%s"%str(self.color))

class Parameters(object):
	def __init__(self):
		self.color = None
		self.symbol = None
		self.style = None
		self.fill=FillParameters()
		self.hatch=HatchParameters()
		self._filled=False
		self._hatched=False
	def filled(self):
		self._filled=True
	def hatched(self):
		self._hatched=True
	def add_to_options(self,opt):
		if self.color :
			opt.add_option("linecolor=%s"%str(self.color))
		if self.style :
			opt.add_option("linestyle=%s"%str(self.style))
		if self.symbol :
			opt.add_option("PointSymbol=%s"%str(self.symbol))
		if self._filled:
			self.fill.add_to_options(opt)
		if self._hatched:
			self.hatch.add_to_options(opt)

class GraphOfAnObject(object):
	""" This class is supposed to be used to create other "GraphOfA..." by inheritance. It is a superclass. """
	# self.record_add_to_bb is a list of points to be added to the bounding box.
	# Typically, when a point has a mark, one can only know the size of the box at the end of the picture 
	#(because of xunit, yunit that change when using dilatation)
	# Thus if one wants to draw the bounding box, it has to be done at the end.
	def __init__(self,obj):
		self.obj = obj
		self.parameters = Parameters()
		self.wavy = False
		self.waviness = None
		self.options = Options()
		self.marque = False
		self.add_option("linecolor=black")
		self.add_option("linestyle=solid")
		self.record_add_to_bb=[]		 
	def wave(self,dx,dy):					# dx is the wave length and dy is the amplitude
		self.wavy = True
		self.waviness = Waviness(self,dx,dy)
	def put_mark(self,dist,angle,text):
		self.marque = True
		self.mark = Mark(self,dist,angle,text)
	def add_option(self,opt):
		self.options.add_option(opt)
	def get_option(opt):
		return self.options.DicoOptions[opt]
	def remove_option(opt):
		self.options.remove_option(opt)
	def merge_options(self,graphe):
		"""
		takes an other object GraphOfA... and merges the options as explained in the documentation
		of the class Options. That merge takes into account the attributes "color", "style", wavy
		"""
		self.parameters = graphe.parameters
		self.options.merge_options(graphe.options)
		self.wavy = graphe.wavy
		self.waviness = graphe.waviness
	def conclude_params(self):
		self.parameters.add_to_options(self.options)
	def params(self):
		self.conclude_params()
		return self.options.code()

class GraphOfAPoint(GraphOfAnObject,GeometricPoint):
	def __init__(self,point):
		GraphOfAnObject.__init__(self,point)
		GeometricPoint.__init__(self,point.x,point.y)
		self.psNom = point.psNom		# The psNom of the point is erased when running Point.__init__
		self.point = self.obj
		self.add_option("PointSymbol=*")
		self._advised_mark_angle=None
	def bounding_box(self,pspict):
		"""
		return the bounding box of the point including its mark

		A small box of radius 0.1 is given in any case, and the mark is added if there is a one.
		You need to provide a pspict in order to compute the size since it can vary from the place in your document you place the figure.
		"""
		bb = BoundingBox(Point(self.x-0.1,self.y-0.1),Point(self.x+0.1,self.y+0.1))
		if self.marque:
			pspict.record_marks.append(self.mark)		# We cannot compute here the size of the bounding box
									# due to the mark because xunit,yunit will only be fixed
									# after possible use of pspict.Dilatation
									# See pspicture.contenu
		for P in self.record_add_to_bb:
			bb.AddPoint(P)
		return bb
	def math_bounding_box(self,pspict):
		"""Return a bounding box which include itself and that's it."""
		return BoundingBox(self.point,self.point)
	def pstricks_code(self):
		a = []
		a.append("\pstGeonode["+self.params()+"]"+self.coordinates()+"{"+self.psNom+"}")
		if self.marque :
			mark = self.mark
			R = RealField(round(log(10,2)*7))
			angle=R(mark.angle)			# If not, pstricks complains because of a too long number.
			a.append(r"\rput(%s){\rput(%s;%s){%s}}"%(self.psNom,str(mark.dist),str(angle),str(mark.text)))
		return "\n".join(a)

def Code_Pscurve(listePoints,params):
	"""
	From a list of points and parameters, gives the code of the corresponding pscurve.

	TODO : create something like a class InterpolationCurve.
	"""
	l = []
	l.append("\pscurve["+params+"]")
	for p in listePoints :
		l.append(p.coordinates())
	ligne = "".join(l)
	return ligne

class GraphOfASegment(GraphOfAnObject,GeometricSegment):
	def __init__(self,seg):
		GraphOfAnObject.__init__(self,seg)
		GeometricSegment.__init__(self,seg.I,seg.F)
		self.seg = self.obj
		self.I = self.seg.I
		self.F = self.seg.F
	def bounding_box(self,pspicture=1):
		return BoundingBox(self.I,self.F)		# If you change this, maybe you have to adapt math_bounding_box
	def math_bounding_box(self,pspicture=1):
		return self.bounding_box(pspicture)
	def pstricks_code(self):
		if self.wavy:
			waviness = self.waviness
			return Code_Pscurve(self.get_wavy_points(waviness.dx,waviness.dy),self.params())
		else:
			a =  self.I.create_PSpoint() + self.F.create_PSpoint()
			a=a+"\n\pstLineAB[%s]{%s}{%s}"%(self.params(),self.I.psNom,self.F.psNom)
			return a

class GraphOfAVector(GraphOfAnObject,GeometricVector):
	def __init__(self,vect):
		GraphOfAnObject.__init__(self,vect)
		GeometricVector.__init__(self,vect.I,vect.F)
		self.vector = self.obj
		self.I.psNom = self.vector.I.psNom
		self.F.psNom = self.vector.F.psNom
	def bounding_box(self,pspict):
		return GraphOfASegment(self.segment).bounding_box()
	def math_bounding_box(self,pspict):
		return GraphOfASegment(self.segment).math_bounding_box(pspict)
	def pstricks_code(self):
		a = self.segment.I.create_PSpoint() + self.segment.F.create_PSpoint()
		a = a + "\\ncline["+self.params()+"]{->}{"+self.segment.I.psNom+"}{"+self.segment.F.psNom+"}"
		if self.marque :
			P = self.F
			P.parameters.symbol = "none"
			P.put_mark(self.mark.dist,self.mark.angle,self.mark.text)
			a = a + P.pstricks_code()
		return a

class MeasureLength(GraphOfASegment):
	def __init__(self,seg):
		self.segment=seg
		GraphOfASegment.__init__(self,seg)
		self.dist=0.1
		self.delta=self.normal_vector().fix_size(self.dist)
		self.mseg=self.seg.translate(self.delta)
		self.mI=self.mseg.I
		self.mF=self.mseg.F
	def recompute(self):
		"""
		Because self.dist can change, we have to be able to adapt the other features
		"""
		self.delta=self.normal_vector().fix_size(self.dist)
		self.mseg=self.seg.translate(self.delta)
		self.mI=self.mseg.I
		self.mF=self.mseg.F
	def math_bounding_box(self,pspict):
		return GraphOfASegment(self.mseg).math_bounding_box()
	def bounding_box(self,pspict):
		bb=self.mseg.bounding_box(pspict)
		if self.marque:
			C=self.mseg.center()
			C.marque=self.marque
			C.mark=self.mark
			C.mark.graphe=C
			bb.AddBB(C.bounding_box(pspict))
		return bb
	def pstricks_code(self):
		self.recompute()
		a=[]
		C=self.mseg.center()
		C.marque=self.marque
		vI=Vector(C,self.mI)
		vF=Vector(C,self.mF)
		vI.parameters=self.parameters
		vF.parameters=self.parameters
		a.append(vI.pstricks_code())
		a.append(vF.pstricks_code())
		if self.marque :
			C.mark=self.mark
			C.add_option('PointSymbol=none')
			a.append(C.pstricks_code())
		return "\n".join(a)


class GraphOfARectangle(GraphOfAnObject,GeometricRectangle):
	"""
	The parameters of the four lines are by default the same, but they can be adapted separately.

	graph_N returns the north side as a phystricks.Segment object
	The parameters of the four sides have to be set independently.
	"""
	def __init__(self,rect):
		GraphOfAnObject.__init__(self,rect)
		GeometricRectangle.__init__(self,rect.NW,rect.SE)
		self.rectangle = self.obj
	def _segment(self,side):
		bare_name = "graph_"+side
		if not bare_name in self.__dict__.keys():
			line = self.__getattribute__("segment_"+side)()
			#line.parameters=self.parameters
			self.__dict__[bare_name]=line
		return 	self.__dict__[bare_name]
	def __getattr__(self,attrname):
		if "graph_" in attrname:
			return self._segment(attrname[6])
	def bounding_box(self,pspicture=1):
		return BoundingBox(self.NW,self.SE)
	def math_bounding_box(self,pspicture=1):
		return self.bounding_box(pspicture)
	def pstricks_code(self):
		a=[]
		a.append(self.graph_N.pstricks_code())
		a.append(self.graph_S.pstricks_code())
		a.append(self.graph_E.pstricks_code())
		a.append(self.graph_W.pstricks_code())
		return "\n".join(a)

class GraphOfACircle(GraphOfAnObject,GeometricCircle):
	def __init__(self,circle):
		GraphOfAnObject.__init__(self,circle)
		GeometricCircle.__init__(self,circle.center,circle.radius)
		self.circle = self.obj
		self.angleI = 0
		self.angleF = 2*pi		# By default, the circle is drawn between the angles 0 and 2pi.
	def copy(self):
		"""Return a copy of the object as geometrical object: the style and drawing parameters are not copied."""
		return Circle(self.center,self.radius)
	def math_bounding_box(self,pspict):
		return self.bounding_box(pspict)
	def bounding_box(self,pspict):
		# TODO : take into account self.angleI and self.angleF.
		bb = BoundingBox()
		bb.AddX(self.center.x+self.radius)
		bb.AddX(self.center.x-self.radius)
		bb.AddY(self.center.y+self.radius)
		bb.AddY(self.center.y-self.radius)
		return bb
	def pstricks_code(self):
		if self.wavy:
			waviness = self.waviness
			alphaI = radian(self.angleI)
			alphaF = radian(self.angleF)
			curve = self.parametric_curve()
			G = phystricks.GraphOfAParametricCurve(curve,alphaI,alphaF)
			G.add_option(self.params())
			# The two following lines are a pity. If I add some properties, I have to change by hand...
			G.parameters.style = self.parameters.style
			G.parameters.color = self.color
			G.wave(waviness.dx,waviness.dy)
			return G.pstricks_code()
		else:
			if self.angleI == 0 and self.angleF == 2*pi :
				PsA = Point(self.center.x-self.radius,self.center.y)		
				a = PsA.create_PSpoint()
				a = a + self.center.create_PSpoint()
				a = a + "\pstCircleOA["+self.params()+"]{"+self.center.psNom+"}{"+PsA.psNom+"}"
				return a
				# Some remarks :
				# Besoin d'un point sur le cercle pour le tracer avec \pstCircleOA,"")
				# La commande pscircle ne tient pas compte des xunit et yunit => inutilisable.
				#self.add_latex_line("\pscircle["+params+"]("+Cer.center.psNom+"){"+str(Cer.radius)+"}")
			else :
				PsA = self.get_point(self.angleI)
				PsB = self.get_point(self.angleF)
				a = PsA.create_PSpoint() + PsB.create_PSpoint()
				a = a+"\pstArcOAB[%s]{%s}{%s}{%s}"%(self.params(),self.center.psNom,PsA.psNom,PsB.psNom)
				return a

def SubstitutionMathPsTricks(fx):
	listeSubst = []
	listeSubst.append(["**","^"])
	listeSubst.append(["math.exp","2.718281828459045^"])
	listeSubst.append(["e^","2.718281828459045^"])
	for i in range(1,10):	
		listeSubst.append(["math.log"+str(i),str(0.43429448190325*math.log(i))+"*log"])
	listeSubst.append(["math.log","2.302585092994046*log"])		# Parce que \psplot[]{1}{5}{log(x)} trace le logarithme en base 10
									# Pour rappel, la formule est log_b(x)=log_a(x)/log_a(b)
	listeSubst.append(["math.pi","3.141592653589793"])
	listeSubst.append(["math.cosh","COSH"])
	listeSubst.append(["math.tan","TAN"])
	listeSubst.append(["math.sinh","SINH"])
	listeSubst.append(["math.sinc","SINC"])
	listeSubst.append(["math.",""])
	listeSubst.append(["log","2.302585092994046*log"])		# Parce que \psplot[]{1}{5}{log(x)} trace le logarithme en base 10
	a = fx
	for s in listeSubst :
		a = a.replace(s[0],s[1])
	return a

class phyFunction(object):
	def __init__(self,fun):
		var('x')
		self.sage = fun
		self.sageFast = self.sage._fast_float_(x)
		self.string = repr(self.sage)
		self.fx = self.string.replace("^","**")
		self.pstricks = SubstitutionMathPsTricks(self.fx)
		self.ListeSurface = []
		self.listeTests = []
		self.TesteDX = 0
		self.listeExtrema = []
		self.listeExtrema_analytique = []
		self._derivative = None
	def eval(self,xe):
		return numerical_approx(self.sageFast(xe))
	def inverse(self,y):
		""" returns a list of values x such that f(x)=y """
		listeInverse = []
		var('x')
		eq = self.sage(x) == y
		return CalculSage().solve_one_var([eq],x)
	def PointsNiveau(self,y):
		return [ Point(x,y) for x in self.inverse(y) ]
	def roots(self):
		""" return roots of the function as a list of Points. Some can miss ! """
		return self.PointsNiveau(0)
	def derivative(self):
		""" return the derivative of the function. The result is of type phyFunction """
		if self._derivative == None :
			self._derivative = phyFunction(self.sage.derivative())
		return self._derivative
	def get_point(self,x):		
		P = Point(float(x),self.eval(x))
		ca = self.derivative().eval(x) 
		P.advised_mark_angle=degree(atan(ca))+90
		return P
	#def Listeget_point(self,l):
	#	return [self.get_point(x) for x in l]
	def normal_vector(self,x):
		""" return a normalized normal vector to the graph of the function at x """
		ca = self.derivative().eval(x) 
		return Point(-ca,1).normalize().lie(self.get_point(x))		
	def VectorTangent(self,x):
		ca = self.derivative().eval(x)
		return Point(1,ca).normalize().lie(self.get_point(x))
	# Je donne une abcisse et une petite distance, et il retourne le point qui est sur la fonction, mais un peu décalé de cette distance dans la direction normale à la courbe.
	def get_normal_point(self,x,dy):
		""" return a point at distance dy in the normal direction of the point (x,f(x)) """
		vecteurNormal =  self.normal_vector(x)
		return self.get_point(x).translate(vecteurNormal.fix_size(dy))
	
	def get_regular_points(self,mx,Mx,dx):
		"""
		return a list of points regularly spaced (with respect to the arc length) on the curve x |-->(x,f(x))

		The points are given between the abcisses mx and Mx
		dx : the space between two points
		"""
		var('x')
		f1 = phyFunction(x)
		try :
			f2 = self.f		# Here, self can be of type «GraphOfAphyFunction»
		except AttributeError :
			f2 = self
		curve = ParametricCurve(f1,f2)
		return curve.get_regular_points(mx,Mx,dx)
	def get_wavy_points(self,mx,Mx,dx,dy):
		PIs = self.get_regular_points(mx,Mx,dx)
		Ps = [self.get_point(mx)]
		for i in range(0,len(PIs)) :
			Ps.append( self.get_normal_point(PIs[i].x, ((-1)**i)*dy ) )
		Ps.append(self.get_point(Mx))	
		return Ps
	def liste_extrema(self):
		if self.listeExtrema == []:
			self.extrema_analytique()
		return self.listeExtrema
	def ToutExtrema(self,mx,Mx,dx):
		min = self.get_point(mx)
		max = self.get_point(mx)
		for ex in list(xsrange(mx,Mx,dx,include_endpoint=true)):
			ey = self.eval(ex)
			if ey > max.y : max = Point(ex,ey)
			if ey < min.y : min = Point(ex,ey)
		self.listeExtrema.extend([min,max])
	# La méthode phyFunction.extrema_analytique() ajoute les solutions de f'(x)=0 à self.listeExtrema
	def extrema_analytique(self):
		print "Analytique"
		var('x')
		a = []
		listeSymbolicEquation = solve( [self.sage.diff(x)==0],[x] )
		for sol in listeSymbolicEquation :
			#s = sol[2]
			s = sol.right_hand_side()
			if "x" not in repr(s) :				# En attendant de trouver comment demander des solutions non implicites
				a.append(self.get_point(numerical_approx(s)))
		self.listeExtrema.extend(a)
	# Donne les extrema connus entre mx et Mx
	def extrema(self,mx,Mx):
		a = []
		for p in self.liste_extrema() :
			if p.x >= mx and p.x <= Mx :
				a.append(p)
		return a
	# Donne le maximum de la fonction entre mx et Mx. 
	def get_minmax_data(self,mx,Mx):
		return plot(self.sage,(mx,Mx)).get_minmax_data()
	def xmax(self,deb,fin):
		return self.get_minmax_data(deb,fin)['xmax']
	def xmin(self,deb,fin):
		return self.get_minmax_data(deb,fin)['xmin']
	def ymax(self,deb,fin):
		return self.get_minmax_data(deb,fin)['ymax']
	def ymin(self,deb,fin):
		return self.get_minmax_data(deb,fin)['ymin']
	def maximum_global(self,mx,Mx):
		max = self.liste_extrema()[0]
		for p in self.liste_extrema() :
			if p.y > max.y : max = p
		return max
	# Donne le minimum de la fonction entre mx et Mx. 
	def minimum_global(self,mx,Mx):
		min = self.get_point(mx)
		for p in self.liste_extrema() :
			print "candidat : %s" %p.Affiche()
			if p.y < min.y : min = p
		print min.Affiche()
		return min
	def tangente(self,x):
		ca = self.derivative().eval(x)
		A = self.get_point(x)
		Ad = Point( A.x+1,A.y+ca )
		Ag = Point( A.x-1,A.y-ca )
		return ( Segment(Ag,Ad) )
	# Note que une surface créée par self.AjouteSurface sera automatiquement tracée par la méthode TracephyFunction de psfigure.
	def AjouteSurface(self,mx,Mx):
		self.ListeSurface.append( SurfacephyFunction(self,mx,Mx) )
		# Ceci sont quelque réglages par défaut
		self.ListeSurface[-1].ChangeCouleur("blue")
		self.ListeSurface[-1].add_option("fillstyle=vlines,linestyle=dashed,linecolor=black")
	def graph(self,mx,Mx):
		return phystricks.GraphOfAphyFunction(self,mx,Mx)
	def __pow__(self,n):
		return phyFunction(self.sage**n)

class ParametricCurve(object):
	"""
	This class describes a parametric curve.

	You create a parametric curve by
		curve = ParamatricCurve(f1,f2)
	where f1 and f2 are phyFunction.

	The graph of curve with the parameter going from a to b is got by
		curve.graph(a,b)
	"""
	def __init__(self,f1,f2):
		if type(f1) is phyFunction : self.f1 = f1
		else : self.f1 = phyFunction(f1)
		if type(f2) is phyFunction : self.f2 = f2
		else : self.f2 = phyFunction(f2)

	# Le truc difficile avec le pstricks est que la syntaxe est  "f1(t) | f2(t)" avec t comme variable.
	#  C'est cela qui demande d'utiliser repr et la syntaxe f(x=t).
	def pstricks(self):
		var('t')
		return "%s | %s "%(SubstitutionMathPsTricks(repr(self.f1.sage(x=t)).replace("pi","3.1415")),  SubstitutionMathPsTricks(repr(self.f2.sage(x=t)).replace("pi","3.1415")) )
	def tangent_angle(self,llam):
		""""Return the angle of the tangent (gradient)"""
		dx=self.f1.derivative().eval(llam)
		dy=self.f2.derivative().eval(llam)
		ca=dy/dx
		return atan(ca)
	def derivative(self):
		return ParametricCurve(self.f1.derivative(),self.f2.derivative())
	def get_point(self,llam):
		"""Return the point on the curve for the value llam of the parameter."""
		P = Point( self.f1.eval(llam),self.f2.eval(llam) )
		P.advised_mark_angle=degree(self.tangent_angle(llam))+90	# Here I cannot use the method normal_vector due to recursion.
		return P
	def tangent_vector(self,llam):
		"""
		returns the tangent vector to the curve for the value of the parameter given by llam.
		   The vector is normed to 1.
		"""
		initial = self.get_point(llam)
		return Vector( initial,Point(initial.x+self.derivative().f1.eval(llam),initial.y+self.derivative().f2.eval(llam)) ).normalize()
	def normal_vector(self,llam):
		"""
		Return the normal vector to the curve for the value llam of the parameter.
		   The vector is normed to 1.
		"""
		return self.tangent_vector(llam).orthogonal()
	def get_minmax_data(self,deb,fin):
		return parametric_plot( (self.f1.sage,self.f2.sage), (deb,fin) ).get_minmax_data()
	def xmax(self,deb,fin):
		return self.get_minmax_data(deb,fin)['xmax']
	def xmin(self,deb,fin):
		return self.get_minmax_data(deb,fin)['xmin']
	def ymax(self,deb,fin):
		return self.get_minmax_data(deb,fin)['ymax']
	def ymin(self,deb,fin):
		return self.get_minmax_data(deb,fin)['ymin']
	def get_normal_point(self,x,dy):
		vecteurNormal =  self.normal_vector(x)
		return self.get_point(x).translate(self.normal_vector.fix_size(dy))
	def arc_length(self,mll,Mll):
		""" numerically returns the arc length on the curve between the value mll and Mll of the parameter """
		g = sqrt( self.f1.derivative().sage**2+self.f2.derivative().sage**2 )
		return numerical_integral(g,mll,Mll)[0]
	def get_regular_parameter(self,mll,Mll,dl):
		""" 
		returns a list of values of the parameter such that the corresponding points are equally spaced by dl.
		Here, we compute the distance using the method arc_length.
		"""
		prop_precision = float(dl)/100 		# precision of the interval
		fp = self.derivative()
		minDll = abs(Mll-mll)/1000
		ll = mll
		PIs = []
		while ll < Mll :
			v = math.sqrt( (fp.f1.eval(ll))**2+(fp.f2.eval(ll))**2 )
			if v == 0 :
				print "v=0"
				Dll = minDll
			Zoom = 1
			Dll = dl/v
			grand = Mll
			petit = ll
			#print "RECHERCHE d'un DÉBUT"
			#print "grand", grand
			#print "petit", petit
			if abs(self.arc_length(ll,ll+Dll)) > dl :
				grand = ll+Dll
				while abs(self.arc_length(ll,petit)) > dl :
					petit = (grand+petit)/2
			else :
				petit = ll+Dll
				while abs(self.arc_length(ll,grand)) < dl :
					grand = 2*grand - ll
			ell = (petit+grand)/2
			while abs(self.arc_length( ll, ell )-dl) > prop_precision:
				if prop_precision == 0:
					print "prop_precision is zero. Something sucks. You probably want to launch me in an infinite loop. I'm going to crash now; please contact my labour union."
					print "dl=",dl
					raise ValueError
				ell = (grand+petit)/2
				if self.arc_length(ll,ell) > dl :
					grand = ell
				else :
					petit = ell
			ll = (petit+grand)/2
			if ll < Mll :
				PIs.append( ll )
		return PIs
	def get_regular_points_old(self,mll,Mll,dl):
		return [self.get_point(ll) for ll in self.get_regular_parameter_old(mll,Mll,dl)]
	def get_regular_points(self,mll,Mll,dl):
		return [self.get_point(ll) for ll in self.get_regular_parameter(mll,Mll,dl)]
	def get_wavy_points(self,mll,Mll,dl,dy):
		"""
		Return a list of points which do a wave around the parametric curve.
		"""
		PAs = self.get_regular_parameter(mll,Mll,dl)
		PTs = []
		for i in range(0,len(PAs)) :
			llam = float(PAs[i])
			PTs.append( self.get_point(llam)+self.normal_vector(llam).fix_size(dy)*(-1)**i )
		PTs.append(self.get_point(Mll))
		return PTs
	def graph(self,mx,Mx):
		return phystricks.GraphOfAParametricCurve(self,mx,Mx)

class Nuage_de_Points(object):
	def __init__(self):
		self.listePoints = []
	def ajoute_point(self,p):
		self.listePoints.append(p)

def PolarVector(P,r,theta):
	"""
	returns a vector on the base point P (class Point) of length r angle theta (degree)
	"""
	alpha = radian(theta)
	return Vector(P, Point(P.x+r*math.cos(alpha),P.y+r*math.sin(alpha)) )

class BoundingBox(object):
	def __init__(self,dbg=GeometricPoint(0,0),dhd=GeometricPoint(0,0)):
		self.bg = dbg
		self.hd = dhd
	def NO(self):
		return Point(self.bg.x,self.hd.y)
	def NE(self):
		return self.hd
	def SO(self):
		return self.bg
	def SE(self):
		return Point(self.hd.x,self.bg.y)
	def coordinates(self):
		return self.bg.coordinates()+self.hd.coordinates()
	def Affiche(self):
		return self.coordinates()
	def tailleX(self):
		return self.hd.x-self.bg.x
	def tailleY(self):
		return self.hd.y-self.bg.y
	def extraX_left(self,l):
		"""Enlarge the bounding box of a length l on the left"""
		self.bg.x=self.bg.x-l
	def extraX_right(self,l):
		"""Enlarge the bounding box of a length l on the right"""
		self.hd.x=self.hd.x+l
	def extraX(self,l):
		"""Enlarge the bounding box of a length l on both sides"""
		self.extraX_left(l)
		self.extraX_right(l)

	def AddX(self,x):
		self.bg = Point( min(self.bg.x,x), self.bg.y )
		self.hd = Point( max(self.hd.x,x), self.hd.y )
	def AddY(self,y):
		self.bg = Point( self.bg.x, min(self.bg.y,y) )
		self.hd = Point( self.hd.x, max(self.hd.y,y) )
	def AddPoint(self,P):
		self.AddX(P.x)
		self.AddY(P.y)
	def AddSegment(self,seg):
		self.AddPoint(seg.I)
		self.AddPoint(seg.F)
	def AddCircle(self,Cer):
		raise AttributeError,"method AddCircle is depreciated"
		self.AddX(Cer.radius.x+Cer.radius)
		self.AddX(Cer.radius.x-Cer.radius)
		self.AddY(Cer.radius.y+Cer.radius)
		self.AddY(Cer.radius.y-Cer.radius)
	def AddArcCircle(self,Cer,deb,fin):
		self.AddX(Cer.xmin(deb,fin))
		self.AddY(Cer.ymin(deb,fin))
		self.AddX(Cer.xmax(deb,fin))
		self.AddY(Cer.ymax(deb,fin))
	def AddBB(self,bb):
		self.AddPoint(bb.bg)
		self.AddPoint(bb.hd)
	def add_graph(self,graphe,pspict):
		try :
			self.AddBB(graphe.bounding_box(pspict))
		except TypeError :
			self.AddBB(graphe.bounding_box(pspict))
	def AddCircleBB(self,Cer,xunit,yunit):
		"""
		Ajoute un cercle déformé par les xunit et yunit; c'est pratique pour agrandir la BB en taille réelle, pour
		faire rentrer des lettres dans la bounding box, par exemple.
		"""
		self.AddPoint( Point( Cer.center.x-Cer.radius/xunit,Cer.center.y-Cer.radius/yunit ) )
		self.AddPoint( Point( Cer.center.x+Cer.radius/xunit,Cer.center.y+Cer.radius/yunit ) )
	def AddAxes(self,axes,xunit,yunit):
		self.AddPoint( axes.BB.bg )
		self.AddPoint( axes.BB.hd )
		#self.AddCircleBB( Circle(axes.C,0.7),xunit,yunit )			# This is to make enter the graduation of the axes.
	def AddphyFunction(self,fun,deb,fin):
		raise AttributeError,"method AddphyFunction is depreciated"
		self.AddY(fun.ymin(deb,fin))
		self.AddY(fun.ymax(deb,fin))
		self.AddX(deb)
		self.AddX(fin)
	def AddParametricCurve(self,F,deb,fin):
		raise AttributeError,"method AddParametricCurve is depreciated"
		self.AddX(F.xmin(deb,fin))
		self.AddX(F.xmax(deb,fin))
		self.AddY(F.ymin(deb,fin))
		self.AddY(F.ymax(deb,fin))
	def enlarge_a_little(self,Dx,Dy,epsilonX,epsilonY):
		"""
		Essentially intended to the bounding box of a axis coordinate. 
		The aim is to make the axis slightly larger than the picture in such a way that all the numbers are written
		1. If a coordinate is integer multiple of epsilon, (say n), we enlarge to n+epsilon, so that the number n appears on the axis
		2. If a coordinate is non integer multiple, we enlarge to the next integer multiple (plus epsilon) so that the axis still has a number written
			further than the limit of the picture.
		The aim is to make the axes slightly bigger than their (Dx,Dy) in order the last graduation to be visible.
		"""
		self.bg.x = enlarge_a_little_low(self.bg.x,Dx,epsilonX)
		self.bg.y = enlarge_a_little_low(self.bg.y,Dy,epsilonY)
		self.hd.x = enlarge_a_little_up(self.hd.x,Dx,epsilonX)
		self.hd.y = enlarge_a_little_up(self.hd.y,Dy,epsilonY)
	def bounding_box(self,pspict):
		return self
	def copy(self):
		return BoundingBox(self.bg.copy(),self.hd.copy())
	def __str__(self):
		return "(%s,%s),(%s,%s)"%tuple(str(x) for x in(self.bg.x,self.bg.y,self.hd.x,self.hd.y))
