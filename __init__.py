# -*- coding: utf8 -*-

###########################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2009-2010
# email: moky.math@gmail.com

"""
A collection of tools for building LaTeX-pstricks figures with python.
"""

from __future__ import division
from sage.all import *
import numpy
#import commands, os, math
import math, sys

class global_variables(object):
	def __init__(self):
		self.eps_exit = False
		self.pdf_exit = False
		self.pstricks_language = True
		self.list_exits = ["eps","pdf"]
	def special_exit(self):
		for sortie in self.list_exits :
			if self.__getattribute__(sortie+"_exit"):
				return True
		return False

class Fichier(object):
	def __init__ (self, filename):
		self.NomComplet = filename
		self.chemin = self.NomComplet				
		self.nom = os.path.basename(self.chemin)
	def open_file(self,opt):
		self.file = open(self.chemin,opt)			
	def close_file(self):
		self.file.close()
	def write(self,texte,opt):				
		""" Write in a file following the option """
		self.open_file(opt)
		self.file.write(texte)
		self.close_file()
	def contenu(self):
		r"""
		Return the list of the lines of the file, inlcuding the \n at the end of each line.
		"""
		self.open_file("r")
		c = [l for l in self.file]
		self.close_file()
		return c

class ListeNomsPoints(object):
	def __init__(self):
		self.donne = 1000
	def suivant(self):
		self.donne = self.donne + 1
		a = ["AutoPt"]
		s = str(self.donne)
		for c in s:
			a.append(chr(int(c)+97))
		return "".join(a)

NomPointLibre = ListeNomsPoints()

class CalculSage(object):
	# I cannot merge the function for solving with respect to one or more variables because Sage returns like that:
	# If 1 and 2 are the solutions for one variable : [x == 1,x==2]
	# If (1,2) and (3,4) are solutions of a two variable equation : [ [x==1,y==2],[x==3,y==4] ]
	# The list nesting structure is really different. Do I have to read the doc ?
	def solve_one_var(self,eqs,var):
		"""
		Solve the equations with respect to the given variable

		Returns a list of numerical values.
		"""
		liste = solve(eqs,var,explicit_solutions=True)
		a = []
		for soluce in liste :	
			a.append(numerical_approx(soluce.rhs()))
		return a
	def solve_more_vars(self,eqs,*vars):
		"""
		Solve the equations with respect to the given variables

		Returns a list like [  [1,2],[3,4] ] if the solutions are (1,2) and (3n4)
		"""
		liste = solve(eqs,vars,explicit_solutions=True)
		a = []
		for soluce in liste :	
			sol = []
			for variable in soluce :
				sol.append( numerical_approx(variable.rhs()))
			a.append(sol)
		return a

# Cette classe est ce qui reste de l'ancienne classe maxima(). Elle est juste encore utile tant que je ne trouve pas comment faire des divisions euclidiennes avec Sage.
class CalculPolynome(object):
	# La méthode calcul donne la sortie de maxima en brut. Pour traiter l'information, il faudra encore des tonnes de manipulations, et on peut déjà en mettre dans filtre
	def calcul(self,ligne,filtre):
		commande =  "maxima --batch-string=\"display2d:false; "+ligne+";\""+filtre 
		return commands.getoutput(commande)
	# reponse donne ce que calcule donne, après extraction de la partie intéressante, c'est à dire prise de grep o2 et enlevure de "o2" lui-même.
	def reponse(self,ligne):
		ligne = self.calcul(ligne,"|grep o2")
		return ligne.replace("(%o2)","").replace(" ","")

	def DivPoly(self,P,Q):
		l = []
		m = []
		for i in range(0,P.deg-Q.deg+1):
			ligne =  "coeff( expand( divide("+P.maxima+","+Q.maxima+"))[1],x,"+str(P.deg-Q.deg-i)+")"
			l.append(  int( self.reponse(ligne) ) )
		for i in range(0,Q.deg+1): 
			ligne =  "coeff( expand( divide("+P.maxima+","+Q.maxima+"))[2],x,"+str(Q.deg-i)+")"
			m.append( int (self.reponse(ligne) ) )
		return [Polynome(l),Polynome(m)]

	def MulPoly(self,P,Q):
		l = []
		for i in range(0,P.deg+Q.deg+1):
			ligne = "coeff( expand(("+P.maxima+")*("+Q.maxima+")),x,"+str(P.deg+Q.deg-i)+")"    
			l.append( int( self.reponse(ligne)) )
		return Polynome(l)

	# Cette méthode est exactement la même que la précédente, au changement près de * vers +. Y'a peut être moyen de factoriser ...
	def sub_polynome(self,P,Q):
		l = []
		for i in range(0,P.deg+Q.deg+1):
			ligne =   "coeff( expand(("+P.maxima+")-("+Q.maxima+")),x,"+str(P.deg+Q.deg-i)+")"    
			rep = self.reponse(ligne) 
			if rep <> "":
				l.append(int(rep))
		return Polynome(l)

class BoundingBox(object):
	def __init__(self,dbg,dhd):
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
		self.AddX(Cer.centre.x+Cer.rayon)
		self.AddX(Cer.centre.x-Cer.rayon)
		self.AddY(Cer.centre.y+Cer.rayon)
		self.AddY(Cer.centre.y-Cer.rayon)
	def AddArcCircle(self,Cer,deb,fin):
		self.AddX(Cer.xmin(deb,fin))
		self.AddY(Cer.ymin(deb,fin))
		self.AddX(Cer.xmax(deb,fin))
		self.AddY(Cer.ymax(deb,fin))
	def AddBB(self,bb):
		self.AddPoint(bb.bg)
		self.AddPoint(bb.hd)

	# Ajoute un cercle déformé par les xunit et yunit; c'est pratique pour agrandir la BB en taille réelle, pour
	# faire rentrer des lettres dans la bounding box, par exemple.
	def AddCircleBB(self,Cer,xunit,yunit):
		self.AddPoint( Point( Cer.centre.x-Cer.rayon/xunit,Cer.centre.y-Cer.rayon/yunit ) )
		self.AddPoint( Point( Cer.centre.x+Cer.rayon/xunit,Cer.centre.y+Cer.rayon/yunit ) )
	def AddAxes(self,axes,xunit,yunit):
		self.AddPoint( axes.BB.bg )
		self.AddPoint( axes.BB.hd )
		self.AddCircleBB( Circle(axes.C,0.7),xunit,yunit )
	def AddphyFunction(self,fun,deb,fin):
		#self.AddCircle( Circle(Point(deb,fun.eval(deb)),0.3))
		#self.AddCircle( Circle(Point(fin,fun.eval(fin)),0.3))
		self.AddY(fun.ymin(deb,fin))
		self.AddY(fun.ymax(deb,fin))
		self.AddX(deb)
		self.AddX(fin)
	def AddParametricCurve(self,F,deb,fin):
		self.AddX(F.xmin(deb,fin))
		self.AddX(F.xmax(deb,fin))
		self.AddY(F.ymin(deb,fin))
		self.AddY(F.ymax(deb,fin))

	def enlarge_a_little(self):
		"""
		Essentially intended to the bounding box of a axis coordinate. 
		The aim is to make the axis slightly larger than the picture in such a way that all the numbers are written
		1. If a coordinate is integer (say n), we enlarge to n+0.5, so that the number n appears on the axis
		2. If a coordinate is non integer, we enlarge to the next integer (plus an epsilon) so that the axis still has a number written
			further than the limit of the picture.
		"""
		epsilon = 0.2
		self.bg.x = enlarge_a_little_low(self.bg.x,epsilon)
		self.bg.y = enlarge_a_little_low(self.bg.y,epsilon)
		self.hd.x = enlarge_a_little_up(self.hd.x,epsilon)
		self.hd.y = enlarge_a_little_up(self.hd.y,epsilon)
		
def enlarge_a_little_up(x,epsilon):
	"""
	see the description of the function enlarge_a_little of the class BoundingBox.
	This function makes the job for one number.
	"""
	if int(x) == x:
		return x+0.5
	else : 
		return CalculEntierPlus(x)+epsilon
		
def enlarge_a_little_low(x,epsilon):
	"""
	see the description of the function enlarge_a_little of the class BoundingBox.
	This function makes the job for one number.
	"""
	if int(x) == x:
		return x-0.5
	else : 
		return CalculEntierMoins(x)-epsilon

def SubGridArray(mx,Mx,Dx,num_subX):
	""" Provides the values between mx and Mx such that there are num_subX-1 numbers between two integer separated by Dx """
	dx = float(Dx)/num_subX
	valeurs = []
	base = MultipleLower(mx,Dx)
	for i in range(0,ceil((Mx-mx)*num_subX/Dx)+3*num_subX):		# The range is designed by purpose to be sure to be too wide
		tentative = base + float(i)*dx
		if (tentative < Mx) and (tentative > mx) and ( i % num_subX <> 0 ) :
			valeurs.append(tentative)
	return valeurs

# Cette définition retourne l'entier plus grand ou égal à un nombre donné
def CalculEntierPlus(x):
	t = x
	if t <> int(t):
		if t < 0 : t = t-1
		t = int(t) + 1
		return float(t)
	else : return x

# Cette définition retourne l'entier plus grand ou égal à un nombre donné
def CalculEntierMoins(x):
	t = x
	if t <> int(t):
		if t < 0 : t = t-1
		t = int(t)
		return float(t)
	else : return x


def MultipleLower(x,m):
	""" Provides the bigger multiple of m which is lower or equal to x"""
	base = floor(x)
	for i in range(0,m+1):
		tentative = float(base - i)
		if tentative/m - round(tentative/m)==0:
			return int(tentative)

