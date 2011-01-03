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

def ListBetween(cotes,n,delta):
	"""return the list of grades in [n-delta,n+delta]"""
	return [p for p in cotes if p>=n-delta and p<=n+delta]

def ProportionBetween(cotes,n,delta):
	"""return the proportion of grades in [n-delta,n+delta]"""
	a=ListBetween(cotes,n,delta)
	return float(len(a))/len(cotes)


class Grades(object):
	"""
	grades_list : the list of grades that are given.
	full_grade : the maximal note
	"""
	def __init__(self,grades_list,full_grade):
		self.grades_list = grades_list
		self.full_grade = float(full_grade)
		self.media = self.full_grade/2
	def convert_to_full_grade(self,n):
		""" return the list of grades if the maximum is n instead of self.full_grade """
		return Grades([c*n/self.full_grade for c in self.grades_list],n)
	def y_is_proportion_bigger_than_x(self,pspictName,tailleX=15,tailleY=10):
		"""
		Return the pspict that represents the graph of the function
		y(x) = proportion of the students that have x or more.

		The intervals are X=[0,self.full_grade] and Y=[0,1]
		"""
		pspict=pspicture(pspictName)
		abcisses=self.grades_list
		abcisses.extend([0,self.full_grade,self.full_grade/2])
		for x in abcisses:
			y = ProportionHaveMore(self.grades_list,x)
			P = Point( x, y )
			P.parameters.color = "blue"
			pspict.DrawGraph(P)

		S = Segment( Point(self.media,0),Point(self.media,1) )
		S.parameters.color = "red"
		pspict.DrawGraph(S)

		pspict.grid.Dy = 0.1
		pspict.grid.num_subX = 0
		pspict.grid.num_subY = 5
		pspict.axes.Dy = 0.1
		pspict.DrawDefaultGrid()
		pspict.DrawDefaultAxes()
		pspict.dilatation_X(float(tailleX)/self.full_grade)
		pspict.dilatation_Y(tailleY)
		return pspict
	def average_bigger(self,pspictName):
		"""
		return the pspict that represents the graph of the function
		y(x)=average of grades that are bigger than x

		The intervals are X=[0,self.full_grade] and Y=[0,self.full_grade]
		"""
		pspict=pspicture(pspictName)
		abcisses=self.grades_list
		abcisses.extend([0,self.full_grade,self.full_grade/2])
		for x in abcisses:
			y = AverageBigger(self.grades_list,x)
			P = Point( x, y )
			P.parameters.color = "blue"
			pspict.DrawGraph(P)

		segmentH = Segment( Point(0,self.media),Point(self.full_grade,self.media) )
		segmentH.parameters.color = "red"
		pspict.DrawGraph(segmentH)
		segmentV = Segment( Point(self.media,0),Point(self.media,self.full_grade) )
		segmentV.parameters.color = "red"
		pspict.DrawGraph(segmentV)
		pspict.math_BB.AddPoint(Point(0,0))

		pspict.grid.Dy = 1
		pspict.grid.num_subX = 0
		pspict.grid.num_subY = 5
		pspict.axes.Dy = 1
		pspict.DrawDefaultGrid()
		pspict.DrawDefaultAxes()
		return pspict
	def proportion_between(self,pspictName,delta=1):
		"""
		return the pspict that represents the graph of the function
		y(x)=proportion of students in [x-delta,x+delta].

		The intervals are X=[0,self.full_grade] and Y=[0,1]
		"""
		pspict=pspicture(pspictName)
		abcisses=self.grades_list
		abcisses.extend([0,self.full_grade,self.full_grade/2])
		for x in abcisses:
			y = ProportionBetween(self.grades_list,x,delta)
			P = Point( x, y )
			P.parameters.color = "blue"
			pspict.DrawGraph(P)

		#pspict.math_BB.AddPoint(Point(0,0))

		pspict.grid.Dy = 0.1
		pspict.grid.num_subX = 0
		pspict.grid.num_subY = 5
		pspict.axes.Dy = 0.1
		pspict.DrawDefaultGrid()
		pspict.DrawDefaultAxes()
		return pspict
	def all_statistics(self,name,delta=1):
		"""
		Create all the figures and write them in files.
		"""
		self.y_is_proportion_bigger_than_x(name+"pcb").write_the_figure_file("svt")
		self.average_bigger(name+"avb").write_the_figure_file("svt")
		self.proportion_between(name+"pbt",delta=1).write_the_figure_file("svt")
	def __str__(self):
		return str(self.grades_list)
