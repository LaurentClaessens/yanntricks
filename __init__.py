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
#import numpy				# I do not remember why I used that.
import math, sys
from BasicGraphObjects import *
from MathComputations import *
from SmallComputations import *
import MathConstructions


def _latinize(word):
	latin = ""
	for s in word:
		if s.lower() in "abcdefghijklmnopqrstuvwxyz" :
			latin = latin+s
	return latin

sysargvzero = sys.argv[0][:]
def newwriteName():
	r"""
	This function provides the name of the \newwrite that will be used all long the script. We cannot use one different \newwrite for each counter because
	LaTeX is limited in the number of available \newwrite.

	See the attribute pspict.newwriteDone and the method pspict.get_counter_value
	"""
	return "writeOf"+_latinize(sysargvzero)
def counterName():
	r"""
	This function provides the name of the counter. This has the same use of newwriteName, for the same reason of limitation.
	"""
	return "counterOf"+_latinize(sysargvzero)
def newlengthName():
	r"""
	This function provides the name of the length. This has the same use of newwriteName, for the same reason of limitation.
	"""
	return "lengthOf"+_latinize(sysargvzero)

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

#NomPointLibre = ListeNomsPoints()
#BasicGraphObjects.NomPointLibre = NomPointLibre

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

class CalculPolynome(object):
	"""
	This class should disappear when I learn how to perform euclidian divisions with Sage.
	"""
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
	def __init__(self,graphe,dist,angle,text):
		self.graphe = graphe
		self.dist = dist
		self.angle = angle
		self.text = text
	def central_point(self):
		"""return the central point of the mark, that is the point where the mark arrives"""
		return self.graphe.translate(PolarVector(self.graphe,self.dist,self.angle))

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

class GraphOfAPoint(GraphOfAnObject,Point):
	def __init__(self,point):
		GraphOfAnObject.__init__(self,point)
		Point.__init__(self,point.x,point.y)
		self.point = self.obj
		self.add_option("PointSymbol=*")
	def bounding_box(self,pspict):
		"""
		return the bounding box of the point including its mark

		A small box of radius 0.1 is given in any case, and the mark is added if there is a one.
		You need to provide a pspict in order to compute the size since it can vary from the place in your document you place the figure.
		"""
		bb = BoundingBox(Point(self.x-0.1,self.y-0.1),Point(self.x+0.1,self.y+0.1))
		if self.marque:
			central_point = self.mark.central_point()
			dimx,dimy=pspict.get_box_size(self.mark.text)
			bb.AddPoint( Point(central_point.x-dimx/2,central_point.y-dimy/2) )
			bb.AddPoint( Point(central_point.x+dimx/2,central_point.y+dimy/2) )
		return bb

class GraphOfASegment(GraphOfAnObject):
	def __init__(self,seg):
		GraphOfAnObject.__init__(self,seg)
		self.seg = self.obj
		self.I = self.seg.I
		self.F = self.seg.F

class GraphOfAVector(GraphOfAnObject):
	def __init__(self,vect):
		GraphOfAnObject.__init__(self,vect)
		self.vector = self.obj

