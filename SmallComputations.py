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

#class coordinatesPolaires(object):
class PolarCoordinates(object):
	def __init__(self,r,value_degree=None,value_radian=None):
		self.r = r
		if value_degree == None :
			value_degree=degree(value_radian)
		if radian == None :
			value_radian=radian(value_degree)
		self.degree=value_degree
		self.radian=value_radian
		if self.degree==None or self.radian==None:
			raise ValueError,"Something wrong"
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

def simplify_degree(angle,keep_max=False):
	if keep_max and angle == 360:
		return 360
	while angle >= 360 :
		angle=angle-360
	while angle < 0 :
		angle=angle+360
	return angle
def simplyfy_radian(angle,keep_max=False):
	if keep_max and angle == 2*pi:
		return 2*pi
	while angle >= 2*pi :
		angle=angle-2*pi
	while angle < 0 :
		angle=angle+2*pi
	return angle
# Convention : theta is in degree while alpha is in gradient.
def radian(theta):
	"""Convert from degree to radian. Return a value between 0 and 2pi (not 2pi itself)"""
	angle = theta*math.pi/180
	return simplyfy_radian(angle)
def degree(alpha):
	"""Convert from radian to degree. Return a value between 0 and 360 (not 360 itself)"""
	angle = 180*alpha/math.pi
	return simplify_degree(angle)

def Distance_sq(P,Q):
	""" return the squared distance between P and Q """
	return (P.x-Q.x)**2+(P.y-Q.y)**2

def Distance(P,Q):
	""" return the distance between P and Q """
	return math.sqrt(Distance_sq(P,Q))
