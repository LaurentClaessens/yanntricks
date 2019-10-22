##########################################################################
#   This is part of the module yanntricks
#
#   yanntricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   yanntricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with yanntricks.py.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

# copyright (c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu

"""
This file contains the utilities that do not depend on sage or other
parts of yanntricks.

So you can safely import from here.
"""

import codecs
import hashlib

from yanntricks.src.Defaults import LOGGING_FILENAME

dprint = print


def text_to_hexdigest(text):
    """
    Return the sha1 hexdigest of a text.

    The point of this function is to take care about the fact
    that the hashlib wants 'str', not 'unicode'
    """
    h = hashlib.new("sha1")
    h.update(str(text).encode('utf8'))
    return h.hexdigest()


def first_bracket(text):
    """
    return the first bracket in the string 'text'  
    """
    if "[" not in text:
        return ""
    a = text.find("[")
    b = text[a:].find("]")+1+a
    bracket = text[a:b]
    return bracket


def logging(text, pspict=None):
    if pspict:
        text = "in "+pspict.name+" : "+text
    print(text)
    with codecs.open(LOGGING_FILENAME, "a", encoding="utf8") as f:
        f.write(text+"\n")
