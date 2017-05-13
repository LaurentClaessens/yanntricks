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
# This file contains the exceptions that can be raised by 'phystricks'.
# 
# These exceptions should subcalss `PhystricksGenericException` because 
#I have in mind to catch them all when performing a test suite.


class PhystricksGenericException(Exception):
    def __str__(self):
        print("Well. Really you should subclass and overrive this")
        raise

class MissingPictureException(PhystricksGenericException):
    """
    Exception raised when a function needs a non furnished picture argument.
    """
    def __init__(self,text):
        self.text=text
    def __str__(self):
        return self.text

class NotObjectGraphException(PhystricksGenericException):
    ## raised when one tries to draw an object which does not subclass
    #  `ObjectGraph`
    def __init__(self,ob):
        self.ob=ob
    def __str__(self):
        return "You cannot draw this object of type {} because this is not 'ObjectGraph'".format(type(self.ob))

class ShouldNotHappenException(PhystricksGenericException):
    """
    Exception raised when something should not happen (bad use of a method)
    """
    def __init__(self,text):
        self.text=text
    def __str__(self):
        return self.text

class AlreadyEnlargedException(PhystricksGenericException):
    """
    Exception raised when the bounding box is already enlarged and when
    one tries to enlarge it again.
    """
    def __init__(self,text):
        self.text=text
    def __str__(self):
        return self.text

class PhystricksTestError(PhystricksGenericException):
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
            print("Warning : this error is provided without pspict. Maybe something is wrong.")
    def __str__(self):
        a=[]
        a.append("Test failed")
        a.append(self.justification)
        return "\n".join(a)

class PhystricksNoError(PhystricksGenericException):
    def __init__(self,figure):
        self.figure=figure

class NoMathBoundingBox(PhystricksGenericException):
    def __init__(self,obj,fun):
        self.message = "Object {0} from class {1} has no attribute {2}".format(obj,type(obj),fun)

class TooLargeBBException(PhystricksGenericException):
    def __init__(self,obj,faulty,acceptable,got):
        """
        Describe the exception raised when a too large bounding box is found.
        - `obj` : the object that has a too large bounding box
        - `faulty` : "xmin", "xmax", "ymin" or "ymax" : the coordinate that
            that was too large.
        - `acceptable` : the maximal value that the picture 
             was accepting for that coordinate.
        - `got` : the computed/found size.
        """
        self.obj=obj
        self.faulty=faulty
        self.acceptable=acceptable
        self.got=got
    def __str__(self):
        a=[]
        a.append("Problem with the bounding box of "+str(self.obj))
        try :
            a.append("The mother of {0} is {1}".format(self.obj,self.obj.mother))
        except AttributeError :
            pass
        a.append("The bound "+self.faulty+" is "+str(self.got)+" while the maximal accepted value is "+str(self.acceptable))
        a.append("""The easiest way to debug this is to make the picture compile adding something like 
                        pspict.Mx_acceptable_BB=1000
                        pspict.mx_acceptable_BB=-1000
                        pspict.My_acceptable_BB=1000
                        pspict.my_acceptable_BB=-1000
        and then see de visu what is the faulty object.
                    """)
        return "\n".join(a)

class ImaginaryPartException(PhystricksGenericException):
    def __init__(self,text):
        self.message=text
