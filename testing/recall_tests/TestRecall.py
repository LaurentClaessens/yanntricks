#! /usr/bin/python3
# -*- coding: utf8 -*-


# This script compares the files "*.pstricks" with the corresponding one 
# "*.pstricks.recall" and prints a warning if they are not equal.

# The directory passed as argument is the main directory of the
# mazhe project.
#
# So, relative to the passed argument 
# - '.pstricks' files to be checked are in `auto/pictures_tex`
# - '.recall' files to be checked against are in `src_phystricks`

import os

def pstricks_files_iterator(directory):
    for f in os.listdir(directory):
        if f.endswith(".pstricks"):
            yield os.path.join(directory,f)

def wrong_file_list(pstricks_directory,recall_directory):
    """
    return a tuple of lists
    - the list of missing 'recall'
    - the list of 'recall/pstricks' which do not match

    parameters :
    - `pstricks_directory` : the directory in which the 'pstricks' files are.
                        This is also the directory that we are going to parse.

    - `recall_directory` : the directory in which are the recall files.
    """
    wfl=[]  # wrong file list
    mfl=[]  # missing file list
    for filename in pstricks_files_iterator(pstricks_directory):
        with open(filename,'r') as f:
            get_text=f.read()
        try :
            recall_filename=os.path.join(recall_directory,
                                os.path.split(filename)[1]+".recall")
            with open(recall_filename,'r') as f:
                recall_text=f.read()
        except FileNotFoundError as err :
            mfl.append(filename)
            recall_text=get_text    # we do not append it to the wfl list.

        if get_text != recall_text :
            wfl.append(filename)
    return mfl,wfl

class Point(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def is_almost_equal(self,other,epsilon):
        if abs(self.x-other.x)>epsilon:
            return False
        if abs(self.y-other.y)>epsilon:
            return False
        return True
    def __eq__(self,other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True
    def __str__(self):
        return "({},{})".format(self.x,self.y)

class FileDecomposition(object):
    """
    Represent a 'pstricks' file decomposed as a list of points and
    text between points.

    Hypothesises 
    - Points coordinates are of the form
        (x,y)
    - The other open parenthesis are in the combination \(
    """
    def __init__(self,filename):
        import re
        self.filename=filename
        self.points_list=[]
        self.texts_list=[]

        content=open(filename,'r').read()

        reg=re.compile("[^\\\]\(")
        bl=reg.split(content)

        self.texts_list.append(bl[0])
        for block in bl[1:] :
            closing=block.find(")")
            point=block[0:closing]
            text=block[closing:]

            x=None
            y=None
            try :
                x=float(point.split(",")[0])
                y=float(point.split(",")[1])
            except :
                # Hapens for this kind of lines :
#\setlength{\lengthOfforphystricks}{\totalheightof{$f(x)$}}% 
                pass 

            if x is not None :
                self.points_list.append(Point(x,y))
                self.texts_list.append(text)

## \brief Print a comparison of files 'f1' and 'f2' which are assumed
# to be auto generated '.pstricks' files.
def comparison(f1,f2,epsilon):
    d1=FileDecomposition(f1)
    d2=FileDecomposition(f2)
    for t in zip(d1.texts_list,d2.texts_list):
        if t[0] != t[1]:
            print("There is a change of text")
    for t in zip(d1.points_list,d2.points_list):
        Dx=t[1].x-t[0].x
        Dy=t[1].y-t[0].y
        if abs(Dx)>epsilon or abs(Dy)>epsilon :
            print("{} Vs {} : Dx={}, Dy={}".format(t[0],t[1],Dx,Dy))

def check_pictures(pstricks_directory,recall_directory):
    mfl,wfl=wrong_file_list(pstricks_directory,recall_directory)

    for f in mfl:
        print("Missing recall file for ",f)
    for f in wfl:
        print("Wrong : ")
        g=f.replace(pstricks_directory,recall_directory)+".recall"
        comparison(f,g,epsilon=0.001)
