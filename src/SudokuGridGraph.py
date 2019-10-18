###########################################################################
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
###########################################################################

# copyright (c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu

from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.Constructors import *

def sudoku_substitution(tableau,symbol_list=[  str(k) for k in range(-4,5) ]):
    """
    From a string representing a sudoku grid,
    1. remove empty lines
    2. remove spaces
    3. substitute 1..9 to the symbol_list
    """
    import string
    lines = tableau.split("\n")[1:]
    n_lines=[   l.replace(" ","") for l in lines if len(l)!=0  ]
    nn_lines=[]
    for l in n_lines :
        a=[]
        for c in l.split(","):
            if  c in string.digits:
                a.append(  symbol_list[int(c)-1])
            else :
                a.append(c)
        nn_lines.append(",".join(a))
    n_tableau="\n".join(nn_lines)
    return n_tableau

class SudokuGridGraph(ObjectGraph):
    def __init__(self,question,length=1):
        ObjectGraph.__init__(self,self)
        self.question=sudoku_substitution(question)
        self.length=length       # length of a cell
    def action_on_pspict(self,pspict):
        import string

        vlines=[]
        hlines=[]
        content=[]
        numbering=[]

        # Numbering (1,2,3, ... and A,B,C ...)
        for i in range(0,9):
            A=Point(  (i+1)*self.length-self.length/2,self.length/2  )
            A.parameters.symbol=""
            A.put_mark(0,0,string.uppercase[i],pspict=pspict)
            B=Point(-self.length/2,-i*self.length-self.length/2)
            B.parameters.symbol=""
            B.put_mark(0,0,string.digits[i+1],pspict=pspict)
            numbering.append(A)
            numbering.append(B)

        # Grid
        for i in range(0,10):
            v=Segment(Point(i*self.length,0),Point(i*self.length,-9*self.length))
            h=Segment(Point(0,-i*self.length),Point(9*self.length,-i*self.length))
            # for the subgrid
            if i%3==0 :
                v.parameters.linewidth=2
                h.parameters.linewidth=2
            vlines.append(v)
            hlines.append(h)
        # Content of the cells
        lines = self.question.split("\n")
        for i,li in enumerate(lines):
            for j,c in enumerate(li.split(",")):
                A=Point(j*self.length+self.length/2,-i*self.length-self.length/2)
                A.parameters.symbol=""
                if c=="i":
                    A.put_mark(3*self.length/9,text="\ldots",pspict=pspict,position="N")
                if c in [  str(k) for k in range(-9,10)  ] :
                    A.put_mark(0,0,c,pspict=pspict)
                content.append(A)
        pspict.DrawGraphs(vlines,hlines,content,numbering)
    def _math_bounding_box(self,pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        return BoundingBox()
    def _bounding_box(self,pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        return BoundingBox()
    def latex_code(self,language=None,pspict=None):
        return ""
