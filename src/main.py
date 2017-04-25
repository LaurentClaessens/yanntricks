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

# copyright (c) Laurent Claessens, 2009-2017
# email: laurent@claessens-donadello.eu


from __future__ import division
from __future__ import unicode_literals

from sage.all import *
import sys
import codecs
import math, sys, os

import BasicGeometricObjects
import SmallComputations as SmallComputations

from PointGraph import PointsNameList
from Exceptions import *
from GlobalVariables import global_vars
from phystricks.src.SmallComputations import *


from phystricks.src.WrapperStr import WrapperStr
var=WrapperStr(var)


# TODO : f=phyFunction(x**2+3*x-10), then  g=f/3 does not work.
# TODO : In figureHYeBZVj, the grid begins at negative numbers. Why ? (see smath available on  https://github.com/LaurentClaessens/smath)
# TODO : waving functions behaves badly when X and Y dilatations are different. See figureHYeBZVj

def no_symbol(*arg):
    for l in arg:
        try:
            for P in l:
                no_symbol(P)
        except TypeError:
            l.parameters.symbol=""

def get_equal_lengths_code(s1,s2,n=1,d=0.1,l=0.1,angle=45,pspict=None,pspicts=None):
    from ObjectGraph import AddedObjects
    added1=AddedObjects()
    added2=AddedObjects()
    pspicts=make_psp_list(pspict,pspicts)
    for psp in pspicts :
        c1=s1.get_code(n=n,d=d,l=l,pspict=psp)
        c2=s2.get_code(n=n,d=d,l=l,pspict=psp)
        added1.append(psp,c1)
        added2.append(psp,c2)
    return added1,added2

def put_equal_lengths_code(s1,s2,n=1,d=0.1,l=0.1,angle=45,pspict=None,pspicts=None):
    """
    Add the code for equal length between segments s1 and s2
    """
    pspicts=make_psp_list(pspict,pspicts)
    for psp in pspicts :
        added=get_equal_lengths_code(s1,s2,n,d,l,angle,pspict=psp)
        c1=added[0]
        c2=added[1]
        s1.added_objects.fusion( c1 )
        s2.added_objects.fusion( c2 )

def GenericFigure(nom,script_filename=None):
    """
    This function returns a figure with some default values. 
    It creates coherent label, file name and prints the lines 
    to be appended in the LaTeX file to include the figure.
    """
    if not script_filename:
        script_filename=nom
    caption = "\CaptionFig"+nom     # This is also hard-coded in the function main.figure.LaTeX_lines
    label = "LabelFig"+nom          # The string "LabelFig" is hard-coded in the function main.figure.LaTeX_lines
    filename = "Fig_"+nom+".pstricks"

    from phystricks.src.Figure import Figure
    fig=Figure(caption,label,filename,script_filename)
    fig.figure_mother=fig   # I'm not sure that this line is useful.
    print fig.LaTeX_lines()
    return fig

def SinglePicture(name,script_filename=None):
    """ Return the tuple of pspicture and figure that one needs in 90% of the cases. """
    fig = GenericFigure(name,script_filename)
    pspict=fig.new_pspicture(name)
    fig.child_pspictures.append(pspict)
    return pspict,fig

def MultiplePictures(name,n=None,pspicts=None,script_filename=None):
    r"""
    Return a figure with multiple subfigures. 

    INPUT:

    - `name` - the name of the figure.

    - `n` (optional)  - the number of subfigures.

    -  `pspicts` (optional) : a list of pspictures to be appended.

    You can either give `n` or `pspicts`. In the first case, `n` new pspictures are created;
    in the second case, the given pspictures are attached to the multiple pictures.

    You have to think about naming the subfigures.

    EXAMPLE::

        sage: from phystricks import *
        sage: pspicts,fig = MultiplePictures("MyName",3)
        The result is on figure \ref{LabelFigMyName}.
        \newcommand{\CaptionFigMyName}{<+Type your caption here+>}
        \input{Fig_MyName.pstricks}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName0}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName1}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName2}
        sage: pspicts[0].mother.caption="My first subfigure"
        sage: pspicts[1].mother.caption="My second subfigure"
        sage: pspicts[2].mother.caption="My third subfigure"

    Notice that a caption is related to a figure or a subfigure, not to a pspicture.

    See also :class:`subfigure`
    """
    if not script_filename:
        script_filename=name
    fig = GenericFigure(name,script_filename)


    if n is not None :
        pspictures_list=[]
        for i in range(n):
            subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
            picture=subfigure.new_pspicture(name+"pspict"+str(i))
            picture.figure_mother=fig
            fig.child_pspictures.append(picture)
            pspictures_list.append(picture)

    if pspicts is not None :
        pspictures_list=[]
        n=len(pspicts)
        for i,psp in enumerate(pspicts) :
            subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
            subfigure.new_pspicture(pspict=psp)
            psp.figure_mother=fig
            fig.child_pspictures.append(psp)
            pspictures_list.append(psp)

    return pspictures_list,fig