def MultipleBigger(x,m):
	""" Provides the lower multiple of m which is bigger or equal to x"""
	base = ceil(x)
	for i in range(0,m+1):
		tentative = float(base + i)
		if tentative/m - round(tentative/m)==0:
			return int(tentative)

class coordinatesPolaires(object):
	def __init__(self,r,theta):
		self.r = r
		self.theta = theta

def PolarPoint(r,theta):
	return Point(r*math.cos(radian(theta)),r*math.sin(radian(theta)))

def PointToPolaire(P):
	"""
	The polar coordinates are given in radian.
	"""
	r = P.norme()
	if P.x == 0:
		if P.y > 0:
			alpha = math.pi/2
		if P.y < 0:
			alpha = -math.pi/2
		if P.y == 0 : 			# Convention : l'angle pour le point (0,0) est 0.
			alpha = 0
	else :
		alpha = arctan(P.y/P.x)
	if (P.x < 0) and (P.y == 0) :
		alpha = math.pi
	if (P.x < 0) and (P.y > 0) :
		alpha = alpha + math.pi
	if (P.x < 0) and (P.y < 0 ) :
		alpha = alpha +math.pi
	#theta = degree(alpha)
	return coordinatesPolaires(r,alpha)


class Point(object):
	def __init__(self,x,y):
		if type(x) == str : print "Attention : x est du type str"
		if type(y) == str : print "Attention : y est du type str"
		self.x = float(x)
		self.y = float(y)
		self.psNom = NomPointLibre.suivant()

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

	# translate un point selon le vecteur v.
	def translate(self,v):
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
		if type(v) == Vector :
			dx = v.Dx
			dy = v.Dy
		if type(v) == Point :
			dx = v.x
			dy = v.y
		return Point(self.x+dx,self.y+dy)
	def __mul__(self,r):
		return Point(r*self.x,r*self.y)

class Nuage_de_Points(object):
	def __init__(self):
		self.listePoints = []
	def ajoute_point(self,p):
		self.listePoints.append(p)

def radian(theta):
	return theta*math.pi/180
def degree(alpha):
	return 180*alpha/math.pi

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


# Donne le carré de la distance entre P et Q
def Distance_sq(P,Q):
	return (P.x-Q.x)**2+(P.y-Q.y)**2

# Donne la distance entre P et Q
def Distance(P,Q):
	return math.sqrt(Distance_sq(P,Q))

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

def PolarVector(P,r,theta):
	"""
	returns a vector on the 
	base point P (class Point)
	of length r 
	angle theta (degree)
	"""
	alpha = radian(theta)
	return Vector(P, Point(P.x+r*cos(alpha),P.y+r*sin(alpha)) )
		
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

class MesureLongueur(Segment):			# Sert à faire des doubles flèches pour indiquer des distances
	def __init__(self,a,b):
		Segment.__init__(self,a,b)

class Triangle(object):
	def __init__(self,A,B,C):
		self.A = A
		self.B = B
		self.C = C

class Rectangle(object):
	def __init__(self,A,B):
		self.bg = A
		self.hd = B
		self.bd = Point( self.hd.x,self.bg.y )
		self.hg = Point( self.bg.x,self.hd.y )
		self.centre = Segment(self.bg,self.hd).milieu()

