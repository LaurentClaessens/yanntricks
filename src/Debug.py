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

# copyright (c) Laurent Claessens, 2010-2016
# email: laurent@claessens-donadello.eu

"""
A set af small debug utilities.
"""

from NoMathUtilities import ensure_str
from Exceptions import PhystricksGenericException

class DebugException(PhystricksGenericException):
    """
    Exception raised for debuging purpose
    """
    def __init__(self,text):
        self.text=text
    def __str__(self):
        return self.text

def testtype(s):
    print(s,type(s))
    print("\n")

def dprint(*args):
    """
    This function is for debug purpose. It serves to roughly print stuff
    on the screen. Then "grep dprint" helps to remove all the garbage.
    """
    a=[ensure_str(x) for x in list(args)]
    print(" ".join(a))