def IndependentPictures(name,n):
    """
    Return a tuple of a list of 'n' pspictures and 'n' figures.
    """
    pspicts=[]
    figs=[]
    from phystricks.src.Utilities import latinize
    for i in range(0,n):
        # One has to latinize to be in grade of making subfigures :
        # if not one gets things like \newcommand{\CaptionFigFoo1}{blahblah}  which does not work in LaTeX because of the "1"
        pspict,fig = SinglePicture(name+"oo"+latinize(str(i)))
        pspicts.append(pspict)
        figs.append(fig)
    return pspicts,figs

def SubsetFigures(old_pspicts,old_fig,l):
    r"""
    Return a subset of a figure with subfigures.

    If you've prepared a figure with 10 subfigure but at the end of the day,
    you change your mind and decide to remove the subfigure 3 and 8
    
    EXAMPLE::

    
    .. literalinclude:: phystricksSubSetMultiple.py

    .. image:: Picture_FIGLabelFigSubSetMultiplessLabelSubFigSubSetMultiple2PICTSubSetMultiplepspict2-for_eps.png
    .. image:: Picture_FIGLabelFigSubSetMultiplessLabelSubFigSubSetMultiple3PICTSubSetMultiplepspict3-for_eps.png
    .. image:: Picture_FIGLabelFigSubSetMultiplessLabelSubFigSubSetMultiple5PICTSubSetMultiplepspict5-for_eps.png

    I'm not sure that it is still possible to use the old fig.
    """
    name=old_fig.name
    script_filename=old_fig.script_filename
    fig = GenericFigure(name,script_filename)
    pspict=[]
    for i in l:
        subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
        subfigure._add_pspicture(old_pspicts[i])
        old_pspicts[i].figure_mother=fig
        pspict.append(old_pspicts[i])
    return pspict,fig

def unify_point_name(s):
    r"""
    Interpret `s` as the pstricks code of something and return a chain with
    all the points names changed to "Xaaaa", "Xaaab" etc.

    Practically, it changes the strings like "{abcd}" to "{Xaaaa}".

    When "{abcd}" is found, it also replace the occurences of "(abcd)".
    This is because the marks of points are given by example as
    '\\rput(abcd){\\rput(0;0){$-2$}}'

    This serves to build more robust doctests by providing strings in which
    we are sure that the names of the points are the first in the list.

    INPUT:

    - ``s`` - a string

    OUTPUT:
    string

    EXAMPLES:
    
    In the following example, the points name in the segment do not begin
    by "aaaa" because of the definition of P, or even because of other doctests executed before.
    (due to complex implementation, the names of the points are
    more or less unpredictable and can change)

    ::

        sage: from phystricks import *
        sage: P=Point(3,4)
        sage: S = Segment(Point(1,1),Point(2,2))

    However, using the function unify_point_name, the returned string begins with "Xaaaa" ::

    Notice that the presence of "X" is necessary in order to avoid
    conflicts when one of the points original name is one of the new points name as in the following example ::

        sage: s="{xxxx}{aaaa}{yyyy}"
        sage: print unify_point_name(s)
        {Xaaaa}{Xaaab}{Xaaac}

    Without the additional X,

    1. The first "xxxx" would be changed to "aaaa".
    2. When changing "aaaa" into "aaab", the first one would be changed too.

    """
    import re

    point_pattern=re.compile("({[a-zA-Z]{4,4}})")
    match = point_pattern.findall(s)

    rematch=[]
    for m in match:
        n=m[1:-1]       # I transform "{abcd}" into "abcd"
        if n not in rematch:
            rematch.append(n)

    from phystricks.src.PointGraph import PointsNameList
    names=PointGraph.PointsNameList()
    for m in rematch:
        name=names.next()
        s=s.replace("{%s}"%m,"{X%s}"%name).replace("(%s)"%m,"(X%s)"%name)
    return s