class Waviness(object):
	"""
	This class contains the informations about the waviness of a curve. It takes as argument a GraphOfAFunction and the parameters dx, dy of the wave.
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
	def __init__(self,graphe,dist,angle,mark):
		self.graphe = graphe
		self.dist = dist
		self.angle = angle
		self.mark = mark

class Parameters(object):
	def __init__(self):
		self.color = ""
		self.symbol = ""
		self.style = ""
	def add_to_options(self,opt):
		if self.color <> "":
			opt.add_option("linecolor=%s"%str(self.color))
		if self.style <> "":
			opt.add_option("linestyle=%s"%str(self.style))
		if self.symbol <> "":
			opt.add_option("PointSymbol=%s"%str(self.symbol))

class GraphOfAnObject(object):
	""" This class is supposed to be used to create other "GraphOfA..." by inheritance. It is a superclass. """
	def __init__(self,obj):
		self.obj = obj
		self.parameters = Parameters()
		self.wavy = False
		self.waviness = None
		self.options = Options()
		self.marque = False
		self.add_option("linecolor=black")
		self.add_option("linestyle=solid")
	def wave(self,dx,dy):					# dx is the wave length and dy is the amplitude
		self.wavy = True
		self.waviness = Waviness(self,dx,dy)
	def mark(self,dist,angle,mark):
		self.marque = True
		self.mark = Mark(self,dist,angle,mark)
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

class GraphOfAPoint(GraphOfAnObject,Point):
	def __init__(self,point):
		GraphOfAnObject.__init__(self,point)
		Point.__init__(self,point.x,point.y)
		self.point = self.obj
		self.add_option("PointSymbol=*")
	#def conclude_params(self):
	#	GraphOfAnObject.conclude_params(self)
	#def params(self):
	#	self.conclude_params()
	#	return self.options.code()

class GraphOfASegment(GraphOfAnObject):
	def __init__(self,seg):
		GraphOfAnObject.__init__(self,seg)
		self.seg = self.obj
		self.I = self.seg.I
		self.F = self.seg.F
	#def params(self):
	#	self.conclude_params()
	#	return self.options.code()

class GraphOfAVector(GraphOfAnObject):
	def __init__(self,vect):
		GraphOfAnObject.__init__(self,vect)
		self.vector = self.obj
	#def params(self):
	#	self.conclude_params()
	#	return self.options.code()

class GraphOfACircle(GraphOfAnObject):
	def __init__(self,circle):
		GraphOfAnObject.__init__(self,circle)
		self.circle = self.obj
		self.angleI = 0
		self.angleF = 2*pi		# By default, the circle is drawn between the angles 0 and 2pi.
	#def params(self):
	#	self.conclude_params()
	#	return self.options.code()


class GraphOfAFunction(GraphOfAnObject):
	"""
	Cette classe est une abstraction pour la méthode TracephyFunction. Lorqu'on utilise TracephyFunction, on passe f,mx,Mx,params.
	La class GraphOfAFunction permet d'abstaire la donné de f,mx,Mx et des paramètres. Elle contient en outre des méhtodes pour
		personnaliser les graphes plus facilement, et surtout sans savoir la syntaxe de pstricks.
	"""
	def __init__(self,f,mx,Mx):
		GraphOfAnObject.__init__(self,f)
		self.f = self.obj
		self.mx = mx
		self.Mx = Mx
		self.plotpoints	= 100				# Par défaut, on fait 100 points
		self.parameters.color = "blue"				# Modification with respect to the attribute in GraphOfAnObject
	def params(self):
		self.conclude_params()
		self.add_option("plotpoints=%s"%str(self.plotpoints))
		return self.options.code()

class GraphOfAParametricCurve(GraphOfAnObject):
	def __init__(self,curve,llamI,llamF):
		GraphOfAnObject.__init__(self,curve)
		self.curve = self.obj
		self.llamI = llamI
		self.llamF = llamF
		self.parameters.color = "blue"
		self.plotstyle = "curve"
		self.plotpoints = "1000"
	def params(self):
		self.conclude_params()
		self.add_option("plotpoints=%s"%str(self.plotpoints))
		self.add_option("plotstyle=%s"%str(self.plotstyle))
		return self.options.code()

def Graph(X,arg1=None,arg2=None):
	"""This function is supposed to be only used by the end user."""
	if type(X) == phyFunction :
		return GraphOfAFunction(X,arg1,arg2)
	if type(X) == ParametricCurve :
		return GraphOfAParametricCurve(X,arg1,arg2)
	if type(X) == Segment :
		return GraphOfASegment(X)
	if type(X) == Vector :
		return GraphOfAVector(X)
	if type(X) == Circle :
		return GraphOfACircle(X)
	if type(X) == Point :
		return GraphOfAPoint(X)
	
class GrapheDesphyFunctions(object):
	def __init__(self,L):
		self.liste_GraphOfAFunction = L
	def add_option(opt):
		for gf in self.liste_fonctions :
			gf.add_option(opt)

def SubstitutionMathMaxima(exp):
	a = exp
	for i in range(1,10):
		a = a.replace("math.log"+str(i),"log("+str(i)+")^(-1)*log")
	return a.replace("math.log","log").replace("math.tan","tan").replace("math.pi","%pi").replace("math.","")

# Juste pour rappel, la commande \ValeurAbsolue est définie automatiquement dans la pspicure.
# Juste pour re-rappel, j'ai commenté la ligne qui faisait ça.
def SubstitutionMathLaTeX(exp):
	a = exp
	for i in range(1,10):
		a = a.replace("math.log"+str(i),"\\log_{"+str(i)+"}")
	return a.replace("math.tan","\\tan").replace("math.log","\\ln").replace("math.","\\").replace("*"," ")

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
		self.maxima = SubstitutionMathMaxima(self.fx).replace("**","^")
		self.latex = SubstitutionMathLaTeX(self.fx.replace("**","^").replace("(","{(").replace(")",")}").replace("(x)","x").replace("(-x)","-x")).replace("\\abs","\ValeurAbsolue")
		if "{(" in self.latex and ")}" in self.latex :
			self.latex = self.latex.replace("{(","{").replace(")}","}")
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
		return Point(float(x),self.eval(x))
	def Listeget_point(self,l):
		return [self.get_point(x) for x in l]
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
	
	def __pow__(self,n):
		return phyFunction(self.sage**n)

class ParametricCurve(object):
	def __init__(self,f1,f2):
		if type(f1) is phyFunction : self.f1 = f1
		else : self.f1 = phyFunction(f1)
		if type(f2) is phyFunction : self.f2 = f2
		else : self.f2 = phyFunction(f2)

	# Le truc difficile avec le pstricks est que la syntaxe est  "f1(t) | f2(t)" avec t comme variable.
	#  C'est cela qui demande d'utiliser repr et la syntaxe f(x=t).
	def pstricks(self):
		var('t')
		return "%s | %s "%(SubstitutionMathPsTricks(repr(self.f1.sage(x=t))),  SubstitutionMathPsTricks(repr(self.f2.sage(x=t))) )

	def derivative(self):
		return ParametricCurve(self.f1.derivative(),self.f2.derivative())
	def get_point(self,llam):
		return Point( self.f1.eval(llam),self.f2.eval(llam) )
	def tangent_vector(self,llam):
		"""
		returns the tangent vector to the curve for the value of the parameter given by llam.
		   The vector is normed to 1.
		"""
		initial = self.get_point(llam)
		return Vector( initial,Point(initial.x+self.derivative().f1.eval(llam),initial.y+self.derivative().f2.eval(llam)) ).normalize()
	def normal_vector(self,llam):
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
		prop_precision = dl /100 		# precision of the interval
		#prop_precision = 0.0001
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
					#print "petit",petit
			else :
				petit = ll+Dll
				while abs(self.arc_length(ll,grand)) < dl :
					grand = 2*grand - ll
					#print "grand",grand
			ell = (petit+grand)/2
			while abs(self.arc_length( ll, ell )-dl) > prop_precision:
				#print "grand ",grand," petit :",petit
				#print self.arc_length(ll,ell), prop_precision
				ell = (grand+petit)/2
				if self.arc_length(ll,ell) > dl :
					grand = ell
				else :
					petit = ell
			ll = (petit+grand)/2
			if ll < Mll :
				PIs.append( ll )
				#print "j'ai trouvé ",ll
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
		#PAs.append(mll)
		PTs = []
		#print "les paramètres sont "
		#print PAs
		for i in range(0,len(PAs)) :
			llam = float(PAs[i])
			PTs.append( self.get_point(llam)+self.normal_vector(llam).fix_size(dy)*(-1)**i )
		PTs.append(self.get_point(Mll))
		return PTs

		
class SurfacephyFunction(object):
	def __init__(self,f,mx,Mx):
		self.mx = mx
		self.Mx = Mx
		self.f = f
		self.options = Options()
		self.add_option("fillstyle=vlines,linestyle=dashed,linecolor=black")
		self.ChangeCouleur("cyan")							# Cela donne quelque réglages par défaut
	def add_option(self,opt):
		self.options.add_option(opt)
	def ChangeCouleur(self,coul):
		self.add_option("fillcolor="+coul+",linecolor="+coul+",hatchcolor="+coul)

class SurfaceEntrephyFunctions(object):
	def __init__(self,f,g,mx,Mx):
		self.mx = mx
		self.Mx = Mx
		self.f = f
		self.g = g
		self.options = Options()
		self.add_option("linestyle=none,fillstyle=vlines,linecolor=black")
		self.ChangeCouleur("cyan")							# Cela donne quelque réglages par défaut
	def add_option(self,opt):
		self.options.add_option(opt)
	def ChangeCouleur(self,coul):
		self.add_option("fillcolor="+coul+",linecolor="+coul+",hatchcolor="+coul)


class Grid(object):
	"""
	ATTRIBUTES
		self.BB : the bounding box of the grid : its size.
		self.options : customisation.
		self.Dx,self.Dy : the step of main subdivision along X and Y directions (have to be integers)
		self.num_subX, self.num_subY : number of subdivision within each integer interval. When it is zero, there are no subdivisions.
		self.draw_border : a boolean which says if the border of the grid has to be drawn (default=False)

		self.options : the options for the grid
		self.main_horizontal : an objet of type GraphOfASegment from the opions of which the main horizontal lines
					will be customized.
					As an example, in order to have red main horizontal lines:
					grid.main_horizontal.parameters.color = "red"

	METHODS
		self.drawing() : returns a list of objects to be drawn. This is typically instances of GraphOfASegment
	DESCRIPTION
		An instance is a grid to appear on the picture.
		If draw_border is True, the border is drawn. 
		Then, it draws lines on the integer values of X and Y with a step given by Dx and Dy. It begins at the closest integer
			from the lower left corner. It finishes before to reach the upper right corner if Dx or Dy is not an integer divisor of 
			the size.
		Subdivisions are drawn following the same rule.
	"""
	def __init__(self,bb):
		self.BB = bb
		self.options = Options()
		self.add_option({"Dx":1,"Dy":1})		# Default values, have to be integer.
		self.Dx = self.options.DicoOptions["Dx"]
		self.Dy = self.options.DicoOptions["Dy"]
		self.num_subX = 2
		self.num_subY = 2
		self.draw_border = False
		self.main_horizontal = GraphOfASegment(Segment(Point(0,1),Point(1,1)))	# Ce segment est bidon, c'est juste pour les options de tracé.
		self.main_horizontal.parameters.color="gray"
		self.main_horizontal.parameters.style = "solid"
		self.main_vertical = GraphOfASegment(Segment(Point(0,1),Point(1,1)))	
		self.main_vertical.parameters.color="gray"
		self.main_vertical.parameters.style = "solid"
		self.sub_vertical = GraphOfASegment(Segment(Point(0,1),Point(1,1)))	
		self.sub_vertical.parameters.color="gray"
		self.sub_vertical.parameters.style = "dotted"
		self.sub_horizontal = GraphOfASegment(Segment(Point(0,1),Point(1,1)))	
		self.sub_horizontal.parameters.color="gray"
		self.sub_horizontal.parameters.style = "dotted"
		self.border = GraphOfASegment(Segment(Point(0,1),Point(1,1)))	
		self.border.parameters.color = "gray"
		self.border.parameters.style = "dotted"
	def add_option(self,opt):
		self.options.add_option(opt)

	def optionsTrace(self):
		return self.options.sousOptions(OptionsStyleLigne())
	def optionsParams(self):
		return self.options.sousOptions(["Dx","Dy"])
	def drawing(self):
		#print "Je passe"
		a = []
		# ++++++++++++ Le bord ++++++++ 
		if self.draw_border :
			if self.BB.SO().x <> int(self.BB.SO().x):
				#print "SOx"
				seg = Segment( self.BB.SO(),self.BB.NO() )
				S = GraphOfASegment(seg)
				S.merge_options(self.border)
				a.append(S)
			if self.BB.NE().y <> int(self.BB.NE().y):
				#print "NEy"
				seg = Segment( self.BB.NO(),self.BB.NE() )
				S = GraphOfASegment(seg)
				S.merge_options(self.border)
				a.append(S)
			if self.BB.NE().x <> int(self.BB.NE().x):
				#print "NEx"
				seg = Segment( self.BB.NE(),self.BB.SE() )
				S = GraphOfASegment(seg)
				S.merge_options(self.border)
				a.append(S)
			if self.BB.SO().y <> int(self.BB.SO().y):
				#print "SOy"
				seg = Segment( self.BB.SO(),self.BB.SE() )
				S = GraphOfASegment(seg)
				S.merge_options(self.border)
				a.append(S)
		# ++++++++++++ The vertical sub grid ++++++++ 
		if self.num_subX <> 0 :
			for x in  SubGridArray(self.BB.SO().x,self.BB.SE().x,self.Dx,self.num_subX) :
					seg = Segment( Point(x,self.BB.SO().y),Point(x,self.BB.NO().y) )
					S = GraphOfASegment(seg)
					S.merge_options(self.sub_vertical)
					a.append(S)
		# ++++++++++++ The horizontal sub grid ++++++++ 
		if self.num_subY <> 0 :
			for y in  SubGridArray(self.BB.SO().y,self.BB.NO().y,self.Dy,self.num_subY) :
					seg = Segment( Point(self.BB.SO().x,y),Point(self.BB.SE().x,y) )
					S = GraphOfASegment(seg)
					S.merge_options(self.sub_horizontal)
					a.append(S)
		# ++++++++++++ Les lignes horizontales principales ++++++++ 
		for y in range(MultipleBigger(self.BB.SO().y,self.Dy),MultipleLower(self.BB.NO().y,self.Dy)+1,self.Dy):
			seg = Segment( Point(self.BB.bg.x,y),Point(self.BB.hd.x,y) )
			S = GraphOfASegment(seg)
			S.merge_options(self.main_horizontal)
			a.append(S)
		# ++++++++++++ Les lignes verticales principales ++++++++
		for x in range(MultipleBigger(self.BB.SO().x,self.Dx),MultipleLower(self.BB.SE().x,self.Dx)+1,self.Dx):
			seg = Segment( Point(x,self.BB.SO().y),Point(x,self.BB.NO().y) )
			S = GraphOfASegment(seg)
			S.merge_options(self.main_vertical)
			a.append(S)
		return a
	def code(self):
		print "This is a depreciated feature ... I think the program is going to crash now :)"


# Des axes sont donnés par le point central et sa BB (Bounding Box).
# Les axes peuvent s'ajuster pour contenir toute une série d'objets. Le début et la fin des axes sont donc une BoundingBox
# Note qu'en pratique, c'est mieux d'utiliser la grille par défaut de la pspicture, et de la tracer avec pspicture.DrawDefaultAxes. 
#	Il devrait être assez exceptionnel d'avoir une instance explicite de la classe Axes dans le programme principal.
class Axes(object):
	"""
	ATTRIBUTS
		self.grille :		la grille associée
		self.Dx, self.Dy :	l'intervalle avec laquelle des marques sont faites sur les axes
	MÉTHODES
		self.AjouteGrid	Crée une grille avec des options par défaut
		self.add_label_X	Ajoute un label X (idem pour Y)
		self.add_option	Ajoute une option. Ceci doit être fait avec la syntaxe pstricks
		self.no_graduation		Pas de marques sur les axes
		self.AjustephyFunction	Ajuste les axes sur une fonction donnée. Ceci ne devrait pas être utilisé si on utilise la grille par défaut de pspict, cf. TraceGridDefaut
	"""
	def __init__(self,C,bb):
		self.C = C						# Attention : celui-ci a changé, avant c'était O, mais maintenant c'est C.
		self.BB = bb
		self.BB.AddPoint( Point(C.x-0.5,C.y-0.7) )		# Celle-ci est pour tenir compte des chiffres écrits sur les axes X et Y
		self.options = Options()
		self.grille = Grid(self.BB)
		self.IsLabelX = 0
		self.IsLabelY = 0
		self.N=Point( self.C.x,self.BB.hd.y )
		self.S=Point( self.C.x,self.BB.bg.y )
		self.O=Point( self.BB.bg.x,self.C.y )
		self.E=Point( self.BB.hd.x,self.C.y )
		self.SO=Point(self.O.x,self.S.y)
		self.NE=Point(self.E.x,self.N.y)
		self.SE=Point(self.E.x,self.S.y)
		self.NO=Point(self.O.x,self.N.y)
		self.Dx = 1
		self.Dy = 1						# Ce sont les valeurs par défaut.
		self.arrows = "->"
	
	# Cette méthode ne devrait pas être utilisée parce qu'il n'y a pas de grille associée à un système d'axes.
	def AjouteGrid(self):
		self.IsGrid = 1
		self.grille.add_option("gridlabels=0")
		self.grille.add_option("subgriddiv=0")
		self.grille.add_option("griddots=5")

	def add_label_X(self,dist,angle,marque):
		self.IsLabelX = 1
		self.LabelX = marque
		self.DistLabelX = dist
		self.AngleLabelX = angle

	def add_label_Y(self,dist,angle,marque):
		self.IsLabelY = 1
		self.LabelY = marque
		self.DistLabelY = dist
		self.AngleLabelY = angle
		# Je crois que le label n'est pas encore prit en compte dans la BB.

	def add_option(self,opt):
		self.options.add_option(opt)
	def no_graduation(self):
		self.add_option("labels=none,ticks=none")

	# AjustephyFunction sert à élargir les axes pour ajuster une fonction entre deux abcisses.
	def AjustephyFunction(self,f,mx,Mx):
		self.BB.AddphyFunction(f,mx,Mx)
	def AjusteCircle(self,Cer):
		self.BB.AddCircle(Cer)
	def AjusteGraphephyFunction(self,gf):
		self.AjustephyFunction(gf.f,gf.mx,gf.Mx)
	def code(self):
		# Ce petit morceau évite d'avoir le bord bas gauche des axes sur une coordonnée entière, ce qui fait en général moche. Cela se fait ici et non dans __init__, parce que les limites des axes peuvent changer, par exemple en ajustant une fonction.
		# Note qu'il faut donner ses coordonnées à la grille avant, sinon, au moment de s'ajuster sur une valeur entière, la grille perd en fait toute une unité.
		self.add_option("Dx=%s"%str(self.Dx))
		self.add_option("Dy=%s"%str(self.Dy))
		bgx = self.BB.bg.x
		bgy = self.BB.bg.y
		if self.BB.bg.x == int(self.BB.bg.x): 
			bgx = self.BB.bg.x + 0.01
		if self.BB.bg.y == int(self.BB.bg.y):
			bgy = self.BB.bg.y +0.01
		self.BB.bg = Point (bgx,bgy)

		#return "\psaxes["+self.options.code()+"]{"+self.arrows"}"+self.C.coordinates()+self.BB.coordinates()
		return "\psaxes[%s]{%s}%s%s"%(self.options.code(),self.arrows,self.C.coordinates(),self.BB.coordinates())
			
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
		if type(opt) == str:
			for op in opt.split(","):
				s = op.split("=")
				self.DicoOptions[s[0]] = s[1]
		else:
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

# La classe Description_Dynkin décrit la mathématique de Dynkin : elle n'a pas les informations sur les sigles qu'on veut mettre sur les racines.
# Le paramètre ll est une liste de "o" et "*" suivant que la racine ait une norme maximale ou non (cerle plein ou vide dans Dynkin)
# __init__ donne des valeurs par défaut. Par exemples les racines sont mises en ligne droite, et la matrice d'adjacence est nulle.
class Dynkin(object):
	def __init__(self,descr,deco):
		self.description = descr
		self.decoration = deco

class Decoration_Dynkin(object):
	def __init__(self,descr):
		n = len(descr.remplissure)
		self.distMark = []
		self.angleMark = []
		self.visMark = []
		for i in range(0,n):
			self.angleMark.append(90)
			self.distMark.append(0.3)
			self.visMark.append("")
	def PlaceMarque(self,n,dist,angle):
		self.distMark[n] = dist
		self.angleMark[n] = anlge
	def DefMarque(self,n,marque):
		self.visMark[n] = marque

# Un 4 dans une matrice d'adjacence signifie une ligne en pointillé
class Description_Dynkin(object):
	def __init__(self,ll):
		els = list(ll)
		n = len(els)
		lAdj = int(float(n)/2)+1
		#print n
		self.remplissure = []
		for i in range(0,lAdj):
			self.remplissure.append(els[2*i])
		#print self.remplissure
		self.ronds = []
		for i in range(0,n):
			self.ronds.append( Point(i,0) )
		self.Adjacence = []
		for i in range(0,lAdj):	
			z = []
			for j in range(0,lAdj) : z.append(0)
			self.Adjacence.append(z)
		for i in range(0,int(float(n)/2)):
			if ll[2*i+1] == "-": self.Adjacence[i][i+1] = 1
			if ll[2*i+1] == "=": self.Adjacence[i][i+1] = 2
			if ll[2*i+1] == ".": self.Adjacence[i][i+1] = 4

	# n sera le nombre de segments entre les points i et j. C'est relié aux angles entre les racines (cf matrice de Cartan).
	def AjouteSegment(self,i,j,n):
		self.Adjacence[i][j] = n
	def PlacePoint(self,num,P):
		self.ronds[num] = P

class Young(object):
	def __init__(self,T):
		self.diagramme = T

# Une instance de cette classe est un terme à l'intérieur d'un polynôme. Dans 7x^2+3x+9, le second terme est "+3x" et non simplement "3x". C'est à dire que ça tient compte du contexte dans lequel le terme est pour s'afficher.
# Note qu'un terme qui vaut zéro est noté "+0".
class TermeDansPolynome(object):
	def __init__(self,P,n):
		# La liste l crée le code LaTeX, tandis que la liste m crée le code maxima.
		l = []
		m = []
		#print "Je cherche le degré "+str(n)+" dans "+str(P.tab)
		cof = P.coeff[n]
		# Bienvenue au pays du bricolage !!
		if cof == 0:
			l.append("+0")
		if cof <> 0:
			if cof > 0: 
				if n <> P.deg :	
					l.append("+")
					m.append("+")
					if (cof <> 1) or (n == 0) :
						l.append(str(cof))
					m.append(str(cof))
						
				if n == P.deg :
					m.append(str(cof))
					if cof <> 1:
						l.append(str(cof))

			if cof < 0 :
				if cof <> -1:
					l.append(str(cof))
					m.append(str(cof))
				if (cof == -1) and (n <> 0):
					l.append("-")
					m.append("-1")
			if (n <> 0) :
				l.append("x")
				m.append("*x")
				if n <> 1:
					l.append("^"+str(n))
					m.append("^"+str(n))
			if (n == 0) and (cof == -1):
				l.append("-1")
				m.append("-1")

		self.latex = "".join(l)
		self.maxima = "".join(m)

		self.polynome = P
		self.deg = n

	def polynome_seul(self):
		t = [self.polynome.coeff[self.deg]]
		t.extend( [0]*self.deg )
		return Polynome(t)
		

# La classe Polynome prend un tableau et le considère comme un polynôme.
class Polynome(object):
	def __init__(self,P):

		# Si le tableau donné commence par des zéros, il faut les enlever (ça arrive si le polynôme est le résultat d'une addition)
		self.tab = P
		while (self.tab[0] == 0) and (len(self.tab) > 1) : self.tab = self.tab[1:]

		self.deg = len(self.tab)-1
		self.coeff = []
		for i in range(0,self.deg+1) : self.coeff.append(self.tab[self.deg-i])
		
		# self.liste_non_nuls donne la liste des termes non nuls du polynôme.
		lnn = []
		for i in reversed(range(0,self.deg)):
			if self.coeff[i] <> 0:
				lnn.append(self.terme(i))
		self.liste_non_nuls = lnn

		l = []
		for i in reversed(range(0,self.deg+1)):
			terme = self.terme(i).latex
			if terme <> "+0":
				l.append(terme)
		self.latex = "".join(l)
		m = []
		for i in reversed(range(0,self.deg+1)):
			terme = self.terme(i).maxima
			if terme <> "0":
				m.append(terme)
		self.maxima = "".join(m)
		if self.tab == [0] : 
			self.latex = "0"
			self.maxima = "0"

		#for i in range(0,len(self.tab)) :
		if (self.latex <> "0") and (self.coeff[0] == 0 ):
			j = 0
			#print self.coeff
			#print self.latex
			while self.coeff[j] == 0 : j = j+1
			self.minDeg = j
		else : self.minDeg = 0

	def terme(self,degre):
		return TermeDansPolynome(self,degre)

	# Surcharge des opérations courantes pour les polynômes
	def __mult__(self,P):
		return CalculPolynome().MulPoly(self,P)
	def __sub__ (self,P):
		return CalculPolynome().sub_polynome(self,P)

class DivEuclide(object):
	def __init__(self,A,B):
		self.A = A
		self.B = B
		self.reponse = CalculPolynome().DivPoly(A,B)[0]
		self.reste = CalculPolynome().DivPoly(A,B)[1]
		#print "Je divise "+A.latex+" par "+B.latex+". La réponse est : "+self.reponse.latex
		#print "Le degré de "+self.A.latex+" est "+str(self.A.deg)


	# self.reponse_etapes(n) donne un polynome dont les termes non nuls sont les n premiers non nuls de la réponse.
	# Une bonne idée serait de mettre ça comme une méthode de la classe Polynome.
	def reponse_etapes(self,nombre_etapes):
		p = []
		n = 0
		i = self.reponse.deg
		while n < nombre_etapes :
			if self.reponse.coeff[i] <> 0:
				if p == [] : deg = i
				p.append(self.reponse.coeff[i])
				n = n+1
				i = i-1
		p.extend( [0]*(deg-Polynome(p).deg) )
		return Polynome(p)

	# Donne le code LaTeX de n pas de la division euclidienne.
	def code(self,nombre_etapes):
		l = []

		l.append("\\begin{array}{")

		# Poser la division écrite
		for i in range(0,self.A.deg+1) : l.append("c")
		l.append("|l}\n")
		l.append(self.ligne_inter(self.A))
		l.append("	"+self.B.latex+"\\\\\n")
		#l.append("\cline{"+str(self.A.deg+2)+"-"+str(self.A.deg+2+self.B.deg)+"}")
		l.append("\cline{"+str(self.A.deg+2)+"-"+str(self.A.deg+2)+"}")
		l.append("\n")
		
		# Calculer les étapes
		aDiv = self.A
		deg_courant = self.reponse.deg
		for i in range(0,nombre_etapes):		
			while (self.reponse.coeff[deg_courant] == 0) and (deg_courant > 0) : deg_courant = deg_courant - 1		# Trouver le suivant qui n'est pas nul dans la réponse
			aSub = self.reponse.terme(deg_courant).polynome_seul()*self.B
			l.append(self.ligneSub(aSub,nombre_etapes))
			print "Je soustrait "+aDiv.maxima+" - "+aSub.maxima
			aDiv = aDiv - aSub
			print "et le résultat est : "+aDiv.latex
			l.append(self.ligne_inter(aDiv))
			l.append("\\\\\n")
			deg_courant = deg_courant - 1

		# Fermer les environements et conclure.
		l.append("\end{array}")
		return "".join(l)

	# Donne la ligne dans le array qui montre ce qu'il reste à diviser. Il ne met pas le \\ parce qu'il est aussi utilisé au moment de poser
	#   la division écrite.
	def ligne_inter(self,aDiv):
		l = []
		for i in range(0,self.A.deg-aDiv.deg) : l.append("	&	")
		for i in reversed(range(0,aDiv.deg+1)):
			l.append(aDiv.terme(i).latex+"	&	")
		print "Le poly à caser est "+aDiv.latex
		print "".join(l)
		return "".join(l)

	# Donne la ligne dans le array qui consiste à soustraire.
	# Il y a deux cas particuliers : la première ligne contient aussi la réponse de la division,
	# et la dernière ligne ne met pas de & après la parenthèse (Je crois que je pourrais ne pas traiter ce cas particulier)
	def ligneSub(self,aSub,nombre_etapes):
		print "J'essaye de faire rentrer "+aSub.latex
		l = []
		for i in range(aSub.deg,self.A.deg):
			l.append("	&	")
		l.append("-(")

		print aSub.latex+" a degré "+str(aSub.deg)+" et minimum "+str(aSub.minDeg)+"."
		for i in reversed(range(aSub.minDeg,aSub.deg+1)):
			l.append(aSub.terme(i).latex)
			if (i == aSub.minDeg) and (aSub.deg > self.B.deg ) : 
				l.append(")	&	")
			if (i == aSub.minDeg) and (aSub.deg == self.B.deg ) and (aSub.deg <> self.A.deg) : 
				l.append(")")
			if (i == aSub.minDeg) and (aSub.deg == self.B.deg ) and (aSub.deg == self.A.deg) : 
				l.append(")	&	")
			if i <> aSub.minDeg : l.append("	&	")
		for i in range(0,aSub.minDeg): l.append("\\vdots	&	")
		if aSub.deg == self.A.deg : l.append(self.reponse_etapes(nombre_etapes).latex)
		l.append("\\\\\n")
		cd = self.A.deg - aSub.deg + 1
		cf = cd + aSub.deg
		l.append("\cline{"+str(cd)+"-"+str(cd+aSub.deg-aSub.minDeg)+"}")

		l.append("\n")
		return "".join(l)

	def write_the_file(self,nom,n):								# Nous sommes dans la classe DivEuclide
		nombre_etapes = n
		if nombre_etapes > self.reponse.deg : nombre_etapes = self.reponse.deg + 1
		self.fichier = Fichier(nom)
		self.fichier.open_file("w")
		self.fichier.file.write(self.code(nombre_etapes))
		self.fichier.file.close()
		
# Pour demander l'intersection avec une fonction, utiliser la fonction CircleInterphyFunction.
def CircleInterLigne(Cer,Ligne):
	if type(Ligne) == phyFunction :
		soluce = maxima().solve( [Cer.maxima,"y="+Ligne.maxima],["x","y"] )
	else :
		soluce = maxima().solve( [Cer.maxima,Ligne.maxima],["x","y"] )
	#print Ligne.maxima
	#print soluce
	if len(soluce) == 0:
		#print "Pas d'intersection"
		return [Point(0,0),Point(0,0)]
	if len(soluce) == 1:
		#print "Une d'intersection"
		return [Point(soluce[0][0],soluce[0][1]),Point(0,0)]
	if len(soluce) == 2:
		#print "Deux d'intersection"
		return [Point(soluce[0][0],soluce[0][1]),Point(soluce[1][0],soluce[1][1])]

def CircleInterphyFunction(Cer,f):
	return CircleInterLigne(Cer,f)

def phyFunctionInterphyFunction(f,g):
	var('x,y')
	eq1 = y == f.sage(x)
	eq2 = y == g.sage(x)
	soluce = CalculSage().solve( [eq1,eq2],[x,y] )
	a = []
	print "Nombre de solutions : "+str(len(soluce))
	for s in soluce :
		a.append( Point(s[0],s[1]) )
	return a

def LineInterLine(l1,l2):
	eq1 = l1.sage_equation()
	eq2 = l2.sage_equation()
	soluce = CalculSage().solve_more_vars( [eq1,eq2],x,y )
	s = soluce[0]
	return Point( s[0],s[1] )
	
	
def GenericFigure(nom):
	"""
	This function returns a figure with some default values. It creates coherent label, file name and prints the lines to be appended in the LaTeX file to include the figure.
	"""
	label = "LabelFig"+nom
	caption = "\CaptionFig"+nom
	nFich = "Fig_"+nom+".pstricks"
	print "The result is on the figure \\ref{"+label+"}"
	print "\\newcommand{"+caption+"}{<+mettre le texte+>}"
	print "\\input{Fig_"+nom+".pstricks}"
	#return  figure(caption,label,REP+"/"+nFich)
	return  figure(caption,label,nFich)

# Une figure est le but ultime de ce script. Une figure est une suite de subfigures, lesquelles sont destinées à être essentiellement des pspictures.
class figure(object):
	def __init__(self,caption,label,fich):
		self.caption = caption
		self.label = label
		self.xunit = 1
		self.yunit = 1
		self.code = []
		self.SSfigures = []
		self.fichier = Fichier (fich)

		add_latex_line_entete(self)

		self.add_latex_line("\\begin{figure}[ht]")
		#self.add_latex_line("\\newcommand{\ValeurAbsolue}[1]{\left| #1 \\right| }")
		self.add_latex_line("\centering")
	# Note qu'il est préférable d'utiliser les commandes de dilatation avant de commencer à composer la pspicture,
	# parce que la BoundingBox doit aussi tenir compte de choses écrites en taille réelle.
	def dilatation_X(self,fact):
		""" Makes a dilatation of the whole picture in the X direction. A contraction if the coefficient is lower than 1 """
		self.xunit = self.xunit * fact
	def dilatation_Y(self,fact):
		self.yunit = self.yunit * fact
	def dilatation(self,fact):
		""" dilatations or contract that picture in both directions with the same coefficient """
		self.dilatation_X(fact)
		self.dilatation_Y(fact)

	def AjouteSSfigure(self,ssFig):
		self.SSfigures.append(ssFig)
	def add_pspicture(self,pspict):
		self.add_latex_line(pspict.contenu())			# Here, what is added depends on --eps
	# La différence entre add_latex_line et IncrusteLigne, c'est que la deuxième permet de la mettre où on veut.
	def add_latex_line(self,ligne):
		self.code.append(ligne+"\n")
	def IncrusteLigne(self,ligne,n):
		self.code[n:n]=ligne+"\n"
	def AjouteCode(self,liste_code):
		self.code.extend(liste_code)

	def conclude(self):
		if not globals.special_exit() :
			self.IncrusteLigne("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+"}\n",2)
		for f in self.SSfigures :
			self.add_latex_line("\subfigure["+f.caption+"]{%")
			self.AjouteCode(f.code)
			self.add_latex_line("}					% Fermeture de la sous-figure "+str(self.SSfigures.index(f)+1))
			self.add_latex_line("%")
			
		self.add_latex_line("\caption{"+self.caption+"}\label{"+self.label+"}")
		self.add_latex_line("\end{figure}")
		self.contenu = "".join(self.code)

	def write_the_file(self):					# Nous sommes dans la classe figure.
		self.fichier.open_file("w")
		self.fichier.file.write(self.contenu)
		self.fichier.file.close()
			
# Le \subfigure[caption]{ ne se met pas dans le code de la classe subfigure parce que dans la classe figure, je numérote les sous-figures.
# Typiquement, une sousfigure sera juste créée en ajoutant une pspicture d'un coup, et puis c'est tout.
class subfigure(object):
	def __init__(self,caption,label):
		self.caption = caption
		self.label = label
		self.code = []

	def add_latex_line(self,ligne):
		self.code.append(ligne)
	def AjouteCode(self,cod):
		self.code.extend(cod)

	def add_pspicture(self,psp):
		self.add_latex_line(psp.contenu())

class PspictureToOtherOutputs(object):
	"""
	contains the informations about the transformation of a pspicture into an eps/pdf file
	The method to produce the eps file is taken from the documentation of the package pst-eps, and from some fruitful discussions on fctt
		http://archive.cs.uu.nl/mirror/CTAN/graphics/pstricks/contrib/pst-eps/pst-eps-doc.pdf
		http://groups.google.fr/group/fr.comp.text.tex/browse_thread/thread/a5c4a67c457c46b8?hl=fr#

	self.file_for_eps is the file in which we will put the LaTeX code needed to create the eps file
	self.input_code_eps
	self.input_code_pdf	is the code to be input in the file that contains the picture. This is what replaces the pstricks code in the final figure.
	"""
	def __init__(self,pspict):
		self.pspict = pspict
		self.name = self.pspict.name
		self.file_for_eps = Fichier("Picture_%s-for_eps.tex"%(self.name))
		self.file_dvi = Fichier(self.file_for_eps.chemin.replace(".tex",".dvi"))
		self.file_eps = Fichier(self.file_dvi.chemin.replace(".dvi",".eps"))
		self.file_pdf = Fichier(self.file_eps.chemin.replace(".eps",".pdf"))
		self.input_code_eps = "\includegraphics{%s}"%(self.file_eps.nom)
		self.input_code_pdf = "\includegraphics{%s}"%(self.file_pdf.nom)
	def latex_code_for_eps(self):
		code = ["\documentclass{article}\n","\usepackage{pstricks,pst-eucl,pstricks-add}\n","\usepackage{pst-plot}\n","\usepackage{pst-eps}\n","\pagestyle{empty}\n"]
		# Allows to add some lines, like packages or macro definitions required. This is useful when one add formulas in the picture
		# that need packages of personal commands.
		code.append(self.pspict.specific_needs)		
		code.extend(["\\begin{document}\n","\\begin{TeXtoEPS}"])
		code.append(self.pspict.contenu_pstricks())
		code.extend(["\end{TeXtoEPS}\n","\end{document}\n"])
		print code
		return "".join(code)
	def create_eps_file(self):
		""" Creates an eps file by the chain latex/dvips """
		file_tex = self.file_for_eps
		file_tex.write(self.latex_code_for_eps(),"w")
		commande_e = "latex %s"%self.file_for_eps.chemin
		print "J'execute"
		print commande_e
		os.system(commande_e)
		commande_e = "dvips -E %s -o %s -q"%(self.file_dvi.chemin,self.file_eps.chemin)
		print "J'execute"
		print commande_e
		os.system(commande_e)
	def create_pdf_file(self):
		""" Creates a pdf file by the chain latex/dvips/epstopdf """
		self.create_eps_file()
		commande_e = "epstopdf %s --outfile=%s"%(self.file_eps.chemin,self.file_pdf.chemin)
		print "J'execute"
		print commande_e
		os.system(commande_e)

def add_latex_line_entete(truc):
	truc.add_latex_line("% This file is automatically generated by phystricks")
	truc.add_latex_line("%  see the documentation ")
	truc.add_latex_line("%  http://student.ulb.ac.be/~lclaesse/phystricks-doc.pdf ")
	truc.add_latex_line("%  See the projects phystricks and phystricks-doc at ")
	truc.add_latex_line("%  http://gitorious.org/~moky\n")

class LabelNotFound:
	def __init__(self,message):
		self.message=message

class pspicture(object):
	r"""
	self.pstricks_code contains the pstricks code of what has to be between \begin{pspicture} and \end{pspicture}. This is not the environment itself, neither the definition of xunit, yunit.
	self.contenu_pstricks() is the whole code including the x/yunit
	self.contenu_eps() contains the line to be added in order to include the eps file
	"""
 
	class _DrawVector(object):
		def __init__(self,picture,vect,params):
			self.picture = picture
			self.vect = vect
			self.params = params
			picture.BB.AddSegment(vect.Segment)
			picture.AddPoint(vect.I)
			picture.AddPoint(vect.F)
			picture.add_latex_line("\\ncline["+params+"]{->}{"+vect.Segment.I.psNom+"}{"+vect.Segment.F.psNom+"}")
		def MarkTheVector(self,dist,angle,marque):
				self.picture.DrawPoint(self.vect.F,"none",self.params).MarkThePoint(dist,angle,marque)
	class _DrawPoint(object):
		def __init__(self,picture,P,symbol,params):
			self.picture = picture
			self.P = P
			self.picture.BB.AddPoint(self.P)
			params_mettre = "PointSymbol="+symbol
			if params != "":
				params_mettre = params_mettre + ","+params
			self.picture.add_latex_line( P.code(params_mettre) )
		def MarkThePoint(self,dist,angle,marque):
			if self.P.psNom not in self.picture.listePoint :
				self.picture.AddPoint(self.P)
			self.picture.add_latex_line("\\rput("+self.P.psNom+"){\\rput("+str(dist)+";"+str(angle)+"){"+marque+"}}")
			# The next line was intended to take the size of the point into account in the bounding box.
			#    This was removed because it does not bring so much improvement, but it dramatically change the axis,
			#    since the axis are adjusted on the bounding box. In particular, the function enlarge_a_little makes no
			#    sense in the case where we have a totally artificial 0.1.
			#self.picture.BB.AddCircle( Circle(self.P,0.1) )

			#if marque <> "":
				# Le point M est à la place où le nom du point va arriver. Ensuite, j'élargis la BB pour contenir ce point et un petit voisinage.
			#	M = Point( self.P.x+dist*math.cos(angle)+0.1,self.P.y+dist*math.sin(angle) )
				#   Note que le cercle qui entoure la marque est tout à fait à la main et entoure à peu près une lettre
				# the following two lines were intended to take the mark into account in the BB. 
				# It was removed because of the same reason as the one explained above.
				#CM =  Circle(M,0.2) 
				#self.picture.BB.AddCircle( CM )

	class _TraceMesureLongueur(object):
		def __init__(self,picture,mesure,decale,params):
			self.picture = picture
			self.mesure = mesure
			if decale == 0 :
				self.signe = 0
			else :
				self.signe = decale/abs(decale)

			self.vect_normal = self.mesure.normal_vector()
			self.vect_decale = self.vect_normal.fix_size(decale)
			self.Seg = mesure.translate(self.vect_decale)		# self.Seg est le segment à tracer; il est décalé par rapport au "vrai"
			self.picture.AddPoint(self.Seg.I)
			self.picture.AddPoint(self.Seg.F)
			self.picture.BB.AddSegment(self.Seg)
			self.picture.add_latex_line("\\ncline["+params+"]{<->}{"+self.Seg.I.psNom+"}{"+self.Seg.F.psNom+"}")
		def MarqueMesureLongueur(self,dist,marque):
			milieu = self.Seg.milieu()
			if self.signe == -1 :
				dist = -dist
			vecteur_distance = self.vect_normal.fix_size(dist)
			polaires = vecteur_distance.polaires()
			self.picture.MarkThePoint(milieu,polaires.r,polaires.theta,"none",marque)

	def __init__(self,name="CAN_BE_A_PROBLEM_IF_TRY_TO_PRODUCE_EPS"):
		r"""
		A name is required for producing intermediate files. This is the case when one wants to produce eps/pdf files of one wants to 
		   make interactions with LaTeX (see pspict.get_counter_value).
		"""
		self.name = name		# self.name is used in order to name the intermediate files when one produces the eps file.
		self.pstricks_code = []
		self.specific_needs = ""	# See the class PspictureToOtherOutputs
		self.listePoint = []
		self.xunit = 1
		self.yunit = 1
		self.LabelSep = 1
		self.BB = BoundingBox(Point(1000,1000),Point(-1000,-1000))
		self.axes = Axes( Point(0,0), BoundingBox(Point(1000,1000), Point(-1000,-1000)) )
		self.grid = Grid(BoundingBox(Point(1000,1000), Point(-1000,-1000)) )
		# We add the "anchors" %GRID and %AXES in order to force the axes and the grid to be written at these places.
		#    see the functions DrawAxes and DrawGrid and the fact that they use IncrusteLigne

		add_latex_line_entete(self)

		self.add_latex_line("\psset{PointSymbol=none,PointName=none,algebraic=true}\n")
		self.add_latex_line("%GRID")	# A \n is automatically added.		
		self.add_latex_line("%AXES")
		self.add_latex_line("%OTHER STUFF")

	def get_counter_value(self,counter_name,default_value=0):
		"""
		return the value of the (LaTeX) counter <name> at this point of the LaTeX file 

		Makes LaTeX write the value of the counter in the auxiliary <file self.name>.aux, then reads the value in that file.
		(needs several compilations to work)
		"""

		# Make LaTeX write the value of the counter in a specific file
		interCounterName = "counter"+NomPointLibre.suivant()
		interWriteName = "write"+interCounterName
		interWriteFile = interWriteName+".pstricks.aux"
		self.add_latex_line(r"\newcounter{%s}"%interCounterName)
		self.add_latex_line(r"\setcounter{%s}{\value{%s}}"%(interCounterName,counter_name))
		self.add_latex_line(r"\newwrite\%s"%interWriteName)
		self.add_latex_line(r"\immediate\openout\%s=%s"%(interWriteName,interWriteFile))
		self.add_latex_line(r"\immediate\write\%s{%s:\arabic{%s}:}"%(interWriteName,interCounterName,interCounterName))
		self.add_latex_line(r"\immediate\closeout\%s"%interWriteName)

		# Read the file and return the value
		try :
			try :
				f=open(interWriteFile)
				text = f.read().split(":")
				return text[text.index(interCounterName)+1]			
			except IOError :
				raise LabelNotFound("Warning : the auxiliary file seems not to exist. Compile your LaTeX file.")
			except ValueError :
				raise LabelNotFound("Warning : the auxiliary file does not contain the searched label. Compile your LaTeX file.")
		except LabelNotFound,data:
			print data.message
			print "I' going to return the default value for counter %s, namely %s"%(counter_name,str(default_value))
			return default_value



	def DrawVector(self,vect,params):
		return self._DrawVector(self,vect,params)

	def TraceMesureLongueur(self,mesure,dist,params):
		return self._TraceMesureLongueur(self,mesure,dist,params)

	def dilatation(self,fact):
		self.dilatation_X(fact)
		self.dilatation_Y(fact)
	def dilatation_X(self,fact):
		self.xunit = self.xunit * fact
	def dilatation_Y(self,fact):
		self.yunit = self.yunit * fact
	def fixe_tailleX(self,l):
		self.dilatation_X(l/self.BB.tailleX())
	def fixe_tailleY(self,l):
		self.dilatation_Y(l/self.BB.tailleY())
		
	def add_latex_line(self,ligne):
		self.pstricks_code.append(ligne+"\n")
	def IncrusteLigne(self,ligne,n):
		self.pstricks_code[n:n]=ligne+"\n"

	# AddPoint sert à créer un point pstricks. Pour le faire apparaître effectivement, il faut utiliser DrawGraphOfAPoint.
	def CodeAddPoint(self,P):
		self.listePoint.append(P.psNom)
		return "\pstGeonode[PointSymbol=none,PointName=none]"+P.coordinates()+"{"+P.psNom+"}"
	def AddPoint(self,P):
		self.add_latex_line(self.CodeAddPoint(P))

	def TraceBB(self):
		self.TraceRectangle( Rectangle(self.BB.bg,self.BB.hd), "linecolor=cyan")

	# Ici, typiquement, symbol sera "*" et params sera vide.
	def DrawPoint(self,P,symbol,params):
		return self._DrawPoint(self,P,symbol,params)

	def TraceNuage_de_Points(self,nuage,symbol,params):
		self.add_latex_line("% ---------Nuage de point--------")
		for P in nuage.listePoints :
			self.DrawPoint(P,symbol,params)

	def MarqueAngle(self,A,B,C,label,params):
		self.add_latex_line("\pstMarkAngle["+params+"]{"+A.psNom+"}{"+B.psNom+"}{"+C.psNom+"}{"+label+"}")

	def TraceSurfacephyFunction(self,surf):
		mx = surf.mx
		Mx = surf.Mx
		f = surf.f
		opt = surf.options
		A = Point(mx,0)
		B = Point(Mx,0)
		X = f.get_point(mx)
		Y = f.get_point(Mx)
		self.BB.AddPoint(A)
		self.BB.AddPoint(B)
		self.BB.AddphyFunction(f,mx,Mx)
		self.add_latex_line("\pscustom["+opt.code()+"]{")
		self.add_latex_line("\psline"+A.coordinates()+X.coordinates())
		self.add_latex_line("\psplot{"+str(mx)+"}{"+str(Mx)+"}{"+f.pstricks+"}")
		self.add_latex_line("\psline"+Y.coordinates()+B.coordinates())
		self.add_latex_line("}")
	def TraceSurfaceEntrephyFunction(self,surf):
		mx = surf.mx
		Mx = surf.Mx
		f = surf.f
		g = surf.g
		opt = surf.options
		self.BB.AddphyFunction(f,mx,Mx)
		self.BB.AddphyFunction(g,mx,Mx)
		self.add_latex_line("\pscustom["+opt.code()+"]{")
		self.add_latex_line("\psplot[plotstyle=curve]{"+str(mx)+"}{"+str(Mx)+"}{"+f.pstricks+"}")
		self.add_latex_line("\psplot[liftpen=1]{"+str(Mx)+"}{"+str(mx)+"}{"+g.pstricks+"}")
		self.add_latex_line("}")

	def TracephyFunction(self,fun,min,max,params):
		# The use of numerical_approx is intended to avoid strings like "2*pi" in the final pstricks code.
		deb = numerical_approx(min)	
		fin = numerical_approx(max)
		self.BB.AddphyFunction(fun,deb,fin)
		for surf in fun.ListeSurface:
			self.TraceSurfacephyFunction(surf)
		self.add_latex_line("\psplot["+params+"]{"+str(deb)+"}{"+str(fin)+"}{"+fun.pstricks+"}")

	def DrawGraph(self,graphe,N=None):
		# If n is not None, it is the number of the line where the code has to be put. This is used by DrawGrid
		if type(graphe) == GraphOfAFunction :
			self.DrawGraphOfAFunction(graphe)
		if type(graphe) == GraphOfAParametricCurve :
			self.DrawGraphOfAParametricCurve(graphe)
		if type(graphe) == GraphOfASegment :
			self.DrawGraphOfASegment(graphe,N=N)
		if type(graphe) == GraphOfAVector :
			self.DrawGraphOfAVector(graphe)
		if type(graphe) == GraphOfACircle :
			self.DrawGraphOfACircle(graphe)
		if type(graphe) == GraphOfAPoint :
			self.BB.add_graph(graphe)
			self.add_latex_line(graphe.code())
		if type(graphe) == Grid :
			self.DrawGrid(graphe)

	def DrawGraphOfAPoint(self,graphe):
		p = graphe.point
		self.BB.AddPoint(p)
		self.add_latex_line( p.code(graphe.params()) )
		if graphe.marque :
			mark = graphe.mark
			if p.psNom not in self.listePoint :
				self.AddPoint(p)
			self.add_latex_line("\\rput(%s){\\rput(%s;%s){%s}}"%(p.psNom,str(mark.dist),str(mark.angle),str(mark.mark)))


	def DrawGraphOfASegment(self,graphe,N=None):
		if graphe.wavy == False :
			self.DrawSegment(graphe.seg,graphe.params(),N=N)
		if graphe.wavy == True :
			waviness = graphe.waviness
			self.DrawWavySegment(graphe.seg,waviness.dx,waviness.dy,graphe.params(),N=N)
	def DrawGraphOfAVector(self,graphe):
		if graphe.marque == False :
			self.DrawVector(graphe.vector,graphe.params())
		if graphe.marque == True :
			mark = graphe.mark
			self.DrawVector(graphe.vector,graphe.params()).MarkTheVector(mark.dist,mark.angle,mark.mark)

		def MarkTheVector(self,dist,angle,marque):
				self.picture.DrawPoint(self.vector.F,"none",self.params).MarkThePoint(dist,angle,marque)

	def DrawGraphOfACircle(self,graphe):
		if graphe.wavy == False :
			if graphe.angleI == 0 and graphe.angleF == 2*pi :
				self.TraceCircle(graphe.circle,graphe.params())
			else :
				self.TraceArcCircle(graphe.circle,graphe.angleI,graphe.angleF,graphe.params())
		else :
			waviness = graphe.waviness
			alphaI = radian(graphe.angleI)
			alphaF = radian(graphe.angleF)
			curve = graphe.circle.parametric_curve()
			G = GraphOfAParametricCurve(curve,alphaI,alphaF)
			G.add_option(graphe.params())
			# The two following lines are a pitty. If I add some properties, I have to change by hand...
			G.parameters.style = graphe.parameters.style
			G.parameters.color = graphe.color
			G.wave(waviness.dx,waviness.dy)
			self.DrawGraph(G)


	def DrawGraphOfAFunction(self,graphe):
		if graphe.wavy :			
			waviness = graphe.waviness
			self.TracephyFunctionOndule(graphe.f,waviness.mx,waviness.Mx,waviness.dx,waviness.dy,graphe.params())
		else :
			self.TracephyFunction(graphe.f,graphe.mx,graphe.Mx,graphe.params())
	def DrawGraphOfAParametricCurve(self,graphe):
		if graphe.wavy == False :
			self.TraceCourbeParametrique(graphe.curve,graphe.llamI,graphe.llamF,graphe.params())
		else:
			waviness = graphe.waviness
			self.TraceCourbeParametriqueOndule(graphe.curve,graphe.llamI,graphe.llamF,waviness.dx,waviness.dy,graphe.params())

	def TraceGrapheDesphyFunctions(self,liste_gf):
		for gf in liste_gf.liste_GraphOfAFunction:
			self.DrawGraphOfAFunction(gf)
	def TraceCourbeParametrique(self,f,mx,Mx,params):
		self.BB.AddParametricCurve(f,mx,Mx)
		self.add_latex_line("\parametricplot[%s]{%s}{%s}{%s}" %(params,str(mx),str(Mx),f.pstricks()))
	def DrawSegment(self,seg,params,N=None):
		self.BB.AddSegment(seg)			# Il me semble que j'avais viré cette ligne.
		code = seg.code(params)
		if N == None :
			self.add_latex_line(code)
		else :
			self.IncrusteLigne(code,N)

	def DrawGrid(self,grid):
		# The difficulty is that the grid has to be draw first, while most of time it is given last because of the bounding box.
		self.BB.AddBB(grid.BB)
		for element in grid.drawing():
			self.DrawGraph(element,self.pstricks_code.index("%GRID\n")+1)


	def TracePsCurve(self,listePoints,params,on_BB=False,N=None):
		"""
		By default, we don't take these poits into account in the bounding box because this method is almost only 
		   used to draw wavy lines. It is sufficient to put the line in the BB.
		"""
		l = []
		l.append("\pscurve["+params+"]")
		for p in listePoints :
			l.append(p.coordinates())
			if on_BB :
				self.BB.AddPoint(p)
		ligne = "".join(l)
		if N == None :
			self.add_latex_line(ligne)
		else :
			self.IncrusteLigne(ligne,N)
	def DrawWavySegment(self,seg,dx,dy,params,N):
		A = seg.I
		B = seg.F
		self.BB.AddPoint(seg.I)
		self.BB.AddPoint(seg.F)
		self.TracePsCurve(seg.get_wavy_points(dx,dy),params,N=N)
	def TracephyFunctionOndule(self,f,mx,Mx,dx,dy,params):
		self.BB.AddphyFunction(f,mx,Mx)
		self.TracePsCurve( f.get_wavy_points(mx,Mx,dx,dy) ,params)
	def TraceCourbeParametriqueOndule(self,curve,llamI,llamF,dx,dy,params):
		self.BB.AddParametricCurve(curve,llamI,llamF)
		self.TracePsCurve( curve.get_wavy_points(llamI,llamF,dx,dy) ,params)
		
	def TraceTriangle(self,tri,params):
		self.BB.AddPoint(tri.A)
		self.BB.AddPoint(tri.B)
		self.BB.AddPoint(tri.C)
		self.add_latex_line("\pstTriangle["+params+",PointSymbol=none]"+tri.A.coordinates()+"{A}"+tri.B.coordinates()+"{B}"+tri.C.coordinates()+"{C}")
		
	def TraceRectangle(self,rect,params):
		self.BB.AddPoint(rect.bg)
		self.BB.AddPoint(rect.hd)
		self.add_latex_line("\psframe["+params+"]"+rect.hd.coordinates()+rect.bg.coordinates())
	def TraceCircle(self,Cer,params):
		self.BB.AddCircle(Cer)
		self.AddPoint(Cer.centre)
		# Besoin d'un point sur le cercle pour le tracer avec \pstCircleOA,"")
		PsA = Point (Cer.centre.x-Cer.rayon,Cer.centre.y)		
		self.AddPoint(PsA)
		self.add_latex_line("\pstCircleOA["+params+"]{"+Cer.centre.psNom+"}{"+PsA.psNom+"}")
		# La commande pscircle ne tient pas compte des xunit et yunit => inutilisable.
		#self.add_latex_line("\pscircle["+params+"]("+Cer.centre.psNom+"){"+str(Cer.rayon)+"}")
	def TraceArcCircle(self,Cer,angleI,angleF,params):
		self.BB.AddArcCircle(Cer,angleI,angleF)
		self.AddPoint(Cer.centre)
		PsA = Cer.get_point(angleI)
		PsB = Cer.get_point(angleF)
		self.AddPoint(PsA)
		self.AddPoint(PsB)
		self.add_latex_line("\pstArcOAB[%s]{%s}{%s}{%s}"%(params,Cer.centre.psNom,PsA.psNom,PsB.psNom))
	# Les grilles se présentent sous la même forme que les axes : on en a par défaut pspicture.grille qu'on a intérêt à tracer
	#	avec pspicture.TraceGridDefaut()
	def TraceGrid(self,grille):
		self.IncrusteLigne(grille.code(self),2)

	def AjusteGrid(self,grille):
		grille.BB = self.BB

	def TraceGridDefaut(self):
		self.AjusteGrid(self.grille)
		self.TraceGrid(self.grille)

	# Il y a deux moyens de tracer des axes. 
	# 1. Construire un système d'axe à la main, puis le tracer avec pspicture.DrawAxes. 
	# 2. la classe pspicture a un système d'axe pspicture.axes. Donc on peut l'utiliser. Alors, le mieux est de tracer ces axes avec pspicture.DrawDefaultAxes qui utilisera ces axes
	#	et en ajustera automatiquement la BB sur la BB de la pspicture
	#
	# Les axes et les grilles sont ajoutées *au début* du code de la pspicture, ainsi elles ne se mettent pas sur les objets, mais en-dessous.
	# 	Cette subtilité est nécessaire parce que l'appel à pspict.DrawDefaultAxes doit se faire *après* avoir tracé les objets
	# 	pour que la BB en tienne compte. C'est pour ça que DrawAxes fait appel à IncrusteLigne et non add_latex_line.
	#

	def DrawAxes(self,axes):
		# C'est important d'ajuster la bounding box de la pspicture et les grilles après ajouter le code parce que axes.BB n'est définit qu'au moment de produire le code, voir l'appel à grille.BB.hd.EntierPlus() dans self.TraceGrid par exemple.
		try :
			self.IncrusteLigne(axes.code(),self.pstricks_code.index("%AXES\n")+1)
		except ValueError :
			print "Mon self.pstricks_code vaut :"
			print self.pstricks_code
			raise
		if axes.IsLabelX == 1:
			self.DrawPoint( Point(axes.BB.hd.x,0) ,"none","").MarkThePoint(axes.DistLabelX,axes.AngleLabelX,axes.LabelX)
		if axes.IsLabelY == 1:
			self.DrawPoint( Point(0,axes.BB.hd.y) ,"none","").MarkThePoint(axes.DistLabelY,axes.AngleLabelY,axes.LabelY)
		self.BB.AddAxes(axes,self.xunit,self.yunit)

	def DrawDefaultAxes(self):
		# If the lowest point has y=0.3, the method enlarge_a_little makes the axis begin at y=1.
		self.axes.BB = self.BB
		self.axes.BB.enlarge_a_little()
		self.DrawAxes(self.axes)

	def DrawDefaultGrid(self):
		# This is supposed to be called after DrawDefaultAxes
		self.grid.BB = self.axes.BB
		self.DrawGrid(self.grid)

	def TraceDynkin(self,Dynkin):
		Adjacence	= Dynkin.description.Adjacence
		ronds		= Dynkin.description.ronds
		remplissure	= Dynkin.description.remplissure
		distMark	= Dynkin.decoration.distMark
		angleMark	= Dynkin.decoration.angleMark
		visMark		= Dynkin.decoration.visMark
		n = len( Adjacence )
		for i in range(0,n):
			for j in range(0,n):
				if Adjacence[i][j]==1:
					self.DrawSegment( Segment(ronds[i],ronds[j]),"" )
				if Adjacence[i][j]==2:
					self.DrawSegment( Segment(ronds[i],ronds[j]),"doubleline=true" )
				if Adjacence[i][j]==4:
					self.DrawSegment( Segment(ronds[i],ronds[j]),"linestyle=dotted" )
				# Je dois encore faire le cas avec trois lignes, mais je ne sais pas comment faire :-(
		for i in range(0,n):
				self.MarkThePoint(ronds[i],distMark[i],angleMark[i],remplissure[i],visMark[i])

	def TraceYoung(self,Y):
		for i in range(0,len(Y.diagramme)):
			for j in range(0,len(Y.diagramme[i])):
				self.TraceRectangle( Rectangle( Point(j,-i),Point(j+1,-i-1) ),"" )
				self.MarkThePoint( Point(j,-i), 0.5,-45,"none", Y.diagramme[i][j] )
	def contenu_eps(self):
		to_eps = PspictureToOtherOutputs(self)
		to_eps.create_eps_file()
		return to_eps.input_code_eps
	def contenu_pdf(self):
		to_pdf = PspictureToOtherOutputs(self)
		to_pdf.create_pdf_file()
		return to_pdf.input_code_pdf
	def contenu_pstricks(self):
		"""
		One has to declare the xunit,yunit before to give the bounding box. The value of LabelSep is the distance between an angle and the lable of the angle. It is by default 1, but if there is a dilatation, the visual effect is bad.
		"""
		if self.LabelSep == 1 : 
			self.LabelSep = 2/(self.xunit+self.yunit)
		a = ["\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+",LabelSep="+str(self.LabelSep)+"}\n"]
		a.extend("\\begin{pspicture}%s%s\n"%(self.BB.bg.coordinates(),self.BB.hd.coordinates()))
		a.extend(self.pstricks_code)
		a.append("\end{pspicture}\n")
		return "".join(a)
	def contenu(self):
		""" Notice that if the option --eps is given, this method launches some compilations when creating contenu_eps """
		for sortie in globals.list_exits:
			if globals.__getattribute__(sortie+"_exit"):
				print "je vois %s"%sortie
				return self.__getattribute__("contenu_"+sortie)()			# Erreur très intéressante si on oublie la dernière paire de parenthèses
		return self.contenu_pstricks()

	# Important de pouvoir produire des fichiers qui ne contiennent qu'une pspicture parce que ça peut être inséré directement 
	# à l'intérieur d'une ligne en LaTeX. J'utilise ça pour des diagrammes de Dynkin par exemple.
	def write_the_file(self,f):					# Nous sommes dans la classe pspicture
		self.fichier = Fichier(f)
		#self.fichier.open_file("w")
		self.fichier.file.write(self.contenu())
		self.fichier.file.close()


globals = global_variables()
if "--eps" in sys.argv :
	globals.eps_exit = True
if "--pdf" in sys.argv :
	globals.pdf_exit = True
