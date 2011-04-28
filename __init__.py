# -*- coding: utf8 -*-

###########################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2009-2011
# email: moky.math@gmail.com

"""
A collection of tools for building LaTeX-pstricks figures with python.

COMMAND LINE ARGUMENTS:

    - ``--pdf`` - the picture arrives as an \includegraphics of a pdf. It also creates the `pdf` file.

    - ``--eps`` - the picture arrives as an \includegraphics of a eps. It also creates the `eps` file.

    - ``--png`` - the picture arrives as an \includegraphics of a png. It also creates the `png` file.

    - ``--create-png`` - create the png file, but does not change the `.pstricks`
                         file. Thus the LaTeX output will not be modified.
                         
                         See :class:`TestPspictLaTeXCode` and the function :func:`create_png_file`
                         in :class:`PspictureToOtherOutputs`

    NOTES:

        - Here we are really speaking about pspicture. There will be one file of one 
          \includegraphics for each pspicture. This is not figure-wise.

        - Using `--pdf`, `--create-png`, etc. create the picture from an auxiliary
          LaTeX file that will we compiled and converted on the fly. As a consequence,
          customizations (e.g. fonts) will not be taken into account. 
          See `pspict.specific_needs`

    - ``--create_tests`` - create a `tmp` file in which the pspicture is written.

    - ``--tests`` - compares the produced pspicture with the corresponding `tmp` file and
                    raises a ValueError if it does not correspond.
                    If this option is set, nothing is written on the disk.

                    See :class:`TestPspictLaTeXCode`
"""

#from __future__ import division
from sage.all import *
import codecs
import math, sys, os

from phystricks.main import *
from phystricks.BasicGeometricObjects import *
from phystricks.SmallComputations import *
