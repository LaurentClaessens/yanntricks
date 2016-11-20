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
This file contains the utilities that do not depend on sage or other
parts of phystricks.

So you can safely import from here.
"""

def text_to_hexdigest(text):
    """
    Return the sha1 hexdigest of a text.

    The point of this function is to take care about the fact
    that the hashlib wants 'str', not 'unicode'
    """
    import hashlib
    str_text=ensure_str(text)

    h=hashlib.new("sha1")
    h.update(str_text)            # This one wants 'str', not 'unicode'
    return h.hexdigest()


def ensure_unicode(s):
    """
    Return a 'unicode' object that represents 's'. 
    No conversion if 's' is already unicode.

    str->unicode (via s.decode("utf8"))
    unicode->unicide (identity map)
    """
    if isinstance(s,str):
        return s.decode("utf8")
    if isinstance(s,unicode):
        return s
    testtype(s)
    raise TypeError("You are trying to convert to unicode the following object "+str(s)+" of type "+str(type(s)))

def ensure_str(s):
    """
    Return a 'str' object that represents 's'. 
    No conversion if 's' is already str.

    unicode->str (via s.encode("utf8"))
    str->str (identity map)
    """
    if isinstance(s,str):
        return s
    if isinstance(s,unicode):
        return s.encode("utf8")
    testtype(s)
    raise TypeError("You are trying to convert to unicode the following object "+str(s)+" of type "+str(type(s)))

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

def logging(text,pspict=None):
    from Defaults import LOGGING_FILENAME
    import codecs
    text=ensure_unicode(text)
    if pspict :
        text="in "+pspict.name+" : "+text
    print(text)
    with codecs.open(LOGGING_FILENAME,"a",encoding="utf8") as f:
        f.write(text+"\n")

class SubdirectoryFilenames(object):
    """
    An object of this class represent a file, 
    or more precisely the path to a file.

    If the file "Directories.py" exists, read the directories in which the 
    tex files have to be put.
    In all cases if the file "Directories.py" is not found, everything will
    return the unmodified filename.
    """
    def __init__(self,filename,position="here"):
        """
    - `filename` is a string containing the filenam
        e with no directory indications.
    - `position` can be "here", "main" or "tex" (default "here")

        if "here" : the file is in the current directory
                when the picture is created.
                    That is the current directory with respec to to Sage
        if "main" : the file is in the main latex directory
        if "tex" : the file is un the picture latex directory, that is the
                    directory in which the file ".pstricks" is put.
        if "tikz" : the file is the directiry for md5 and pdf tikz files.
        """
        import os.path
        self.filename=filename
        self.position=position
        if os.path.isfile("Directories.py"):

            # 'importlib' is the solution for python3
            # 'imp' is the solution for python2
            # This class is imported by python3 from the script 'new_picture.py'
            try :
                import importlib.util
                spec = importlib.util.spec_from_file_location("Directories", "Directories.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except ImportError :
                import imp
                module = imp.load_source("Directories","Directories.py")


            self.PICTURES_TEX=module.PICTURES_TEX
            self.PICTURES_SRC=module.PICTURES_SRC
            self.PICTURES_TIKZ=module.PICTURES_TIKZ
            self.MAIN_TEX=module.MAIN_TEX

            if position=="here":
                self.abs_filename=os.path.abspath(filename)
            if position=="main":
                ff=os.path.join(self.MAIN_TEX,filename)
                self.abs_filename=os.path.abspath(ff)
            if position=="pictures_tex":
                ff=os.path.join(self.PICTURES_TEX,filename)
                self.abs_filename=os.path.abspath(ff)
            if position=="pictures_src":
                ff=os.path.join(self.PICTURES_SRC,filename)
                self.abs_filename=os.path.abspath(ff)
            if position=="pictures_tikz":
                ff=os.path.join(self.PICTURES_TIKZ,filename)
                self.abs_filename=os.path.abspath(ff)
        else :
            self.abs_filename=os.path.abspath(filename)
    def from_here(self):
        import os.path
        if not os.path.isfile("Directories.py"):
            return self.filename
        current="."
        tex=os.path.relpath(self.PICTURES_TEX,current)
        ff=os.path.relpath(self.abs_filename,current)
        return ff
    def from_main(self):
        import os.path
        if not os.path.isfile("Directories.py"):
            return self.filename
        current="."

        main=os.path.relpath(self.MAIN_TEX,current)
        tex=os.path.relpath(self.PICTURES_TEX,current)
        vfile=self.abs_filename

        ff=os.path.relpath(self.abs_filename,main)
        return os.path.relpath(vfile,main)
    def abspath(self):
        return self.abs_filename
