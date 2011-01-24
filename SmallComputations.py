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
This submodule contains functions that perform small computations for phystricks. 
The return values of the functions here are instances of classical classes, not from phystricks classes.
"""

import math
from sage.all import *


def MultipleLower(x,m):
	""" return the biggest multiple of m which is lower or equal to x"""
	return floor(x/m)*m

def MultipleBigger(x,m):
	""" return the lower multiple of m which is bigger or equal to x"""
	return ceil(x/m)*m

def enlarge_a_little_up(x,m,epsilon):
	"""
	see the description of the function enlarge_a_little of the class BoundingBox.
	This function makes the job for one number.
	"""
	if int(x/m) == x/m:
		return x+epsilon
	else : 
		return MultipleBigger(x,m)+epsilon
		
def enlarge_a_little_low(x,m,epsilon):
	"""
	see the description of the function enlarge_a_little of the class BoundingBox.
	This function makes the job for one number.
	"""
	if int(x/m) == x/m:
		return x-epsilon
	else : 
		return MultipleLower(x,m)-epsilon

class AngleMeasure(object):
	"""
	sage: x=AngleMeasure(value_radian=pi/2)
	sage: x()
	28.647889756541161*pi
	sage: numerical_approx(x())
	90.0000000000000
	"""
	def __init__(self,value_degree=None,value_radian=None):
		if value_degree == None :
			value_degree=degree(value_radian)
		if value_radian == None :
			value_radian=radian(value_degree)
		self.degree=value_degree
		self.radian=value_radian
		if self.degree==None or self.radian==None:
			raise ValueError,"Something wrong"
	def __mul__(self,coef):
		return AngleMeasure(value_radian=coef*self.radian)
	def __rmul__(self,coef):
		return self*coef
	def __sub__(self,other):
		return AngleMeasure(value_radian=self.radian-other.radian)
	def __call__(self):
		return self.degree
	def __div__(self,coef):
		return AngleMeasure(value_radian=self.radian/coef)
	def __cmp__(self,other):
		if isinstance(other,AngleMeasure):
			if self.degree > other.degree :
				return 1
			if self.degree < other.degree :
				return 1
			if self.degree == other.degree :
				return 0
	def __str__(self):
		return "AngleMeasure, degree=%s,radian=%s"%(str(numerical_approx(self.degree)),str(self.radian))

class PolarCoordinates(object):
	def __init__(self,r,value_degree=None,value_radian=None):
		self.r = r
		self.measure=AngleMeasure(value_degree,value_radian)
		self.degree=self.measure.degree
		self.radian=self.measure.radian
	def __str__(self):
		return "PolarCoordinates, r=%s,degree=%s,radian=%s"%(str(self.r),str(self.degree),str(self.radian))

def PointToPolaire(P):
	"""
	Return the polar coordinates of a point.
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
		alpha = math.atan(P.y/P.x)
	if (P.x < 0) and (P.y == 0) :
		alpha = math.pi
	if (P.x < 0) and (P.y > 0) :
		alpha = alpha + math.pi
	if (P.x < 0) and (P.y < 0 ) :
		alpha = alpha +math.pi
	return PolarCoordinates(r,value_radian=alpha)

class SimplifyAngles(object):
	def __init__(self,max_value):
		self.max_value=max_value
	def simplify(angle,keep_max=False,number=False)
		if isinstance(angle,AngleMeasure) :
			x=angle.degree
			gotMeasure=True
		else :
			x=angle
			gotMeasure=False
		if keep_max and x == max_value:
			return max_value
		while x >= max_value :
			x=x-max_value
		while x < 0 :
			x=x+max_value
		if gotMeasure and number==False :
			return AngleMeasure(value_degree=x)
		else :
			return x

class ConversionAngles(object):
	def __init__(self,factor):
		self.factor=factor
	def conversion(theta,number=False,keep_max=False,converting=True):
		if isinstance(theta,AngleMeasure):
			return simplify_radian(theta,number=number,keep_max=keep_max)
		else :
			if converting :
				return simplify_radian(theta*factor,keep_max=keep_max)
			else :
				return simplify_radian(theta,keep_max=keep_max)

simplify_degree=SimplifyAngles(360).simplify
simplify_radian=SimplifyAngles(2*pi).simplify

degree=ConversionAngles(180.0/math.pi).conversion
radian=ConversionAngles(math.pi/180).conversion

def Distance_sq(P,Q):
	""" return the squared distance between P and Q """
	return (P.x-Q.x)**2+(P.y-Q.y)**2

def Distance(P,Q):
	""" return the distance between P and Q """
	return math.sqrt(Distance_sq(P,Q))

# Convention : theta is in degree while alpha is in gradient.
#def radian(theta,number=False,converting=True,keep_max=False):
	#"""
	#Convert from degree to radian. Return a value between 0 and 2pi (not 2pi itself)
	#"""
	#if isinstance(theta,AngleMeasure):
		#return simplify_radian(theta,number=number,keep_max=keep_max)
	#else :
		#if converting :
			#return simplify_radian(theta*math.pi/180,keep_max=keep_max)
		#else :
			#return simplify_radian(theta,keep_max=keep_max)
#def degree(alpha,number=False,converting=True,keep_max=False):
	#"""Convert from radian to degree. Return a value between 0 and 360 (not 360 itself)"""
	#if isinstance(alpha,AngleMeasure):
		#return simplify_degree(alpha,numbre=number,keep_max=keep_max)
	#else :
		#return simplify_degree(180*alpha/math.pi)

