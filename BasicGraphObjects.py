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
		a.append("\pstGeonode["+graphe.params()+"]"+self.coordinates()+"{"+self.psNom+"}")
		if graphe.marque :
			mark = graphe.mark
			if p.psNom not in self.listePoint :
				self.AddPoint(p)
			a.append("\\rput(%s){\\rput(%s;%s){%s}}"%(p.psNom,str(mark.dist),str(mark.angle),str(mark.mark)))
		return "\n".join(a)

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
