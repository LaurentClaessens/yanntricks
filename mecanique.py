# -*- coding: utf8 -*-

"""
Classes that represent mechanical situations.
"""

from sage.all import *
from phystricks import *
import math

class TirOblilque(object):
	"""
The trajectory of an object launched with angle alpha (in radiant). 

Arguments

P :	strarting point
v :	velocity (m/s because g is given by 9.81)
alpha :	the angle in radiant

Returns
self.depart :	is the starting point (P)
self.v1 :	is the x component of the velocity
self.v2 :	is the y component of the velocity
self.F :	is the curve given as a phystricks.CourbeParametrique 
self.Dt :	is the value of the parameter (time) where the object reach the ground. It solves self.F.f2 == 0
	"""
	def __init__(self,P,v,alpha):
		g = 9.81
		self.depart = P
		self.v1 = v * math.cos(alpha)
		self.v2 = v * math.sin(alpha)
		var('x')
		self.f1 = Fonction(P.x+self.v1*x)
		self.f2 = Fonction(P.y+self.v2*x-g*x**2/2)
		self.F = CourbeParametrique(self.f1,self.f2)
		# Trouver pour quel x la hauteur s'annule. C'est jusque là qu'il faudra tracer.
		# On veut évidement la solution positive.
		sol = solve(self.f2.sage == 0,x)
		for xS in [ s.rhs() for s in sol ]:
			if xS > 0: self.Dt = numerical_approx(xS)