class GraphOfACircle(GraphOfAnObject):
	def __init__(self,circle):
		GraphOfAnObject.__init__(self,circle)
		self.circle = self.obj
		self.angleI = 0
		self.angleF = 2*pi		# By default, the circle is drawn between the angles 0 and 2pi.


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
# Pour re-re-rappel, je crois que cette fonctione n'est plus du tout utilisée par des choses importantes.
#def SubstitutionMathLaTeX(exp):
#	a = exp
#	for i in range(1,10):
#		a = a.replace("math.log"+str(i),"\\log_{"+str(i)+"}")
#	return a.replace("math.tan","\\tan").replace("math.log","\\ln").replace("math.","\\").replace("*"," ")
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
		print "This is a depreciated feature ... I think the program is going to crash now :("


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
	var('x,y')
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

		# The order of declaration is important, because it is recorded in the Separator.number attribute.
		self.separator_dico = {}			
		self.separator_number = 0
		self.new_separator("ENTETE")
		self.new_separator("BEFORE SUBFIGURES")
		self.new_separator("SUBFIGURES")
		self.new_separator("AFTER SUBFIGURES")
		self.new_separator("DEFAULT")
		self.new_separator("BEFORE PSPICTURE")
		self.new_separator("PSPICTURE")
		self.new_separator("AFTER PSPICTURE")
		self.new_separator("AFTER ALL")
		add_latex_line_entete(self)

		self.add_latex_line("\\begin{figure}[ht]","BEFORE SUBFIGURES")
		self.add_latex_line("\centering","BEFORE SUBFIGURES")
	# Note qu'il est préférable d'utiliser les commandes de dilatation avant de commencer à composer la pspicture,
	# parce que la BoundingBox doit aussi tenir compte de choses écrites en taille réelle.

	def new_separator(self,title):
		self.separator_number = self.separator_number + 1
		self.separator_dico[title]=Separator(title,self.separator_number)

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
	def add_latex_line(self,ligne,separator_name="DEFAULT"):
		self.separator_dico[separator_name].add_latex_line(ligne)
	def IncrusteLigne(self,ligne,n):
		print "The method picture.IncrusteLigne() is depreciated."
		self.code[n:n]=ligne+"\n"
	def AjouteCode(self,liste_code):
		self.code.extend(liste_code)

	def conclude(self):
		if not globals_vars.special_exit() :
			self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+"}","BEFORE SUBFIGURES")
		for f in self.SSfigures :
			self.add_latex_line("\subfigure["+f.caption+"]{%","SUBFIGURES")
			self.add_latex_line(f.code,"SUBFIGURES")
			self.add_latex_line("}					% Fermeture de la sous-figure "+str(self.SSfigures.index(f)+1),"SUBFIGURE")
			self.add_latex_line("%","SUBFIGURES")
			

		after_all=r"""\caption{"+self.caption+"}\label{"+self.label+"}"
			\end{figure}")
			"""
		self.add_latex_line(after_all,"AFTER ALL")



		self.contenu = DicoSeparatorToCode(self.separator_dico)

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
		code = ["\documentclass{article}\n","\usepackage{pstricks,pst-eucl,pstricks-add}\n","\usepackage{pst-plot}\n","\usepackage{pst-eps}\n","\pagestyle{empty}\n\usepackage{calc}\n"]
		# Allows to add some lines, like packages or macro definitions required. This is useful when one add formulas in the picture
		# that need packages of personal commands.
		code.append(self.pspict.specific_needs)		
		code.extend(["\\begin{document}\n","\\begin{TeXtoEPS}"])
		code.append(self.pspict.contenu_pstricks())
		code.extend(["\end{TeXtoEPS}\n","\end{document}\n"])
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
	position = "ENTETE"
	truc.add_latex_line("% This file is automatically generated by phystricks",position)
	truc.add_latex_line("% See the documentation ",position)
	truc.add_latex_line("% http://student.ulb.ac.be/~lclaesse/phystricks-doc.pdf ",position)
	truc.add_latex_line("% and the projects phystricks and phystricks-doc at ",position)
	truc.add_latex_line("% http://gitorious.org/~moky\n",position)


def DicoSeparatorToCode(separator_dico):
	""""takes a dictionary of Separator as argument and return the glued code"""
	list_separator = separator_dico.values()
	list_separator.sort()
	a = []
	for sep in list_separator :
		a.append(sep.code())
	return "".join(a)

class Separator(object):
	def __init__(self,title,number):
		self.title = title
		self.number = number
		self.latex_code=[]
		self.add_latex_line("%"+title)
	def add_latex_line(self,line):
		text = "".join(line)		# In some case, the line can in fact be a list of lines.
		self.latex_code.append(text+"\n")
	def code(self):
		return "".join(self.latex_code)
	def __cmp__(self,other):
		if self.number < other.number :
			return -1
		if self.number == other.number :
			raise "Two separators should not have the same number, you're trying to make me crazy."
		if self.number > other.number :
			return 1

class LabelNotFound:
	def __init__(self,message):
		self.message=message

