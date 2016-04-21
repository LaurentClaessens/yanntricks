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

# copyright (c) Laurent Claessens, 2016
# email: laurent@claessens-donadello.eu

class ShouldNotHappenException(Exception):
    """
    Exception raised when something should not happen (bad use of a method)
    """
    def __init__(self,text):
        self.text=text
    def __str__(self):
        return self.text

class PhystricksTestError(Exception):
    """
    The exception raised when testing the pspictures.

    See :class:`TestPspictLaTeXCode`.
    """
    def __init__(self,expected_text=None,obtained_text=None,justification=None,pspict=None,code=1):
        """
        code is 1 or 2.
        code==1 indicates that the figure has to be visually checked.
        code==2 indicates that the figure has to be recompiled (LaTeX)
        """
        self.expected_text=expected_text
        self.obtained_text=obtained_text
        self.justification=justification
        self.pspict=pspict
        self.code=code
        if pspict==None:
            print "Warning : this error is provided without pspict. Maybe something is wrong."
    def __str__(self):
        a=[]
        a.append("Test failed")
        a.append(self.justification)
        return "\n".join(a)

class PhystricksNoError(Exception):
    def __init__(self,figure):
        self.figure=figure

class NoMathBoundingBox(Exception):
    def __init__(self,obj,fun):
        self.message = "Object {0} from class {1} has no attribute {2}".format(obj,type(obj),fun)

class PhystricksCheckBBError(Exception):
    def __init__(self):
        pass
