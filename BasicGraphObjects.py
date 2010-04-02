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
This module contains the basic Graph objects (the correspond to the basics geometrical objectc)
"""

import math
from sage.all import *
from SmallComputations import *
from BasicGeometricObjects import *



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

	def add_graph(self,graphe,pspict):
		self.AddBB(graphe.bounding_box(pspict))
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
	def code_pstricks(self):
		a = []
		a.append("\pstGeonode["+self.params()+"]"+self.coordinates()+"{"+self.psNom+"}")
		if self.marque :
			mark = self.mark
			a.append("\\rput(%s){\\rput(%s;%s){%s}}"%(self.psNom,str(mark.dist),str(mark.angle),str(mark.text)))
		return "\n".join(a)

class GraphOfASegment(GraphOfAnObject):
	def __init__(self,seg):
		GraphOfAnObject.__init__(self,seg)
		self.seg = self.obj
		self.I = self.seg.I
		self.F = self.seg.F
	def bounding_box(self,pspicture=1):
		return BoundingBox(self.I,self.F)


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
