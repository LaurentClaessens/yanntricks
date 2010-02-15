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
This module uses phystricks in order to produces some mathematical situations/

"""

from __future__ import division
from sage.all import *
from phystricks import *

class NewtonMethodStep():
	"""
	Return the informations about one step of the Newton method.

	self.A : the starting x value
	self.P : the starting point on the graph
	self.B : the next point
	self.vertical_segment : the Segment from the point (xn,0) and the point P
	self.diagonal_segment : the Segment which joins the point P and x_{n+1}
	"""
	def __init__(self,newton,xn):
		self.A = Point(xn,0)
		self.P = newton.f.get_point(xn)
		xnn = xn - (self.P.y)/newton.f.derivative().eval(xn)			# The Newton's iteration formula is here
		self.B = Point(xnn,0)
		self.vertical_segment = Segment(self.A,self.P)
		self.diagonal_segment = Segment(self.P,self.B).dilate(1.5)

class NewtonMethod():
	def __init__(self,f):
		self.f = f
	def step_from_point(self,xn):
		return NewtonMethodStep(self,xn)
