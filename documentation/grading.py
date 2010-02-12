#! /usr/bin/sage -python
# -*- coding: utf8 -*-

import phystricks.StudentGrading
from sage.all import *

maxi = 10
students = [	0,3,5,5,0,0,10,3,10,6,4,1,2,9,1,10,
		0,9,0,5,0,2,2,7,2,0,1,2,4,1,0,5,10,
		1,5,3,10,1,7,0,4,5,2,3,10,5,5,10,
		7,5,3,0,5,1,9,2,2,8,2,6,3,1,7,1,2,
		5,4,5,3,4,5,0,0,8,1,1,5,5,2,2,5,0]

grading = phystricks.StudentGrading.Grades(students,maxi)
grading.y_is_percent_bigger_than_x("GradingStatistics",maxi)