class FigureGenerationSuite(object):
    """
    Generate the figures of a list.

    INPUT:

    - ``test_list`` - a list of functions that are supposed to produce pspictures
    
    - ``first`` - the position in `test_list` at which we begin the tests

    If the option `--tests` is given to the script, the attribute `failed_list` contains
    the list of functions that produced the exception :class:`PhystricksTestError`.

    ATTRIBUTES:

    - ``failed_list`` - a list of tuple `(function,pspict)` where `function` is a 
                        function that produced a :class:`PhystricksTestError` and
                        pspict is the produced pspicture.

    """
    def __init__(self,test_list,first=0,title="My beautiful document"):
        from Defaults import LOGGING_FILENAME
        self.test_list=test_list
        self.first=first
        self.title=title
        self.failed_list=[]
        self.documentation_list=[]
        self.to_be_recompiled_list=[]
        open(LOGGING_FILENAME,"w").close()

    def generate(self):
        """
        perform the tests
        """
        Figure.send_noerror = True
        print ""
        print "********************************************"
        print "*  This is the automatic figure generation"
        print "*  for %s"%self.title
        print "********************************************"
        print ""
        for i in range(self.first,len(self.test_list)):
            print "--------------------------- %s : figure %s/%s (failed: %s) -------------------------------------"%(self.title,str(i+1),str(len(self.test_list)),str(len(self.failed_list)))
            print " ============= %s ============="%str(self.test_list[i])
            try:
                try:
                    self.test_list[i]()
                except PhystricksTestError,e:
                    print "The test of pspicture %s failed. %s"%(self.test_list[i],e.justification)
                    print e
                    self.failed_list.append((self.test_list[i],e.pspict))
                    if e.code==2:
                        self.to_be_recompiled_list.append((self.test_list[i],e.pspict))
            except PhystricksNoError,e:
                if global_vars.create_documentation:
                    self.documentation_list.append( (self.test_list[i],e.figure) )
    def latex_portion(self,failed_list,lstinputlisting=False):
        from latex_to_be import pseudo_caption
        portion=[]
        num=0
        for a in failed_list:
            try:
                base=a[1].figure_mother.LaTeX_lines()
            except AttributeError,e:
                try:
                    base=a[1].LaTeX_lines()     # In the case we are arriving here to create the documentation.
                except AttributeError,e:
                    print "I cannot found the LaTeX lines corresponding to ",a[1]
                    print e
            else :
                text=base.replace(pseudo_caption,str(a[0]))
                portion.append(text)
                if lstinputlisting :
                    filename="phystricks"+str(a[1].script_filename)
                    portion.append(r"\lstinputlisting{"+filename+".py}")
                    portion.append("\clearpage")
                num=num+1
                if num==5:
                    portion.append("\clearpage\n")
                    num=0
        return "\n".join(portion)

    def create_to_be_latex_file(self,failed_list,name="checked"):
        """
        This function produce the LaTeX file that serves to continue the tests. 
        This can be either the figures to be visually checked, either the figures that have to be recompiled.
        """
        from latex_to_be import to_be_checked_general_latex
        general_text=to_be_checked_general_latex
        text=general_text.replace("XXXXXX",self.latex_portion(failed_list))
        filename="to_be_{0}.tex".format(name)
        check_file=open(filename,"w")
        check_file.write(text)
        check_file.close()
        print "The file {0} is created for you".format(filename)

    def create_documentation(self):
        """
        This function produce the LaTeX file that serves for documentation. That contains the source code of all pictures together with the result.
        """
        from latex_to_be import documentation_skel
        general_text=documentation_skel
        text=general_text.replace("EXAMPLES_LIST",self.latex_portion(self.documentation_list,lstinputlisting=True))
        filename="documentation.tex"
        check_file=open(filename,"w")
        check_file.write(text)
        check_file.close()
        print "The file {0} is created for you".format(filename)

    def function_list_to_figures_list(self,function_list):
        first=",".join([a[0].__name__ for a in function_list])
        return "figures_list=[{0}]".format(first.replace("'"," "))
    def summary(self):
        """
        Print the list of failed tests and try to give the 
        lines to be included in the LaTeX file in order to
        visualize them.
        """
        if global_vars.create_documentation:
            self.create_documentation()
        all_tests_passed = True
        if len(self.failed_list) != 0:
            print "The list of function to visually checked :"
            print self.function_list_to_figures_list(self.failed_list)
            self.create_to_be_latex_file(self.failed_list)
            all_tests_passed = False
        if len(self.to_be_recompiled_list) != 0:
            print "The list of function to recompiled :"
            print self.function_list_to_figures_list(self.to_be_recompiled_list)
            self.create_to_be_latex_file(self.to_be_recompiled_list,name="recompiled")
            all_tests_passed = False
        if all_tests_passed :
            print "All tests passes !"
            from Defaults import LOGGING_FILENAME
            with open(LOGGING_FILENAME,"r") as f:
                for l in f:
                    print(l)
        else:
            raise PhystricksTestError

