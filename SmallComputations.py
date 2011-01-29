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

def DegreeAngleMeasure(x):
	return AngleMeasure(value_degree=x)
def RadianAngleMeasure(x):
	return AngleMeasure(value_radian=x)

class AngleMeasure(object):
	"""
	sage: x=AngleMeasure(value_radian=pi/2)
	sage: x()
	28.647889756541161*pi
	sage: numerical_approx(x())
	90.0000000000000


	in that case, y has to be a new instance of AngleMeasure :
	x=AngleMeasure(value_degree=180)
	y=AngleMeasure(x)
	"""
	def __init__(self,value_degree=None,value_radian=None):
		if isinstance(value_degree,AngleMeasure):
			return AngleMeasure(value_degree=value_degree.degree)

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

def PointToPolaire(P=None,x=None,y=None):
	"""
	Return the polar coordinates of a point.

	If you give a point as argument, numerical approximations are returned (because the coordinated of a point is automatically numerically approximed)
	If you explicitelly provides x and y, exact values are returned.

	sage: from phystricks import *     
	sage: print PointToPolaire(x=1,y=1)
	PolarCoordinates, r=sqrt(2),degree=14.323944878270581*pi,radian=1/4*pi	# Exact : pi/4
	sage: print PointToPolaire(Point(1,1))
	PolarCoordinates, r=1.41421356237,degree=45.0,radian=0.785398163397	# Approximation : 0.785...
	"""
	if P:
		x=P.x
		y=P.y
	r = sqrt(x**2+y**2)
	if x == 0:
		if y > 0:
			alpha = pi/2
		if y < 0:
			alpha = pi/2
		if y == 0 : 			# Convention : the angle for point (0,0) is 0.
			print "phystricks Warning. You are trying to convert into polar coordinates the point (0,0). I'm returning 0 as angle."
			alpha = 0
	else :
		alpha = atan(y/x)
	if not P :
		alpha=alpha.simplify_trig()
	if (x < 0) and (y == 0) :
		alpha = pi
	if (x < 0) and (y > 0) :
		alpha = alpha + pi
	if (x < 0) and (y < 0 ) :
		alpha = alpha +pi
	return PolarCoordinates(r,value_radian=alpha)

class ConversionAngles(object):
	def __init__(self,conversion_factor,max_value,exit_attribute=None,create_function=None):
		self.conversion_factor=conversion_factor
		self.max_value=max_value
		self.exit_attribute=exit_attribute
		self.create_function=create_function
	def simplify(self,angle,keep_max=False,number=False):
		"""
		Simplify the angles modulo the maximum. 

		If what is given is a numbre, return a number. If what is given is a AngleMeasure, return a new AngleMeasure
	
		EXAMPLE:
		sage:from phystricks import *
		sage:simplify_degree=ConversionAngles(180.0/pi,360).simplify
		sage:simplify_degree(400)
		40

		If <keep_max> is True, maximal values are kept:
		sage: simplify_degree(400,keep_max=True)
		40
		sage: simplify_degree(360,keep_max=True)
		360

		if <number> is True, return a number even is a AngleMeasure is given.
		"""
		if isinstance(angle,AngleMeasure) :
			x=angle.__getattribute__(self.exit_attribute)
			gotMeasure=True
		else :
			x=angle
			gotMeasure=False
		if keep_max and x == self.max_value:
			if gotMeasure and number==False:
				return angle
			else :
				return self.max_value
		while x >= self.max_value :
			x=x-self.max_value
		while x < 0 :
			x=x+self.max_value
		if gotMeasure and number==False :
			return self.create_function(x)
		else :
			return x
	def conversion(self,theta,number=False,keep_max=False,converting=True):
		"""
		Makes the conversion and simplify.

		The arguments <number> and <keep_max> are the same as the ones in SimplifyAngles.simplify.

		If <converting> is False, make no conversion.

		sage: from phystricks import *                         
		sage: degree=ConversionAngles(180.0/math.pi,360).conversion
		sage: degree(7)                         
		-126*pi + 401.070456591576
		sage: numerical_approx(degree(7))
		5.22978223926231
		sage: degree(120,converting=False)
		120

		Using converting=False,number=True is a way to ensure something to be a number instead of a AngleMeasure
		"""
		if isinstance(theta,AngleMeasure):
			angle = self.simplify(theta,keep_max=keep_max)
			if number:
				 return angle.__getattribute__(self.exit_attribute)
			else :
				return angle
		else :
			if converting :
				return self.simplify(self.conversion_factor*theta,keep_max=keep_max)
			else :
				return self.simplify(theta,keep_max=keep_max)

DegreeConversions=ConversionAngles(180.0/math.pi,360,exit_attribute="degree",create_function=DegreeAngleMeasure)
RadianConversions=ConversionAngles(math.pi/180,2*pi,exit_attribute="radian",create_function=RadianAngleMeasure)

simplify_degree=DegreeConversions.simplify
simplify_radian=RadianConversions.simplify
degree=DegreeConversions.conversion
radian=RadianConversions.conversion

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

