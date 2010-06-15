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
This module uses phystricks in order to produces graphics of the grading. 

From a list of number, we can generate 3 graphics
1. y = percent of students which obtained more or equal to x
(to be implemented):
2. y = average points of the students who obtained more or equal to x
1. y = number of students who obtained x plus or minus 1.

"""

from __future__ import division
import commands, os, copy, math	
from sage.all import *
from phystricks import *

REP = commands.getoutput("pwd")

def PercentHaveMore(cotes,n):
	return ProportionHaveMore(cotes,n)*100

def ProportionHaveMore(cotes,n):
	"""
	Returns the proportion of elements in cotes that are bigger than n
	"""
	return HaveMore(cotes,n)/len(cotes)

def HaveMore(cotes,n):
	"""
	returns the number of elements of the list cotes that are bigger than n
	"""
	return len(ListHaveMore(cotes,n))

def ListHaveMore(grades,n):
	""" return the list of points that are bigger than n"""
	return [p for p in grades if p>=n]

def Average(cotes):
	"""return the average of the list"""
	return float(sum(cotes))/len(cotes)

def AverageBigger(cotes,n):
	"""return the average of grades that are bigger than n"""
	return Average(ListHaveMore(cotes,n))

class Grades(object):
	"""
	grades_list : the list of grades that are given.
	full_grade : the maximal note
	"""
	def __init__(self,grades_list,full_grade):
		self.grades_list = grades_list
		self.full_grade = full_grade
	def convert_to_full_grade(self,n):
		""" return the list of grades if the maximum is n instead of self.full_grade """
		return Grades([c*n/self.full_grade for c in self.grades_list],n)
	def y_is_percent_bigger_than_x(self,pspictName):
		"""
		Return the pspict that represents the graph of the function
		y(x) = proportion of the students that have x or more.

		The intervals are X=[0,self.full_grade] and Y=[0,1]
		"""
		pspict=pspicture(pspictName)
		for x in range(0,self.full_grade+1):
			y = ProportionHaveMore(self.grades_list,x)
			p = Point( x, y )
			P = Graph(p)
			P.parameters.color = "blue"
			pspict.DrawGraph(P)

		segment = Segment( Point(0,0.5),Point(self.full_grade,0.5) )
		S = Graph(segment)
		S.parameters.color = "red"
		pspict.DrawGraph( S )

		pspict.grid.Dy = 0.1
		pspict.grid.num_subX = 0
		pspict.grid.num_subY = 5
		pspict.axes.Dy = 0.1
		pspict.DrawDefaultAxes()
		pspict.DrawDefaultGrid()
		return pspict
	def average_bigger(self,pspictName):
		"""
		return the pspict that represents the graph of the function
		y(x)=average of grades that are bigger than x

		The intervals are X=[0,self.full_grade] and Y=[0,self.full_grade]
		"""