class TestPspictLaTeXCode(object):
    def __init__(self,pspict):
        self.pspict=pspict
        self.name=pspict.name
        self.notice_text="This is a testing file containing the LaTeX code of the figure %s."%(self.name)
        self.test_file=SmallComputations.Fichier("test_pspict_LaTeX_%s.tmp"%(self.pspict.name))
    def create_test_file(self):
        """
        Write the LaTeX code of `pspict` in a file.

        The purpose is to compare that file with the code actually
        produced later. This is a way to test changes in phystricks.

        INPUT:

        - ``pspict`` - a pspicture

        If the option `--create-tests` is passed to the program, this function is called
        on each pspicture when concluding a :class:`figure`.
        """
        text=unify_point_name(self.notice_text+self.pspict.contenu_pstricks)
        self.test_file.write(text,"w")
    def test_if_test_file_is_present(self):
        return os.path.isfile(self.test_file.filename)
    def test(self):
        print "---"
        print "Testing pspicture %s ..."%self.name
        obtained_text=unify_point_name(self.pspict.contenu_pstricks)
        if not self.test_if_test_file_is_present():
            print "Seems to lack of test file."
            raise PhystricksTestError("No tests file found.",obtained_text,"No test file found; I do not know what to do.",pspict=self.pspict)
        expected_text=unify_point_name("".join(self.test_file.contenu()).replace(self.notice_text,""))
        boo,justification = string_number_comparison(obtained_text,expected_text)
        if not boo:
            raise PhystricksTestError(expected_text,obtained_text,justification,self.pspict)
        print justification
        print "Successful test for pspicture %s"%self.name
        print "---"
import Separator
import Figure

