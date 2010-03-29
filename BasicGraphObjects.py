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
"""

from SmallComputations import *

class ListeNomsPoints(object):
	"""
	This class serves to give a psname to my points. 

	TODO : use a real iterator.
	"""
	def __init__(self):
		self.donne = 1000
	def suivant(self):
		self.donne = self.donne + 1
		a = ["AutoPt"]
		s = str(self.donne)
		for c in s:
			a.append(chr(int(c)+97))
		return "".join(a)

class Point(object):
	"""
	This is a point. Each point comes with a name given by a class attribute.
	"""
	NomPointLibre = ListeNomsPoints()

	def __init__(self,x,y):
		if type(x) == str : print "Attention : x est du type str"
		if type(y) == str : print "Attention : y est du type str"
		self.x = float(x)
		self.y = float(y)
		self.psNom = Point.NomPointLibre.suivant()

	# La méthode EntierPlus place le point sur les coordonnées entières plus grandes (ou égales) à les siennes.
	def EntierPlus(self):
		Px = self.x
		Py = self.y
		self.x = CalculEntierPlus(Px)
		self.y = CalculEntierPlus(Py)

	# La méthode EntierMoins place le point sur les coordonnées entières plus petites (ou égales) à les siennes.
	def EntierMoins(self):
		Px = self.x
		Py = self.y
		self.x = CalculEntierMoins(Px)
		self.y = CalculEntierMoins(Py)

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
		return Vector(Point(0,0), self)

	def norme(self):
		return Segment( Point(0,0),self ).longueur
	# La méthode normalize voit le point comme un vecteur partant de zéro, et en donne le vecteur de taille 1
	def normalize(self):
		return self*(1/self.norme())
	def code(self,params="PointSymbol=none,PointName=none"):
		"""
		Return the code if one wants to put the point with the options params (string).
		It is typically used with PointSymbol=none,PointName=none in order to create the code of
		more complex objects.
		"""
		return "\pstGeonode["+params+"]"+self.coordinates()+"{"+self.psNom+"}"

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

class Nuage_de_Points(object):
	def __init__(self):
		self.listePoints = []
	def ajoute_point(self,p):
		self.listePoints.append(p)

class Circle(object):
	def __init__(self,C,r):
		self.centre = C
		self.rayon = r
		self.maxima = "("+str(self.centre.x)+"-x)^2+("+str(self.centre.y)+"-y)^2-"+str(self.rayon)+"^2"+"=0"
	def parametric_curve(self):
		var('x')
		f1 = phyFunction(self.centre.x+self.rayon*cos(x))
		f2 = phyFunction(self.centre.y+self.rayon*sin(x))
		return ParametricCurve(f1,f2)

	def get_point(self,theta):
		return Point(self.centre.x+self.rayon*math.cos(radian(theta)), self.centre.y+self.rayon*math.sin(radian(theta)) )
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


class Segment(object):
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
			self.equation is a list [a,b,c] which corresponds to the cartesian equation
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
		returns the cartesian equation of the line as a instance of the sage's class
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
		#a = self.I*(1-p)
		#b = self.F*p
		#return a+b
		return self.I*(1-p) + self.F*p
	def milieu(self):
		#return Point( (self.I.x+self.F.x)/2, (self.I.y+self.F.y)/2 )
		return self.proportion(0.5)

	def Vector(self):
		return Vector(self.I,self.F)
	def normal_vector(self):
		"""
		returns a normal vector at the center of the segment
		"""
		if self.vertical :
			return Point(-1,0).Vector().lie(self.milieu())
		else :
			P = Point(-self.coefficient,1)
			return P.Vector().normalize().lie(self.milieu())
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
		vI = Vector(self.milieu(),self.I)
		vF = Vector(self.milieu(),self.F)
		I = vI.add_size(lI).F
		F = vI.add_size(lF).F
		return Segment(I,F)
	def fix_size(self,l):
		vI = Vector(self.milieu(),self.I)
		vF = Vector(self.milieu(),self.F)
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

	def code(self,params):
		#pspict.BB.AddSegment(self)
		#a.append(pspict.CodeAddPoint(self.I))	# Ces lignes étaient du temps où la méthode code prenait une pspict en argument.
		#a.append(pspict.CodeAddPoint(self.F))
		a = []
		a.append(self.I.code())
		a.append(self.F.code())
		a.append("\pstLineAB["+params+"]{"+self.I.psNom+"}{"+self.F.psNom+"}")
		return "\n".join(a)

class Vector(object):
	def __init__(self,a,b):
		self.Segment = Segment(a,b)
		self.I = self.Segment.I
		self.F = self.Segment.F
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

	def __mul__(self,coef):
		return Vector(self.I,Point(self.I.x+self.Dx*coef,self.I.y+self.Dy*coef))
	def __div__(self,coef):
		return self * (1/coef)


