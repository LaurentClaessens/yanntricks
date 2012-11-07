# -*- coding: utf8 -*-

###########################################################################
#   This is part of the module phystricks
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

# copyright (c) Laurent Claessens, 2010,2012
# email: moky.math@gmai.com

"""
This module uses phystricks in order to produces some mathematical situations/

"""

from __future__ import division
from sage.all import *
from phystricks import *


# La classe Description_Dynkin décrit la mathématique de Dynkin : elle n'a pas les informations sur les sigles qu'on veut mettre sur les racines.
# Le paramètre ll est une liste de "o" et "*" suivant que la racine ait une norme maximale ou non (cerle plein ou vide dans Dynkin)
# __init__ donne des valeurs par défaut. Par exemples les racines sont mises en ligne droite, et la matrice d'adjacence est nulle.
class Dynkin(object):
    def __init__(self,descr,deco):
        self.description = descr
        self.decoration = deco
    def action_on_pspict(self,pspict):
        n = len( self.Adjacence )
        for i in range(0,n):
            for j in range(0,n):
                seg=Segment(self.ronds[i],self.ronds[j]) 
                if self.Adjacence[i][j]==1:
                    pass
                elif self.Adjacence[i][j]==2:
                    seg.add_option("doubleline=true")
                elif self.Adjacence[i][j]==4:
                    seg.parameters.style='dotted'
                # TODO : I have to make the case with 3 lines, but I don't know how to do
                pspict.DrawGraphs(seg)
        for i in range(0,n):
                self.MarkThePoint(self.ronds[i],distMark[i],angleMark[i],remplissure[i],visMark[i])




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
		xnn = xn - (self.P.y)/newton.f.derivative()(xn)			# The Newton's iteration formula is here
		self.B = Point(xnn,0)
		self.vertical_segment = Segment(self.A,self.P)
		self.diagonal_segment = Segment(self.P,self.B).dilatation(1.5)

class NewtonMethod():
	def __init__(self,f):
		self.f = f
	def step_from_point(self,xn):
		return NewtonMethodStep(self,xn)



class Old_Stuff(object):
    def TraceYoung(self,Y):
        for i in range(0,len(Y.diagramme)):
            for j in range(0,len(Y.diagramme[i])):
                self.TraceRectangle( Rectangle( Point(j,-i),Point(j+1,-i-1) ),"" )
                self.MarkThePoint( Point(j,-i), 0.5,-45,"none", Y.diagramme[i][j] )