class PspictureToOtherOutputs(object):
    """
    Contains the informations about the transformation of a pspicture into an eps/pdf file
    The method to produce the eps file is taken from the documentation of the package pst-eps, and from some fruitful discussions on fctt
        http://archive.cs.uu.nl/mirror/CTAN/graphics/pstricks/contrib/pst-eps/pst-eps-doc.pdf
        http://groups.google.fr/group/fr.comp.text.tex/browse_thread/thread/a5c4a67c457c46b8?hl=fr#

    self.file_for_eps is the file in which we will put the LaTeX code needed to create the eps file
    self.input_code_eps
    self.input_code_pdf is the code to be input in the file that contains the picture. This is what replaces the pstricks code in the final figure.
    """
    def __init__(self,pspict):
        self.pspict = pspict
        self.name = self.pspict.name
        self.file_for_eps = SmallComputations.Fichier("Picture_%s-for_eps.tex"%(self.name))
        self.file_dvi = SmallComputations.Fichier(self.file_for_eps.chemin.replace(".tex",".dvi"))
        self.file_bbb_eps = SmallComputations.Fichier(self.file_dvi.chemin.replace(".dvi","_bbb.eps"))       # Bad bounding box
        self.file_eps = SmallComputations.Fichier(self.file_bbb_eps.chemin.replace("_bbb.eps",".eps"))
        self.file_pdf = SmallComputations.Fichier(self.file_eps.chemin.replace(".eps",".pdf"))
        self.file_png = SmallComputations.Fichier(self.file_eps.chemin.replace(".eps",".png"))
        self.input_code_eps = "\includegraphics{{{}}}%".format(self.file_eps.nom)
        self.input_code_pdf = "\includegraphics{{{}}}%".format(self.file_pdf.nom)
        self.input_code_png = "\includegraphics[width=WIDTH]{{{}}}%".format(self.file_png.nom)   # 'WIDHT' will be replaced by the actual boundig box later.
    def latex_code_for_eps(self):
        text = """\documentclass{article}
        \\usepackage{pstricks,pst-eucl,pstricks-add,pst-plot,pst-eps,calc,catchfile}
        \pagestyle{empty}
        \\usepackage[utf8]{inputenc}
        \\usepackage[T1]{fontenc}
        """     # For some reasons with unicode_literals, not even the raw string can contain \u
        code=text.split("\n")
        # Allows to add some lines, like packages or macro definitions required. This is useful when one adds formulas in the picture
        # that need packages of personal commands.
        # If the figure has specific_needs, that ones are used.
        if self.pspict.figure_mother.specific_needs :
            code.append(self.pspict.mother.specific_needs)
        else:
            code.append(self.pspict.specific_needs)
        code.append(self.pspict.write_and_label_separator_list["WRITE_AND_LABEL"].code())
        code.append(self.pspict.write_and_label_separator_list["CLOSE_WRITE_AND_LABEL"].code())
        code.extend(["\\begin{document}\n","\\begin{TeXtoEPS}"])
        code.append(self.pspict.contenu_pstricks)
        code.append("\end{TeXtoEPS}\n")

        code.append("\end{document}\n")
        return "".join(code)
    def create_test_file(self):
        TestPspictLaTeXCode(self.pspict).create_test_file()
    def create_eps_file(self):
        """ Create an eps file by the chain latex/dvips """
        file_tex = self.file_for_eps
        file_tex.write(self.latex_code_for_eps(),"w")
        commande_e = "latex %s"%self.file_for_eps.chemin
        print("External :",commande_e)
        os.system(commande_e)
        commande_e = "dvips -E %s -o %s -q"%(self.file_dvi.chemin,self.file_bbb_eps.chemin)
        print("External :",commande_e)
        os.system(commande_e)

        if Point(0,0) not in self.pspict.bounding_box():
            commande_e="sage-native-execute epstool --bbox --copy --output {} {}".format(self.file_eps.chemin,self.file_bbb_eps.chemin)
            print "**** External :",commande_e
            os.system(commande_e)
        else :
            commande_e="cp {} {}".format(self.file_bbb_eps.chemin,self.file_eps.chemin)
            print "**** External :",commande_e
            os.system(commande_e)
    def create_png_file(self):
        """
        Creates a png file by the chain latex->eps->png

        The last step is done by convert.

        NOTE :

        It is also possible to use inkscape in order to produce svg but
        on my computer inkscape crashes on a segmentation fault
        when launched from a script :(
        """
        # TODO: check if inkscape is present. If not use convert.
        self.create_eps_file()
        #x_cmsize=100*numerical_approx(self.pspict.xsize*self.pspict.xunit)
        #y_cmsize=100*numerical_approx(self.pspict.ysize*self.pspict.yunit)
        x_cmsize=100*self.pspict.visual_xsize()
        y_cmsize=100*self.pspict.visual_ysize()
        commande_e = "sage-native-execute convert -density 1000 %s -resize %sx%s %s"%(self.file_eps.chemin,str(x_cmsize),str(y_cmsize),self.file_png.chemin)
        #commande_e = "inkscape -f %s -e %s -D -d 600"%(self.file_pdf.chemin,self.file_png.chemin)
        #inkscape -f test.pdf -l test.svg
        print "*** External :", commande_e
        os.system(commande_e)
    def create_pdf_file(self):
        """ Creates a pdf file by the chain latex/dvips/epstopdf """
        self.create_eps_file()
        commande_e = "epstopdf %s --outfile=%s"%(self.file_eps.chemin,self.file_pdf.chemin)
        print commande_e
        os.system(commande_e)

import Picture
