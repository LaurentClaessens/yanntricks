#! /usr/bin/sage -python
# -*- coding: utf8 -*-

from phystricks import *
import sys

# The reason why we put each picture in a separate file is that we want to include the code in the documentation
# using \VerbatimInput. Thus we are sure that the code in the documentation is always corresponding to the picture.
from MarkOnPoint import MarkOnPoint
from Lines import Lines
from Sequence import Sequence
from exCircle import exCircle
from exCircleTwo import exCircleTwo
from exCircleThree import exCircleThree
from Axes import Axes
from AxesSecond import AxesSecond
from VectorOne import VectorOne
from FunctionFirst import FunctionFirst
from FunctionSecond import FunctionSecond
from FunctionThird import FunctionThird
from FunctionFour import FunctionFour
from FunctionFive import FunctionFive
from ParametricOne import ParametricOne
from ParametricTwo import ParametricTwo
from GridOne import GridOne
from GridTwo import GridTwo
from GridThree import GridThree
from GestionRepere import GestionRepere

def MorePoints():
	pspict=pspicture()
	fig = GenericFigure("MorePoints")

	for color in ["red","blue","green"]:
		for i in range(1,10):
			pspict.DrawPoint(Point(),"<+*ou none+>","<+paramètres+>")

	pspict.TraceAxesDefaut()

	pspict.Dilate(1)

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()


def Essais():
	pspict=pspicture("Essais")
	fig = GenericFigure("Essais")

	p = Point(3,4)
	P = Graph(p)
	pspict.DrawGraph(P)

	fig.add_pspicture(pspict)
	fig.conclude()
	fig.write_the_file()

def AllFigures():
	# Don't forget to run the script first_example.py in order to get a full serie of examples.
	GestionRepere()
	GridThree()
	GridTwo()
	GridOne()
	ParametricTwo()
	ParametricOne()
	FunctionFive()
	FunctionFour()
	FunctionThird()
	FunctionSecond()
	FunctionFirst()
	AxesSecond()
	Axes()
	VectorOne()
	exCircleThree()
	exCircleTwo()
	exCircle()
	Lines()
	Sequence()
	MarkOnPoint()

# This is used in order to perform automatic tests.
if len(sys.argv)>1 :
	if sys.argv[1] == "--all":
		AllFigures()
else :
	FunctionFive()