class pspicture(object):
	r"""
	self.pstricks_code contains the pstricks code of what has to be between \begin{pspicture} and \end{pspicture}. This is not the environment itself, neither the definition of xunit, yunit.
	self.contenu_pstricks() is the whole code including the x/yunit
	self.contenu_eps() contains the line to be added in order to include the eps file
	"""
	NomPointLibre = ListeNomsPoints()
 
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

	def __init__(self,name="CAN_BE_A_PROBLEM_IF_TRY_TO_PRODUCE_EPS_OR_PDF"):				# class pspicture
		r"""
		A name is required for producing intermediate files. This is the case when one wants to produce eps/pdf files of one wants to 
		   make interactions with LaTeX (see pspict.get_counter_value).
		"""
		self.name = name		# self.name is used in order to name the intermediate files when one produces the eps file.
		self.pstricks_code = []
		self.specific_needs = ""	# See the class PspictureToOtherOutputs
		self.newwriteDone = False
		self.interWriteFile = newwriteName()+".pstricks.aux"
		self.NomPointLibre = ListeNomsPoints()
		self.counterDone = False
		self.newlengthDone = False
		self.listePoint = []
		self.xunit = 1
		self.yunit = 1
		self.LabelSep = 1
		self.BB = BoundingBox(Point(1000,1000),Point(-1000,-1000))
		self.axes = Axes( Point(0,0), BoundingBox(Point(1000,1000), Point(-1000,-1000)) )
		self.grid = Grid(BoundingBox(Point(1000,1000), Point(-1000,-1000)) )
		# We add the "anchors" %GRID and %AXES in order to force the axes and the grid to be written at these places.
		#    see the functions DrawAxes and DrawGrid and the fact that they use IncrusteLigne


		# The order of declaration is important, because it is recorded in the Separator.number attribute.
		self.separator_dico = {}			
		self.separator_number = 0
		self.new_separator("ENTETE")
		self.new_separator("BEFORE PSPICTURE")
		self.new_separator("BEGIN PSPICTURE")
		self.new_separator("GRID")	# A \n is automatically added.		
		self.new_separator("AXES")
		self.new_separator("OTHER STUFF")
		self.new_separator("DEFAULT")
		self.new_separator("AFTER PSPICTURE")

	def new_separator(self,title):
		self.separator_number = self.separator_number + 1
		self.separator_dico[title]=Separator(title,self.separator_number)

	def initialize_newwrite(self):
		if not self.newwriteDone :
			code = r""" \makeatletter 
				\@ifundefined{%s}			
				{\newwrite{\%s}
				\immediate\openout\%s=%s
				}
				\makeatother"""%(newwriteName(),newwriteName(),newwriteName(),self.interWriteFile)
			self.add_latex_line(code,"BEFORE PSPICTURE")
			self.newwriteDone = True
	def initialize_counter(self):
		if not self.counterDone:
			code = r""" \makeatletter 
				\@ifundefined{c@%s}			
				{\newcounter{%s}}
				\makeatother
				"""%(counterName(),counterName())			# make LaTeX test if the counter exist before to create it.
			self.add_latex_line(code,"BEFORE PSPICTURE")
			self.counterDone = True
	def initialize_newlength(self):
		if not self.newlengthDone :
			code =r"""
			\makeatletter
			\@ifundefined{%s}{\newlength{\%s}}
			\makeatother
			"""%(newlengthName(),newlengthName())
			self.add_latex_line(code,"BEFORE PSPICTURE")
			self.newlengthDone = True
	def add_write_line(self,Id,value):
		r"""Writes in the standard auxiliary file \newwrite an identifier and a value separated by a «:»"""
		interWriteName = newwriteName()
		self.initialize_newwrite()
		self.add_latex_line(r"\immediate\write\%s{%s:%s:}"%(interWriteName,Id,value),"BEFORE PSPICTURE")
	def get_Id_value(self,Id,counter_name="NO NAME ?",default_value=0):
		try :
			try :
				f=open(self.interWriteFile)
				text = f.read().replace('\n','').split(":")
				return text[text.index(Id)+1]			
			except IOError :
				raise LabelNotFound("Warning : the auxiliary file seems not to exist. Compile your LaTeX file.")
			except ValueError :
				raise LabelNotFound("Warning : the auxiliary file does not contain the id «%s». Compile your LaTeX file."%Id)
		except LabelNotFound,data:
			print data.message
			print "I' going to return the default value for %s, namely %s"%(Id,str(default_value))
			return default_value
	def get_counter_value(self,counter_name,default_value=0):
		"""
		return the value of the (LaTeX) counter <name> at this point of the LaTeX file 

		Makes LaTeX write the value of the counter in an auxiliary file, then reads the value in that file.
		(needs several compilations to work)
		"""

		# Make LaTeX write the value of the counter in a specific file
		interCounterId = "counter"+self.name+self.NomPointLibre.suivant()
		print "J'ai le ID",interCounterId
		self.initialize_counter()
		self.add_write_line(interCounterId,r"\arabic{%s}"%counter_name)

		# Read the file and return the value
		return self.get_Id_value(interCounterId,"counter «%s»"%counter_name,default_value)

	def get_box_dimension(self,tex_expression,dimension_name):
		"""
		Return the dimension of the LaTeX box corresponding to the LaTeX expression tex_expression.

		dimension_name is a valid LaTeX macro that can be applied to a LaTeX expression and that return a number. Like
		widthof, depthof, heightof, totalheightof
		"""
		interId = dimension_name+self.name+self.NomPointLibre.suivant()
		self.initialize_newlength()
		self.add_latex_line(r"\setlength{\%s}{\%s{%s}}"%(newlengthName(),dimension_name,tex_expression),"BEFORE PSPICTURE")
		self.add_write_line(interId,r"\the\%s"%newlengthName())
		read_value =  self.get_Id_value(interId,"dimension %s"%dimension_name,default_value="0pt") 
		dimenPT = float(read_value.replace("pt",""))
		#print "J'ai une dimension de ",dimenPT
		return dimenPT/30			# 30 is the conversion factor : 1pt=(1/3)mm
	def get_box_size(self,tex_expression):
		"""
		tex_expression is a valid LaTeX expression. Return the size of the corresponding box in cm

		As far as the problem is concerned from a LaTeX point of view, it was discussed here:
		http://groups.google.fr/group/fr.comp.text.tex/browse_thread/thread/8431f21588b81530?hl=fr
		"""
		height = self.get_box_dimension(tex_expression,"totalheightof")
		width = self.get_box_dimension(tex_expression,"widthof")
		return width,height

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
	# AddPoint sert à créer un point pstricks. Pour le faire apparaître effectivement, il faut utiliser DrawGraphOfAPoint.
	def CodeAddPoint(self,P):
		self.listePoint.append(P.psNom)
		return "\pstGeonode[PointSymbol=none,PointName=none]"+P.coordinates()+"{"+P.psNom+"}"
	def AddPoint(self,P):
		self.add_latex_line(self.CodeAddPoint(P))

	def TraceBB(self):
		self.DrawBoundingBox(self.BB)
	def DrawBoundingBox(self,obj):
		"""Draw the bounding box of an object when it has a method bounding_box. If not, assume that the object is the bounding box to be drawn."""
		try :
			bb = obj.bounding_box(self)
		except AttributeError :
			bb = obj
		self.TraceRectangle( Rectangle(bb.bg,bb.hd), "linecolor=cyan")

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

	def DrawGraphOfAPoint(self,graphe):
		p = graphe.point
		self.BB.AddPoint(p)
		self.BB.AddBB(graphe.bounding_box(self))
		self.add_latex_line( p.code(graphe.params()) )
		if graphe.marque :
			mark = graphe.mark
			if p.psNom not in self.listePoint :
				self.AddPoint(p)
			#self.add_latex_line("\\rput("+p.psNom+"){\\rput("+str(dist)+";"+str(angle)+"){"+marque+"}}")
			self.add_latex_line("\\rput(%s){\\rput(%s;%s){%s}}"%(p.psNom,str(mark.dist),str(mark.angle),str(mark.text)))

	def DrawGraphOfASegment(self,graphe,separator="DEFAULT"):
		if graphe.wavy == False :
			self.DrawSegment(graphe.seg,graphe.params(),separator=separator)
		if graphe.wavy == True :
			waviness = graphe.waviness
			self.DrawWavySegment(graphe.seg,waviness.dx,waviness.dy,graphe.params(),separator=separator)
	def DrawGraphOfAVector(self,graphe):
		if graphe.marque == False :
			self.DrawVector(graphe.vector,graphe.params())
		if graphe.marque == True :
			mark = graphe.mark
			self.DrawVector(graphe.vector,graphe.params()).MarkTheVector(mark.dist,mark.angle,mark.text)

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

	def DrawGraph(self,graphe,separator="DEFAULT"):
		# If n is not None, it is the number of the line where the code has to be put. This is used by DrawGrid
		if type(graphe) == GraphOfAFunction :
			self.DrawGraphOfAFunction(graphe)
		if type(graphe) == GraphOfAParametricCurve :
			self.DrawGraphOfAParametricCurve(graphe)
		if type(graphe) == GraphOfASegment :
			self.DrawGraphOfASegment(graphe,separator=separator)
		if type(graphe) == GraphOfAVector :
			self.DrawGraphOfAVector(graphe)
		if type(graphe) == GraphOfACircle :
			self.DrawGraphOfACircle(graphe)
		if type(graphe) == GraphOfAPoint :
			self.DrawGraphOfAPoint(graphe)

		if type(graphe) == Grid :
			self.DrawGrid(graphe)

	def DrawSegment(self,seg,params,separator="DEFAULT"):
		self.BB.AddSegment(seg)
		code = seg.code(params)
		self.add_latex_line(code,separator)

	def DrawGrid(self,grid):
		# The difficulty is that the grid has to be draw first, while most of time it is given last because of the bounding box.
		self.BB.AddBB(grid.BB)
		for element in grid.drawing():
			self.DrawGraph(element,"GRID")


	def TracePsCurve(self,listePoints,params,on_BB=False,separator="DEFAULT"):
		"""
		By default, we don't take these points into account in the bounding box because this method is almost only 
		   used to draw wavy lines. It is sufficient to put the line in the BB.
		"""
		l = []
		l.append("\pscurve["+params+"]")
		for p in listePoints :
			l.append(p.coordinates())
			if on_BB :
				self.BB.AddPoint(p)
		ligne = "".join(l)
		self.add_latex_line(ligne,separator)
	def DrawWavySegment(self,seg,dx,dy,params,separator):
		A = seg.I
		B = seg.F
		self.BB.AddPoint(seg.I)
		self.BB.AddPoint(seg.F)
		self.TracePsCurve(seg.get_wavy_points(dx,dy),params,separator=separator)
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
			self.add_latex_line(axes.code(),"AXES")
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

	def add_latex_line(self,ligne,separator_name="DEFAULT"):
		"""
		Add a line in the pstricks code. The optional argument <position> is the name of a marker like %GRID, %AXES, ...
		"""
		self.separator_dico[separator_name].add_latex_line(ligne)
	def IncrusteLigne(self,ligne,n):
		print "The method pspicture.IncrusteLigne() is depreciated."
		self.pstricks_code[n:n]=ligne+"\n"
	def contenu_eps(self):
		to_eps = PspictureToOtherOutputs(self)
		to_eps.create_eps_file()
		return to_eps.input_code_eps
	def contenu_pdf(self):
		to_pdf = PspictureToOtherOutputs(self)
		to_pdf.create_pdf_file()
		return to_pdf.input_code_pdf
	def contenu_pstricks(self):					# class pspicture
		"""
		One has to declare the xunit,yunit before to give the bounding box. The value of LabelSep is the distance between an angle and the lable of the angle. It is by default 1, but if there is a dilatation, the visual effect is bad.
		"""
		add_latex_line_entete(self)
		if self.LabelSep == 1 : 
			self.LabelSep = 2/(self.xunit+self.yunit)
		add_latex_line_entete(self)
		self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+",LabelSep="+str(self.LabelSep)+"}","BEFORE PSPICTURE")
		self.add_latex_line("\psset{PointSymbol=none,PointName=none,algebraic=true}\n","BEFORE PSPICTURE")
		self.add_latex_line("\\begin{pspicture}%s%s\n"%(self.BB.bg.coordinates(),self.BB.hd.coordinates()),"BEGIN PSPICTURE")
		self.add_latex_line("\end{pspicture}\n","AFTER PSPICTURE")
		self.add_latex_line(self.pstricks_code,"OTHER STUFF")


		return DicoSeparatorToCode(self.separator_dico)
	def contenu(self):
		"""
		Notice that if the option --eps/pdf is given, this method launches some compilations when creating contenu_eps/pdf 
		"""
		for sortie in globals_vars.list_exits:
			if globals_vars.__getattribute__(sortie+"_exit"):
				print "je vois %s"%sortie
				return self.__getattribute__("contenu_"+sortie)()
		return self.contenu_pstricks()

	# Important de pouvoir produire des fichiers qui ne contiennent qu'une pspicture parce que ça peut être inséré directement 
	# à l'intérieur d'une ligne en LaTeX. J'utilise ça pour des diagrammes de Dynkin par exemple.
	def write_the_file(self,f):					# Nous sommes dans la classe pspicture
		self.fichier = Fichier(f)
		#self.fichier.open_file("w")
		self.fichier.file.write(self.contenu())
		self.fichier.file.close()

globals_vars = global_variables()
if "--eps" in sys.argv :
	globals_vars.eps_exit = True
if "--pdf" in sys.argv :
	globals_vars.pdf_exit = True
