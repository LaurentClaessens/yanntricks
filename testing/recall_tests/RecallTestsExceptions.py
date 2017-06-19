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

# copyright (c) Laurent Claessens, 2016-2017
# email: laurent@claessens-donadello.eu

##
# This file contains the exceptions that can be raised by the tests.



## \brief An error occurred when parsing a file for creating a 
# `TikzDecomposition` object.
#
# Stupidly search for "("  and the corresponding closing ")" and then interpreting
# what lies in between is not sufficient as the following examples 
# (among many others) shows:
# ```
# \subfigure[more points (5000)]{%
# ```

class TikzDecompositionParsingException(Exception):
    def __init__(self,block,f1=None,f2=None,x=None,y=None):
        self.block=block
        self.f1=f1
        self.f2=f2
        self.x=x
        self.y=y
    def __str__(self):
        a=[]
        a.append("An error occurred in the block")
        a.append(self.block)
        a.append("In file")
        a.append(self.f1)
        a.append(self.f2)
        a.append("x={}, y={}".format(self.x,self.y))
        return "\n".join(a)
