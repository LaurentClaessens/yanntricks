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

import sys
import os
from  RecallTestsExceptions import TikzDecompositionParsingException

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
    def __repr__(self):
        return "({},{})".format(self.x,self.y)

## \brief split `text` on basis of the given index
#
# \param text a string to be spliced
# \positions a list of integers.
#
# Iterate over strings that are the parts of `text` between the
# given positions.
# Two border cases :
# - the part before the first given index
# - the part after the last one.y 
# They are part of the iterator.
def split_for_positions(text,positions):
    if positions[0]==0:
        yield ''
        positions=positions[1:]
    yield text[0:positions[0]]
    for i in range(len(positions)-1) :
        yield text[positions[i]+1:positions[i+1]]
    yield text[positions[-1]+1:]

##    Represent a 'pstricks' file decomposed as a list of points and
#    text between points.
#
#    Hypothesises 
#    - Points coordinates are of the form (x,y)
#    - The other open parenthesis are in the combination \(
class TikzDecomposition(object):
    def __init__(self,text):
        import re
        self.points_list=[]
        self.texts_list=[]

        # One cannot iter over reg.split(text) because in
        # bla (a,b)(c,d)
        # the second match  is ")(", so that the first block in the split
        # will be "a,b" without the closing parenthesis.
        # This also explains the "+1" in the definition of 'parenthesis'
        reg=re.compile("[^\\\]\(")
        parenthesis=[m.start()+1 for m in re.finditer(reg,text)]

        bl=list(split_for_positions(text,parenthesis))
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
                # Happens for this kind of lines :
                # \setlength{\foo}{\totalheightof{$f(x)$}}% (1,1)
                pass 

            if x is not None and y is not None :
                self.points_list.append(Point(x,y))
                self.texts_list.append(text)
            else :
                self.texts_list.append(block)

def file_to_tikz_decomposition(filename):
    content=open(filename,'r').read()
    return TikzDecomposition(content)

## \brief contains the comparison between two 'tikz' files
#
# \param f1,f2 filenames which have been compared
# \param kind (string) the kind of encountered problem.
#   for example)
# \param  comment (string) the problem which was found
#
# The possibilities for `kind` are :
# - "wrong texts list size"
# - "wrong points list size"
# - "text change"
# - "large point move"
# - "small point move"
# - "none"
class TikzComparison(object):
    def __init__(self,f1,f2,kind,comment=None):
        self.f1=f1
        self.f2=f2
        self.kind=kind
        self.comment=comment
    def __str__(self):
        a=[]
        a.append(self.kind)
        a.append(self.f1+" "+self.f2)
        a.append(self.comment)
        return "\n".join(a)
        

## \brief return a comparison of files 'f1' and 'f2' which are assumed
# to be auto generated '.pstricks' files.
#
# \param f1,f2  file names.
#
# \return (`TikzComparison`) a small summary of the comparison.
def comparison(f1,f2,epsilon,verbose=False):
    try :
        d1=file_to_tikz_decomposition(f1)
        d2=file_to_tikz_decomposition(f2)
    except TikzDecompositionParsingException as e :
        raise TikzDecompositionParsingException(e.block,f1,f2,x=e.x,y=e.y)
    if len(d1.texts_list) != len(d2.texts_list) :
        return TikzComparison(f1,f2,kind="Wrong texts list size",comment="")
    if len(d1.points_list) != len(d2.points_list) :
        return TikzComparison(f1,f2,kind="Wrong points list size",comment="")
    for t in zip(d1.texts_list,d2.texts_list):
        if t[0] != t[1]:
            return TikzComparison(f1,f2,"text change","{} Vs {} ".format(t[0],t[1]))
    for t in zip(d1.points_list,d2.points_list):
        try :
            Dx=t[1].x-t[0].x
            Dy=t[1].y-t[0].y
        except TypeError :
            print("Type error for ",t[1].x,t[0].x,t[1].y,t[0].y)
            print("In the files : ")
            print(f1)
            print(f2)
            raise
        if abs(Dx)>epsilon or abs(Dy)>epsilon :
            return TikzComparison(f1,f2,"large point move","{} Vs {} : Dx={}, Dy={}".format(t[0],t[1],Dx,Dy))
    for t in zip(d1.points_list,d2.points_list):
        Dx=t[1].x-t[0].x
        Dy=t[1].y-t[0].y
        if abs(Dx)>0 or abs(Dy)>0 :
            return TikzComparison(f1,f2,"small point move",comment="{} Vs {} : Dx={}, Dy={}".format(t[0],t[1],Dx,Dy))

    return TikzComparison(f1,f2,kind='none',comment="")

## \brief check the pictures against their 'recall' file in a directory.
#
# \param pstricks_directory the directory which will be parsed in search
# for '.pstricks' files.
# \param recall_directory the directory in which the corresponding 'recall' files
# will be searched.
# \param verbose if `True`, print the name of all the files whose corresponding 
# 'recall' is not exactly the same.
# If `False`, print only the ones for which a point is significantly moved or 
# a text outside points coordinates is changed.
# \param epsilon is the tolerance for point move. When the coordinates of a point
# did not change by more than `epsilon`, the files are considered as "small point
# move".
def check_pictures(pstricks_directory,recall_directory,verbose=True,epsilon=0.001):
    mfl,wfl=wrong_file_list(pstricks_directory,recall_directory)

    comparison_list=[]

    for f in mfl:
        print("Missing recall file for ",f)
    for f in wfl:
        g=f.replace(pstricks_directory,recall_directory)+".recall"
        comparison_list.append(comparison(f,g,epsilon=epsilon,verbose=verbose))

    kinds=["wrong texts list size", 
            "wrong points list size", 
            "text change", 
            "large point move", 
            "small point move",
            "none"]

    for k in kinds :
        print("========= ",k," ============")
        for comp in [c for c in comparison_list if c.comment==k]:
            print(comp)
