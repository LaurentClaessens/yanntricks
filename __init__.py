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

The documentation is available at
"""

#from __future__ import division
from sage.all import *
#import numpy				# I do not remember why I used that.
import math, sys
from BasicGeometricObjects import *
from MathComputations import *
from SmallComputations import *
import MathConstructions

def RemoveLastZeros(x,n):
	"""
	Take a number <x>, cuts to <n> decimals and then remove the last zeros. 

	If there remain no decimals, also remove the dot.

	Example:
	RemoveLastZeros(1.000,4) returns the string "1"
	RemoveLastZeros(3/4,1) returns the string "0.7"
	RemoveLastZeros(3/4,3) returns the string "0.75"
	RemoveLastZeros(3/4,4) returns the string "0.75"
	"""
	#http://www.java2s.com/Code/Python/Development/StringformatFivedigitsafterdecimalinfloat.htm
	s="%.15f"%x
	t=s[:s.find(".")+n+1]
	k=len(t)-1
	while t[k]=="0":
		k=k-1
	u=t[:k+1]
	if u[-1]==".":
		return u[:-1]
	return u

def _latinize(word):
	latin = ""
	for s in word:
		if s.lower() in "abcdefghijklmnopqrstuvwxyz" :
			latin = latin+s
		if s=="1":
			latin = latin+"O"
		if s=="2":
			latin = latin+"T"
		if s=="3":
			latin = latin+"Th"
		if s=="4":
			latin = latin+"F"
		if s=="5":
			latin = latin+"Fi"
		if s=="6":
			latin = latin+"S"
		if s=="7":
			latin = latin+"Se"
		if s=="8":
			latin = latin+"H"
		if s=="9":
			latin = latin+"N"
		if s=="0":
			latin = latin+"Z"
		if s==".":
			latin = latin+"D"
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

def MainGridArray(mx,Mx,Dx):
		"""
		Return the list of number that are
		1. integer multiple of Dy
		2. between mx and Mx

		If mx=-1.4 and Dx=0.5, the first element of the list will be -1
		If mx=-1.5 and Dx=0.5, the first element of the list will be -1.5
		"""
		#for y in range(MultipleBigger(self.BB.my,self.Dy),MultipleLower(self.BB.My,self.Dy)+1,self.Dy):
		a=[]
		m = floor(mx/Dx - 1)
		M = ceil(Mx/Dx + 1)
		for i in range(m,M):
			tentative=i*Dx
			if (tentative >= mx) and (tentative <= Mx):
				a.append(tentative)
		return a

class Triangle(object):
	def __init__(self,A,B,C):
		self.A = A
		self.B = B
		self.C = C

class GraphOfAParametricCurve(GraphOfAnObject,ParametricCurve):
	def __init__(self,curve,llamI,llamF):
		GraphOfAnObject.__init__(self,curve)
		ParametricCurve.__init__(self,curve.f1,curve.f2)
		self.curve = self.obj			# It is strange that this line does not raise a crash.
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
	def bounding_box(self,pspict=None):
		xmin=self.xmin(self.llamI,self.llamF)
		xmax=self.xmax(self.llamI,self.llamF)
		ymin=self.ymin(self.llamI,self.llamF)
		ymax=self.ymax(self.llamI,self.llamF)
		bb = BoundingBox( Point(xmin,ymin),Point(xmax,ymax)  )
		return bb
	def math_bounding_box(self,pspict=None):
		return self.bounding_box(pspict)
	def pstricks_code(self,pspict=None):
		if self.wavy :
			waviness = self.waviness
			return Code_Pscurve( self.curve.get_wavy_points(self.llamI,self.llamF,waviness.dx,waviness.dy) ,self.params())
		else:
			initial = numerical_approx(self.llamI)		# Avoid the string "pi" in the pstricks code.
			final = numerical_approx(self.llamF)
			return "\parametricplot[%s]{%s}{%s}{%s}" %(self.params(),str(initial),str(final),self.curve.pstricks())

def Graph(X,*arg):
	"""This function is supposed to be only used by the end user."""
	print "The function Graph should not be used"
	raise TypeError
	try :
		return X.default_associated_graph_class()(X,arg)
	except TypeError,datay :
		return X.default_associated_graph_class()(X)
	except AttributeError,data :
		raise
		if type(X) == phyFunction :
			return GraphOfAphyFunction(X,arg[0],arg[1])
		if type(X) == ParametricCurve :
			return GraphOfAParametricCurve(X,arg[0],arg[1])
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
		self.liste_GraphOfAphyFunction = L
	def add_option(opt):
		for gf in self.liste_fonctions :
			gf.add_option(opt)

def SubstitutionMathMaxima(exp):
	a = exp
	for i in range(1,10):
		a = a.replace("math.log"+str(i),"log("+str(i)+")^(-1)*log")
	return a.replace("math.log","log").replace("math.tan","tan").replace("math.pi","%pi").replace("math.","")

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
		self.separator_name="GRID"
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
	def bounding_box(self,pspict=None):		# This method is for the sake of "Special cases aren't special enough to break the rules."
		return self.BB
	def add_option(self,opt):
		self.options.add_option(opt)
	def optionsTrace(self):
		return self.options.sousOptions(OptionsStyleLigne())
	def optionsParams(self):
		return self.options.sousOptions(["Dx","Dy"])
	def drawing(self):
		a = []
		# ++++++++++++ Border ++++++++ 
		self.draw_border = False		# 16 oct 2010 : no more border
		if self.draw_border :
			# Right border
			if self.BB.Mx <> int(self.BB.Mx):
				print "right"
				S = self.BB.east_segment()
				S.merge_options(self.border)
				a.append(S)
			# Left border
			if self.BB.mx <> int(self.BB.mx):
				print "left"
				S = self.BB.west_segment()
				S.merge_options(self.border)
				a.append(S)
			# Upper border
			if self.BB.My <> int(self.BB.My):
				print "upper"
				S = self.BB.north_segment()
				S.merge_options(self.border)
				a.append(S)
			# Lower border
			if self.BB.my <> int(self.BB.my):
				print "lower"
				S = self.BB.south_segment()
				S.merge_options(self.border)
				a.append(S)
		# ++++++++++++ The vertical sub grid ++++++++ 
		if self.num_subX <> 0 :
			for x in  SubGridArray(self.BB.mx,self.BB.Mx,self.Dx,self.num_subX) :
					S = Segment( Point(x,self.BB.my),Point(x,self.BB.My) )
					S.merge_options(self.sub_vertical)
					a.append(S)
		# ++++++++++++ The horizontal sub grid ++++++++ 
		if self.num_subY <> 0 :
			for y in  SubGridArray(self.BB.my,self.BB.My,self.Dy,self.num_subY) :
					S = Segment( Point(self.BB.mx,y),Point(self.BB.Mx,y) )
					S.merge_options(self.sub_horizontal)
					a.append(S)
		# ++++++++++++ Principal horizontal lines ++++++++ 
		for y in MainGridArray(self.BB.my,self.BB.My,self.Dy) :
			S = Segment( Point(self.BB.mx,y),Point(self.BB.Mx,y) )
			S.merge_options(self.main_vertical)
			a.append(S)
		# ++++++++++++ Principal vertical lines ++++++++
		for x in MainGridArray(self.BB.mx,self.BB.Mx,self.Dx) :
			S = Segment( Point(x,self.BB.my),Point(x,self.BB.My) )
			S.merge_options(self.main_vertical)
			a.append(S)
		return a
	def pstricks_code(self,pspict=None):
		a=[]
		for element in self.drawing():
			a.append(element.pstricks_code(pspict))
		return "\n".join(a)

class AxesUnit(object):
	def __init__(self,numerical_value,latex_symbol=""):
		try :
			numerical_value=sage.rings.rational.Rational(numerical_value)
		except TypeError :
			pass
		self.numerical_value=numerical_value
		self.latex_symbol=latex_symbol
	def symbol(self,x):
		return latex(x)+self.latex_symbol
	def place_list(self,mx,Mx,frac=1):
		"""
		return a tuple of 
		1. values that are all the integer multiple of <frac>*self.numerical_value between mx and Mx
		2. the multiple of the basis unit.

		Please give <frac> as litteral real. Recall that python evaluates 1/2 to 0. If you pass 0.5, it will be converted to 1/2 for a nice display.
		"""
		try :
			frac=sage.rings.rational.Rational(frac)		# If the user enter "0.5", it is converted to 1/2
		except TypeError :
			pass
		if frac==0:
			raise ValueError,"frac is zero in AxesUnit.place_list(). Maybe you are giving the fraction 1/2 instead of 0.5\n Are you trying to push me in an infinite loop ?"
		l=[]
		x=mx
		step=var("step")
		k=var("TheTag")
		step=self.numerical_value*frac
		ni=ceil(float(mx)/step)
		nf=floor(float(Mx)/step)
		x0=ni*step
		for i in range(ni,nf+1):
			if i != 0:
				x=i*step
				if self.latex_symbol == "":
					l.append((x,"$"+latex(x)+"$"))
				else :
					pos=(x/self.numerical_value)*k
					text="$"+latex(pos).replace("\mbox{TheTag}",self.latex_symbol)+"$"	# This risk to be Sage-version dependant.
					l.append((x,text))
		return l

class Axes(object):
	"""
	ATTRIBUTS
		self.grille :		la grille associée
		self.Dx, self.Dy :	l'intervalle avec laquelle des marques sont faites sur les axes
	MÉTHODES
		self.AjouteGrid			Crée une grille avec des options par défaut
		self.add_label_X		Ajoute un label X (idem pour Y)
		self.add_option			Ajoute une option. Ceci doit être fait avec la syntaxe pstricks
		self.no_graduation		Pas de marques sur les axes
	"""
	def __init__(self,C,bb):
		self.C = C						
		self.BB = bb.copy()
		#self.BB.AddPoint( Point(C.x-0.5,C.y-0.7) )		# Celle-ci est pour tenir compte des chiffres écrits sur les axes X et Y
									# No more usefull because they are now numbers put «by hand».
		self.options = Options()
		self.grille = Grid(self.BB)
		self.IsLabelX = False
		self.IsLabelY = False
		self.axes_unitX=AxesUnit(1,"")
		self.axes_unitY=AxesUnit(1,"")
		#self.N=Point( self.C.x,self.BB.My )
		#self.S=Point( self.C.x,self.BB.my )
		#self.O=Point( self.BB.mx,self.C.y )
		#self.E=Point( self.BB.Mx,self.C.y )
		#self.SO=Point(self.O.x,self.S.y)
		#self.NE=Point(self.E.x,self.N.y)
		#self.SE=Point(self.E.x,self.S.y)
		#self.NO=Point(self.O.x,self.N.y)
		self.Dx = 1
		self.Dy = 1						# Ce sont les valeurs par défaut.
		self.arrows = "->"
		self.separator_name="AXES"
	# Cette méthode ne devrait pas être utilisée parce qu'il n'y a pas de grille associée à un système d'axes.
	def AjouteGrid(self):
		print "This is depreciated"
		raise
		self.IsGrid = 1
		self.grille.add_option("gridlabels=0")
		self.grille.add_option("subgriddiv=0")
		self.grille.add_option("griddots=5")
	def add_label_X(self,dist,angle,marque):
		self.IsLabelX = True
		self.LabelX = marque
		self.DistLabelX = dist
		self.AngleLabelX = angle
	def add_label_Y(self,dist,angle,marque):
		self.IsLabelY = True
		self.LabelY = marque
		self.DistLabelY = dist
		self.AngleLabelY = angle
		# Je crois que le label n'est pas encore prit en compte dans la BB.

	def add_option(self,opt):
		self.options.add_option(opt)
	def no_graduation(self):
		self.add_option("labels=none,ticks=none")
	def AjustephyFunction(self,f,mx,Mx):
		print "This is depreciated"
		raise
		self.BB.AddphyFunction(f,mx,Mx)
	def AjusteCircle(self,Cer):
		self.BB.AddCircle(Cer)
	def AjusteGraphephyFunction(self,gf):
		print "This is depreciated"
		raise
		self.AjustephyFunction(gf.f,gf.mx,gf.Mx)
	def bounding_box(self,pspict=None):
		return self.BB
	def math_bounding_box(self,pspict=None):
		return self.bounding_box(pspict)
	def pstricks_code(self,pspict=None):
		sDx=RemoveLastZeros(self.Dx,10)
		sDy=RemoveLastZeros(self.Dy,10)
		self.add_option("Dx="+sDx)
		self.add_option("Dy="+sDy)
		bgx = self.BB.mx
		bgy = self.BB.my
		if self.BB.mx == int(self.BB.mx):		# Avoid having end of axes on an integer coordinate for aesthetic reasons.
			bgx = self.BB.mx + 0.01
		if self.BB.my == int(self.BB.my):
			bgy = self.BB.my +0.01
		self.BB.mx = bgx
		self.BB.my = bgy
		c=[]
		if self.IsLabelX :
			P = Point(self.bounding_box(pspict).Mx,0)
			P.parameters.symbol="none"
			P.put_mark(self.DistLabelX,self.AngleLabelX,self.LabelX)
			c.append(P.pstricks_code())
		if self.IsLabelY :
			P = Point(0,self.bounding_box(pspict).My)
			P.parameters.symbol="none"
			P.put_mark(self.DistLabelY,self.AngleLabelY,self.LabelY)
			c.append(P.pstricks_code())
		for x,symbol in self.axes_unitX.place_list(self.bounding_box(pspict).mx,self.bounding_box(pspict).Mx,self.Dx):
			if x != 0:
				A=Point(x,0)
				A.parameters.symbol="|"
				A.psName=A.psName+pspict.name+_latinize(str(numerical_approx(x)))		# Make the name of the point unique.
				A.put_mark(0.4,-90,symbol)	# TODO : use the size of the box as distance
				c.append(A.pstricks_code())
				pspict.record_marks.append(A.mark)
		for y,symbol in self.axes_unitY.place_list(self.bounding_box(pspict).my,self.bounding_box(pspict).My,self.Dy):
			if y != 0:
				A=Point(0,y)
				A.parameters.symbol="|"
				A.add_option("dotangle=90")
				A.psName=A.psName+pspict.name+_latinize(str(numerical_approx(y)))		# Make the name of the point unique.
				A.put_mark(0.4,180,symbol)	# TODO : use the size of the box as distance
				c.append(A.pstricks_code())
				pspict.record_marks.append(A.mark)
		#c.append("\psaxes[%s]{%s}%s%s"%(self.options.code(),self.arrows,self.C.coordinates(),self.bounding_box().coordinates()))
		h1=Point(self.bounding_box(pspict).mx,self.C.y)
		h2=Point(self.bounding_box(pspict).Mx,self.C.y)
		v1=Point(self.C.x,self.bounding_box(pspict).my)
		v2=Point(self.C.x,self.bounding_box(pspict).My)
		h=Vector(h1,h2)
		v=Vector(v1,v2)
		c.append(h.pstricks_code())
		c.append(v.pstricks_code())
		return "\n".join(c)

def CircleInterLigne(Cer,Ligne):
	print "This function is depreciated. Please use Intersection instead"
	raise
	if type(Ligne) == phyFunction :
		soluce = maxima().solve( [Cer.maxima,"y="+Ligne.maxima],["x","y"] )
	else :
		soluce = maxima().solve( [Cer.maxima,Ligne.maxima],["x","y"] )
	if len(soluce) == 0:
		return [Point(0,0),Point(0,0)]
	if len(soluce) == 1:
		return [Point(soluce[0][0],soluce[0][1]),Point(0,0)]
	if len(soluce) == 2:
		return [Point(soluce[0][0],soluce[0][1]),Point(soluce[1][0],soluce[1][1])]

def Intersection(f,g):
	"""
	When f and g are objects with an attribute equation, return the list of points of intersections.

	Example (in a Sage console which has already imported phystricks)

	sage: fun=phyFunction(x**2-5*x+6)
	sage: droite=phyFunction(2)
	sage: pts = Intersection(fun,droite)
	sage: for P in pts:
	....:     print P
	....:     
	Point (4.0,2.0)
	Point (1.0,2.0)
	"""
	var('x,y')
	pts=[]
	soluce=solve([f.equation,g.equation],[x,y])
	for s in soluce:
		a=s[0].rhs()
		b=s[1].rhs()
		pts.append(Point(a,b))
	return pts

def CircleInterphyFunction(Cer,f):
	raise AttributeError,"This is depreciated, use LineInterLine instead"		#(15 oct 2010)
	return CircleInterLigne(Cer,f)

def phyFunctionInterphyFunction(f,g):
	raise AttributeError,"This is depreciated, use LineInterLine instead"		#(15 oct 2010)
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
	eq1 = l1.equation
	eq2 = l2.equation
	soluce = CalculSage().solve_more_vars( [eq1,eq2],x,y )
	s = soluce[0]
	return Point( s[0],s[1] )
	
def SinglePicture(name):
	""" Return the tuple of pspicture and figure that one needs in 90% of the cases """
	fig = GenericFigure(name)
	pspict=fig.new_pspicture(name)
	return pspict,fig

def GenericFigure(nom):
	"""
	This function returns a figure with some default values. It creates coherent label, file name and prints the lines to be appended in the LaTeX file to include the figure.
	"""
	label = "LabelFig"+nom
	caption = "\CaptionFig"+nom
	nFich = "Fig_"+nom+".pstricks"
	print "The result is on figure \\ref{"+label+"}"
	print "\\newcommand{"+caption+"}{<+Type your caption here+>}"
	print "\\input{Fig_"+nom+".pstricks}"
	return  figure(caption,label,nFich)

class figure(object):
	def __init__(self,caption,name,fich):
		self.caption = caption
		self.name = name
		self.xunit = 1
		self.yunit = 1
		self.code = []
		self.record_subfigure = []
		self.record_pspicture=[]
		self.fichier = Fichier (fich)

		# The order of declaration is important, because it is recorded in the Separator.number attribute.
		self.separator_dico = {}			
		self.separator_number = 0
		self.new_separator("ENTETE")
		self.new_separator("WRITE_AND_LABEL")
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
	def new_subfigure(self,caption,name):
		"""
		Create a subfigure in the figure and return it.

		The end-user should use this instead of append_subfigure
		"""
		ssfig=subfigure(caption,self.name+"ss"+name)
		ssfig.mother=self
		self.append_subfigure(ssfig)
		return ssfig
	def append_subfigure(self,ssFig):		# This function was initially named AjouteSSfigure
		self.record_subfigure.append(ssFig)
		suffixe = "ssFig"+str(len(self.record_subfigure))
		if not ssFig.name:
			ssFig.name=self.name+suffixe
		#ssFig.pspicture.name=self.name+"pspict"+suffixe	(no more useful 15 oct 2010)
		print r"See also the subfigure \ref{%s}"%ssFig.name
	def new_pspicture(self,name):
		pspict=pspicture("FIG"+self.name+"PICT"+name)
		pspict.mother=self
		self.add_pspicture(pspict)
		return pspict
	def add_pspicture(self,pspict):
		self.record_pspicture.append(pspict)
	def add_latex_line(self,ligne,separator_name="DEFAULT"):
		self.separator_dico[separator_name].add_latex_line(ligne)
	def IncrusteLigne(self,ligne,n):
		print "The method picture.IncrusteLigne() is depreciated."
		self.code[n:n]=ligne+"\n"
	def AjouteCode(self,liste_code):
		self.code.extend(liste_code)
	def conclude(self):
		for pspict in self.record_pspicture :
			# What has to be written in the WRITE_AND_LABEL part of the picture is written now
			self.add_latex_line(pspict.separator_dico["WRITE_AND_LABEL"].latex_code,"WRITE_AND_LABEL")
			pspict.separator_dico["WRITE_AND_LABEL"].latex_code=[]
			self.add_latex_line(pspict.contenu(),"PSPICTURE")			# Here, what is added depends on --eps
		if not globals_vars.special_exit() :
			self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+"}","BEFORE SUBFIGURES")
		for f in self.record_subfigure :
			self.add_latex_line("\subfigure["+f.caption+"]{%","SUBFIGURES")
			self.add_latex_line(f.subfigure_code(),"SUBFIGURES")
			self.add_latex_line("\label{%s}"%f.name,"SUBFIGURES")
			self.add_latex_line("}					% Closing subfigure "+str(self.record_subfigure.index(f)+1),"SUBFIGURES")
			self.add_latex_line("%","SUBFIGURES")
		after_all=r"""\caption{%s}\label{%s}
			\end{figure}
			"""%(self.caption,self.name)
		self.add_latex_line(after_all,"AFTER ALL")
		self.contenu = DicoSeparatorToCode(self.separator_dico)
	def write_the_file(self):					# Nous sommes dans la classe figure.
		self.fichier.open_file("w")
		self.fichier.file.write(self.contenu)
		self.fichier.file.close()
			
# Le \subfigure[caption]{ ne se met pas dans le code de la classe subfigure parce que dans la classe figure, je numérote les sous-figures.
# Typiquement, une sousfigure sera juste créée en ajoutant une pspicture d'un coup, et puis c'est tout.
class subfigure(object):
	"""
	This is a subfigure.

	If no label are given, a default one will be set when included in the figure.
	"""
	def __init__(self,caption,name=None):
		self.caption = caption
		self.name = name		# The label will be given in figure.append_subfigure
		#self.code = []
		self.record_pspicture=[]
		self.mother=None
	def add_latex_line(self,ligne,separator_name):
		self.mother.add_latex_line(ligne,separator_name)
	#def AjouteCode(self,cod):
	#	self.code.extend(cod)
	def new_pspicture(self,name):
		pspict=pspicture("FIG"+self.name+"PICT"+name)
		pspict.mother=self
		self.add_pspicture(pspict)
		return pspict
	def subfigure_code(self):
		a=[]
		for pspict in self.record_pspicture :
			a.append(pspict.contenu())
		return "\n".join(a)
	def add_pspicture(self,pspicture):
		#self.pspicture=pspicture		# Serves to give a name to the pspicture when the subfigure is included
		self.record_pspicture.append(pspicture)
		#self.add_latex_line(pspicture.contenu())

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

def add_latex_line_entete(truc,position="ENTETE"):
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
		try:
			text=line.code()
		except AttributeError:
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

#class LabelNotFound(exception):		#(suppressed 29 sept 2010)
#	def __init__(self,message):
#		self.message=message

class DrawElement(object):
	# The attributes take_xxx are intended to say what we have to take into account in the element.
	# If you put take_graph=False, this element will not be drawn, but its bounding boxes are going to be taken into account.
	def __init__(self,graphe,separator_name,take_graph=True,take_BB=True,take_math_BB=True,*args):
		self.take_graph=take_graph
		self.take_BB=take_BB
		self.take_math_BB=take_math_BB
		self.graph=graphe
		self.separator_name=separator_name
		self.st_args=args

class pspicture(object):
	r"""
	self.pstricks_code contains the pstricks code of what has to be between \begin{pspicture} and \end{pspicture}. This is not the environment itself, neither the definition of xunit, yunit.
	self.contenu_pstricks() is the whole code including the x/yunit
	self.contenu_eps() contains the line to be added in order to include the eps file
	"""
	NomPointLibre = ListeNomsPoints()

	def __init__(self,name="CAN_BE_A_PROBLEM_IF_TRY_TO_PRODUCE_EPS_OR_PDF"):
		r"""
		A name is required for producing intermediate files. This is the case when one wants to produce eps/pdf files of one wants to 
		   make interactions with LaTeX (see pspict.get_counter_value).

		   self.BB is the bounding box for LaTeX purpose.
		   	Graph object need to have a method bounding_box
		   self.math_BB is the bounding box of objects that are "mathematically relevant". This bounding box does not take into account
		   	marks of points and thinks like that. This is the bounding box that is going to be used for the axes and the grid.
			When a graph object has a method math_bounding_box, this is the one taken into account in the math_BB here.
		"""
		self.name = name		# self.name is used in order to name the intermediate files when one produces the eps file.
		self.mother=None
		self.pstricks_code = []
		self.specific_needs = ""	# See the class PspictureToOtherOutputs
		self.newwriteDone = False
		self.interWriteFile = newwriteName()+".pstricks.aux"
		self.NomPointLibre = ListeNomsPoints()
		self.record_marks=[]
		self.record_bounding_box=[]
		self.record_draw_graph=[]
		self.record_force_math_bounding_box=[]
		#self.record_math_BB=[]
		#self.record_BB=[]
		self.counterDone = False
		self.newlengthDone = False
		self.listePoint = []
		self.xunit = 1
		self.yunit = 1
		self.LabelSep = 1
		self.BB = BoundingBox(Point(1000,1000),Point(-1000,-1000))
		self.math_BB = BoundingBox(Point(1000,1000),Point(-1000,-1000))		# self.BB and self.math_BB serve to add some objects by hand.
											# If you need the bounding box, use self.bounding_box()
											# or self.math_bounding_box()
		self.axes = Axes( Point(0,0),BoundingBox(Point(1000,1000),Point(-1000,-1000))  )
		self.grid = Grid(self.axes.bounding_box())
		# We add the "anchors" %GRID and %AXES in order to force the axes and the grid to be written at these places.
		#    see the functions DrawAxes and DrawGrid and the fact that they use IncrusteLigne

		# The order of declaration is important, because it is recorded in the Separator.number attribute.
		self.separator_dico = {}			
		self.separator_number = 0
		self.new_separator("ENTETE")
		self.new_separator("BEFORE PSPICTURE")
		self.new_separator("WRITE_AND_LABEL")
		self.new_separator("BEGIN PSPICTURE")
		self.new_separator("GRID")
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
			self.add_latex_line(code,"WRITE_AND_LABEL")
			self.newwriteDone = True
	def initialize_counter(self):
		if not self.counterDone:
			code = r""" \makeatletter 
				\@ifundefined{c@%s}			
				{\newcounter{%s}}
				\makeatother
				"""%(counterName(),counterName())			# make LaTeX test if the counter exist before to create it.
			self.add_latex_line(code,"WRITE_AND_LABEL")
			self.counterDone = True
	def initialize_newlength(self):
		if not self.newlengthDone :
			code =r"""
			\makeatletter
			\@ifundefined{%s}{\newlength{\%s}}
			\makeatother
			"""%(newlengthName(),newlengthName())
			self.add_latex_line(code,"WRITE_AND_LABEL")
			self.newlengthDone = True
	def add_write_line(self,Id,value):
		r"""Writes in the standard auxiliary file \newwrite an identifier and a value separated by a «:»"""
		interWriteName = newwriteName()
		self.initialize_newwrite()
		self.add_latex_line(r"\immediate\write\%s{%s:%s:}"%(interWriteName,Id,value),"WRITE_AND_LABEL")
	def get_Id_value(self,Id,counter_name="NO NAME ?",default_value=0):
		try :
			f=open(self.interWriteFile)
		except IOError :
			print "Warning : the auxiliary file seems not to exist. Compile your LaTeX file."
			return default_value
		text = f.read().replace('\n','').split(":")
		try:
			return text[text.index(Id)+1]			
		except ValueError :
			print "Warning : the auxiliary file does not contain the id «%s». Compile your LaTeX file."%Id
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
		self.add_latex_line(r"\setlength{\%s}{\%s{%s}}"%(newlengthName(),dimension_name,tex_expression),"WRITE_AND_LABEL")
		self.add_write_line(interId,r"\the\%s"%newlengthName())
		read_value =  self.get_Id_value(interId,"dimension %s"%dimension_name,default_value="0pt") 
		dimenPT = float(read_value.replace("pt",""))
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
	def AddPoint(self,P):
		self.add_latex_line(self.CodeAddPoint(P))
	def bounding_box(self,pspict=None):
		bb=self.BB
		for a in [x.graph.bounding_box(self) for x in self.record_draw_graph if x.take_math_BB or x.take_BB] :
			bb.AddBB(a)
		return bb
	def DrawBB(self):
		self.DrawBoundingBox(self.BB)
	def DrawBoundingBox(self,obj=None,color="cyan"):
		"""Draw the bounding box of an object when it has a method bounding_box

		If not, assume that the object is the bounding box to be drawn.
		If no object are given, draw its own bounding box
		"""
		if not obj:
			obj=self
		self.record_bounding_box.append(obj)
	# Ici, typiquement, symbol sera "*" et params sera vide.
	def DrawPoint(self,P,symbol,params):
		print "This method is depreciated"
		raise AttributeError
		return self._DrawPoint(self,P,symbol,params)

	def TraceNuage_de_Points(self,nuage,symbol,params):
		self.add_latex_line("% ---------Nuage de point--------")
		for P in nuage.listePoints :
			self.DrawPoint(P,symbol,params)

	def MarqueAngle(self,A,B,C,label,params):
		self.add_latex_line("\pstMarkAngle["+params+"]{"+A.psName+"}{"+B.psName+"}{"+C.psName+"}{"+label+"}")
	def TraceCourbeParametrique(self,f,mx,Mx,params):
		raise AttributeError,"The method TraceCourbeParametrique is depreciated"
		self.BB.AddParametricCurve(f,mx,Mx)
		self.add_latex_line("\parametricplot[%s]{%s}{%s}{%s}" %(params,str(mx),str(Mx),f.pstricks()))
	def DrawGraphs(self,*args):
		for g in args:
			self.DrawGraph(g)
	def DrawGraph(self,graphe,separator_name=None):
		"""
		Draw an object of type GraphOfA*.

		More generally, it can draw anything that has the methods
			bounding_box
			pstricks_code
		The first one should return a bounding box and the second one should return a valid pstricks code as string. 
		If the pstricks code is not valid, LaTeX will get angry but no warning are given here.
		"""
		if separator_name==None:
			try :
				separator_name=graphe.separator_name
			except AttributeError :
				separator_name="DEFAULT"
		x=DrawElement(graphe,separator_name)
		self.record_draw_graph.append(x)
	def DrawGrid(self,grid):
		print "This is depreciated. The grid has to be drawn with DrawGraph as everyone"
		raise
	def TraceTriangle(self,tri,params):
		print "Method TraceTriangle is depreciated"
		raise AttributeError
		self.BB.AddPoint(tri.A)
		self.BB.AddPoint(tri.B)
		self.BB.AddPoint(tri.C)
		self.add_latex_line("\pstTriangle["+params+",PointSymbol=none]"+tri.A.coordinates()+"{A}"+tri.B.coordinates()+"{B}"+tri.C.coordinates()+"{C}")
	def TraceGrid(self,grille):
		self.IncrusteLigne(grille.code(self),2)
	def AjusteGrid(self,grille):
		grille.BB = self.BB
	def DrawAxes(self,axes):
		print "This method is depreciated"
		raise AttributeError
	def DrawDefaultAxes(self):
		self.axes.BB = self.math_bounding_box()
		self.axes.BB.AddPoint(Point(0,0))
		epsilonX=float(self.axes.Dx)/2
		epsilonY=float(self.axes.Dy)/2
		self.axes.BB.enlarge_a_little(self.axes.Dx,self.axes.Dy,epsilonX,epsilonY)
		self.DrawGraph(self.axes)
	def DrawDefaultGrid(self):
		self.grid.BB = self.math_bounding_box()
		Dx=self.grid.Dx
		Dy=self.grid.Dy
		epsilonX=0
		epsilonY=0
		self.grid.BB.enlarge_a_little(Dx,Dy,epsilonX,epsilonY)	# Make the grid end on its "big" subdivisions.
		self.DrawGraph(self.grid)
	def add_latex_line(self,ligne,separator_name="DEFAULT"):
		"""
		Add a line in the pstricks code. The optional argument <position> is the name of a marker like %GRID, %AXES, ...
		"""
		if separator_name==None:
			separator_name="DEFAULT"
		if separator_name=="WRITE_AND_LABEL" and self.mother :
			self.mother.add_latex_line(ligne,separator_name)
		else :
			self.separator_dico[separator_name].add_latex_line(ligne)
	def IncrusteLigne(self,ligne,n):
		print "The method pspicture.IncrusteLigne() is depreciated."
		self.pstricks_code[n:n]=ligne+"\n"
	def contenu_eps(self):
		to_eps = PspictureToOtherOutputs(self)
		to_eps.create_eps_file()
		return to_eps.input_code_eps
	def contenu_pdf(self):
		print "contenu_pdf"
		to_pdf = PspictureToOtherOutputs(self)
		to_pdf.create_pdf_file()
		return to_pdf.input_code_pdf
	def contenu_pstricks(self):					# class pspicture
		"""
		One has to declare the xunit,yunit before to give the bounding box. The value of LabelSep is the distance between an angle and the lable of the angle. It is by default 1, but if there is a dilatation, the visual effect is bad.
		"""
		if self.LabelSep == 1 : 
			self.LabelSep = 2/(self.xunit+self.yunit)
		add_latex_line_entete(self)
		self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+",LabelSep="+str(self.LabelSep)+"}","BEFORE PSPICTURE")
		self.add_latex_line("\psset{PointSymbol=none,PointName=none,algebraic=true}\n","BEFORE PSPICTURE")
		self.add_latex_line("\\begin{pspicture}%s%s\n"%(self.bounding_box(self).SW().coordinates(),self.bounding_box(self).NE().coordinates()),"BEGIN PSPICTURE")
		self.add_latex_line("\end{pspicture}\n","AFTER PSPICTURE")
		self.add_latex_line(self.pstricks_code,"OTHER STUFF")
		return DicoSeparatorToCode(self.separator_dico)
	def force_math_bounding_box(self,g):
		"""
		Add an object to the math bounding box of the pspicture. This object will not be drawn, but the axes and the grid will take it into account.
		"""
		self.record_force_math_bounding_box.append(g)
	def math_bounding_box(self):
		"""
		Return the current BoundingBox, that is the BoundingBox of the objects that are currently in the list of objects to be drawn.
		"""
		bb = self.math_BB.copy()
		for graphe in [x.graph for x in self.record_draw_graph if x.take_math_BB]:
			try :
				bb.AddBB(graphe.math_bounding_box(self))
			except AttributeError:
				print "Warning: it seems to me that object %s has no method math_boundig_box"%str(graphe)
				bb.add_graph(graphe,self)
		return bb
	def contenu(self):
		"""
		Notice that if the option --eps/pdf is given, this method launches some compilations when creating contenu_eps/pdf 
		"""
		# Here we are supposed to be sure of the xunit, yunit, so we can compute the BB's needed for the points with marks.
		# For the same reason, all the marks that were asked to be drawn are added now.
		# Most of the difficulty is when the user use pspicture.dilatation_X and Y with different coefficients.
		list_to_be_drawn = [a.graph for a in self.record_draw_graph if a.take_graph]
		for graph in list_to_be_drawn:
			try :
				if graph.draw_bounding_box:
					bb=graph.bounding_box(self)
					rect = Rectangle(bb.SW(),bb.NE())
					rect.parameters.color="cyan"
					self.DrawGraph(rect)
			except AttributeError :
				pass
		list_to_be_drawn = [a for a in self.record_draw_graph if a.take_graph]
		for x in list_to_be_drawn:
			graph=x.graph
			separator_name=x.separator_name
			try :
				if graph.marque:
					self.BB.AddBB(graph.mark.bounding_box(self))
					self.add_latex_line(graph.mark.pstricks_code(self))
			except AttributeError :
				pass
			try :
				self.BB.add_graph(graph,self)
				self.add_latex_line(graph.pstricks_code(self),separator_name)
			except AttributeError,data:
				if not "pstricks_code" in dir(graph):
					print "phystricks error : object %s has no pstricks_code method"%(str(graph))
					raise 
		for sortie in globals_vars.list_exits:
			if globals_vars.__getattribute__(sortie+"_exit"):
				print "I've to make an exit : %s"%sortie
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
