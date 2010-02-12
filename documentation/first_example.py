#! /usr/bin/sage -python
# -*- coding: utf8 -*-

from phystricks import *

def OnePoint():
	pspict=pspicture("OnePoint")
	fig = GenericFigure("OnePoint")				# Generic name of the figure

	##################### The main lines are here
	p = Point(1,1)
	P = Graph(p)
	P.color = "red"
	pspict.DrawGraph(P)
	########################

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()

OnePoint()
