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


from __future__ import division
from __future__ import unicode_literals

from sage.all import *
import codecs, sys

import BasicGeometricObjects
import SmallComputations as SmallComputations

from phystricks import WrapperStr
var=WrapperStr(var)

from phystricks import *

class PhystricksTestError(Exception):
    """
    The exception raised when testing the pspictures.

    See :class:`TestPspictLaTeXCode`.
    """
    def __init__(self,expected_text=None,obtained_text=None,justification=None,pspict=None):
        self.expected_text=expected_text
        self.obtained_text=obtained_text
        self.justification=justification
        self.pspict=pspict
    def __str__(self):
        a=[]
        a.append("Test failed")
        #a.append("Expected:")
        #a.append(self.expected_text)
        #a.append("----")
        #a.append("Got:")
        #a.append(self.obtained_text)
        #a.append("---")
        a.append(self.justification)
        return "\n".join(a)

class NoMathBoundingBox(Exception):
    def __init__(self,obj,fun):
        self.message = "Object {0} from class {1} has no attribute {2}".format(obj,type(obj),fun)

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
        self.test_list=test_list
        self.first=first
        self.title=title
        self.failed_list=[]

    def generate(self):
        """
        perform the tests
        """

        print ""
        print "********************************************"
        print "*  This is the automatic figure generation"
        print "*  for %s"%self.title
        print "********************************************"
        print ""
        for i in range(self.first,len(self.test_list)):
            print "--------------------------- %s : figure %s/%s (failed: %s) -------------------------------------"%(self.title,str(i),str(len(self.test_list)),str(len(self.failed_list)))
            print " ============= %s ============="%str(self.test_list[i])
            try:
                self.test_list[i]()
            except PhystricksTestError,e:
                print "The test of pspicture %s failed. %s"%(self.test_list[i],e.justification)
                print e
                self.failed_list.append((self.test_list[i],e.pspict))

    def latex_portion(self):
        from latex_to_be import pseudo_caption
        portion=[]
        num=0
        for a in self.failed_list:
            try:
                base=a[1].figure_mother.LaTeX_lines()
                text=base.replace(pseudo_caption,str(a[0]))
                portion.append(text)
            except AttributeError:
                print "I cannot found the LaTeX lines corresponding to ",a[1]
            else :
                num=num+1
                if num==5:
                    portion.append("\clearpage\n")
                    num=0
        return "\n".join(portion)

    def create_to_be_checked_latex_file(self):
        from latex_to_be import to_be_checked_general_latex
        general_text=to_be_checked_general_latex
        text=general_text.replace("XXXXXX",self.latex_portion())
        filename="to_be_checked.tex"
        check_file=open(filename,"w")
        print "The file {0} is created for you.".format(filename)
        check_file.write(text)
        check_file.close()

    def summary(self):
        """
        Print the list of failed tests and try to give the 
        lines to be included in the LaTeX file in order to
        visualize them.
        """
        if len(self.failed_list) != 0:
            print "The following test failed :"
            for a in self.failed_list:
                print a,

            print "\nThe lines for inclusion in your LaTeX file are :\n"
            print self.latex_portion()

            print "The list of function to test deeper :"
            first=",".join([a[0].__name__ for a in self.failed_list])
            print "figures_list=[",first.replace("'"," "),"]"

            self.create_to_be_checked_latex_file()

            raise PhystricksTestError
        else:
            print "All tests passes !"

class TestPspictLaTeXCode(object):
    def __init__(self,pspict):
        self.pspict=pspict
        self.name=pspict.name
        self.notice_text="This is a testing file containing the LaTeX code of the figure %s."%(self.name)
        self.test_file=SmallComputations.Fichier("test_pspict_LaTeX_%s.tmp"%(self.name))
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
    def test(self):
        print "---"
        print "Testing pspicture %s ..."%self.name
        obtained_text=unify_point_name(self.pspict.contenu_pstricks)
        try:
            expected_text=unify_point_name("".join(self.test_file.contenu()).replace(self.notice_text,""))
        except IOError :
            print "Seems to lack of test file."
            raise PhystricksTestError("No tests file found.",obtained_text,"No test file found; I do not know what to do.",pspict=self.pspict)
        boo,justification = string_number_comparison(obtained_text,expected_text)
        if not boo:
            #raise PhystricksTestError(expected_text,obtained_text,justification,self.pspict)
            raise PhystricksTestError(expected_text,obtained_text,justification,self.pspict)
        print justification
        print "Successful test for pspicture %s"%self.name
        print "---"

sysargvzero = sys.argv[0][:]
def counterName():
    r"""
    This function provides the name of the counter.
    
    This has the same use of newwriteName, for the same reason of limitation.
    """
    return "counterOf"+latinize(sysargvzero)
def newlengthName():
    r"""
    This function provides the name of the length.
    
    This has the same use of newwriteName, for the same reason of limitation.
    """
    return "lengthOf"+latinize(sysargvzero)


class figure(object):
    def __init__(self,caption,name,nFich):
        self.caption = caption
        self.name = name
        self.xunit = 1
        self.yunit = 1
        self.code = []
        self.record_subfigure = []
        self.record_pspicture=[]

        self.nFich=nFich
        self.fichier = SmallComputations.Fichier(self.nFich)

        # The order of declaration is important, because it is recorded in the Separator.number attribute.
        self.separator_list=SeparatorList()
        self.separator_list.new_separator("ENTETE FIGURE")
        self.separator_list.new_separator("WRITE_AND_LABEL")
        self.separator_list.new_separator("BEFORE SUBFIGURES")
        self.separator_list.new_separator("SUBFIGURES")
        self.separator_list.new_separator("AFTER SUBFIGURES")
        self.separator_list.new_separator("DEFAULT")
        self.separator_list.new_separator("BEFORE PSPICTURE")
        self.separator_list.new_separator("PSPICTURE")
        self.separator_list.new_separator("AFTER PSPICTURE")
        self.separator_list.new_separator("AFTER ALL")
        add_latex_line_entete(self)

        self.add_latex_line("\\begin{figure}[ht]","BEFORE SUBFIGURES")
        self.add_latex_line("\centering","BEFORE SUBFIGURES")
    def new_separator(self,title):
        raise DeprecationWarning
        self.separator_number = self.separator_number + 1
        self.separator_dico[title]=Separator(title,self.separator_number)
    def dilatation_X(self,fact):
        """ Makes a dilatation of the whole picture in the X direction. A contraction if the coefficient is lower than 1 """
        self.xunit = self.xunit * fact
    def dilatation_Y(self,fact):
        self.yunit = self.yunit * fact
    def dilatation(self,fact):
        """ dilatations or contract that picture in both directions with the same coefficient """
        self.dilatation_X(fact)
        self.dilatation_Y(fact)
    def new_subfigure(self,caption,name=None):
        """
        Create a subfigure in the figure and return it.

        The end-user should use this instead of append_subfigure
        """
        if name==None:
            number=len(self.record_subfigure)
            name="sub"+latinize(str(number))
        ssfig=subfigure(caption,self.name+"ss"+name)
        ssfig.mother=self
        ssfig.figure_mother=self
        self._append_subfigure(ssfig)
        return ssfig
    def _append_subfigure(self,ssFig):      # This function was initially named AjouteSSfigure
        self.record_subfigure.append(ssFig)
        suffixe = "ssFig"+str(len(self.record_subfigure))
        if not ssFig.name:
            ssFig.name=self.name+suffixe
        #ssFig.pspicture.name=self.name+"pspict"+suffixe    (no more useful 15 oct 2010)
        print r"See also the subfigure \ref{%s}"%ssFig.name
    def new_pspicture(self,name=None,pspict=None):
        if name==None:
            number=len(self.record_pspicture)
            name="sub"+latinize(str(number))
        if pspict==None:
            pspict=pspicture("FIG"+self.name+"PICT"+name)
        self._add_pspicture(pspict)
        return pspict
    def _add_pspicture(self,pspict):
        pspict.mother=self
        pspict.figure_mother=self
        self.record_pspicture.append(pspict)
    def add_pspicture(self,pspict):
        raise DeprecationWarning,"Use fig.new_pspicture instead."
    def append_subfigure(self,pspict):
        raise DeprecationWarning,"Use fig.new_subfigure instead."
    def add_latex_line(self,ligne,separator_name="DEFAULT"):
        self.separator_list[separator_name].add_latex_line(ligne)
    def IncrusteLigne(self,ligne,n):
        raise DeprecationWarning, "The method picture.IncrusteLigne() is depreciated."
        self.code[n:n]=ligne+"\n"
    def AjouteCode(self,liste_code):
        self.code.extend(liste_code)
    def LaTeX_lines(self):
        """
        return the lines to be included in your LaTeX file.
        """
        a=[]
        from latex_to_be import pseudo_caption
        a.append("The result is on figure \\ref{"+self.name+"}.")
        a.append("\\newcommand{"+self.caption+"}{"+pseudo_caption+"}")
        a.append("\\input{%s}"%(self.nFich))
        
        return "\n".join(a)
    def conclude(self):
        for pspict in self.record_pspicture :
            # Here we add the picture itself. What arrives depends on --eps, --pdf, --png, ...
            self.add_latex_line(pspict.contenu(),"PSPICTURE")

            # What has to be written in the WRITE_AND_LABEL part of the picture is written now
            # This has to be done _after_ having called pspict.contenu().
            self.add_latex_line(pspict.write_and_label_separator_list["WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")
            self.add_latex_line(pspict.write_and_label_separator_list["CLOSE_WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")

            if global_vars.perform_tests:
                TestPspictLaTeXCode(pspict).test()
        if not global_vars.special_exit() :
            self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+"}","BEFORE SUBFIGURES")
        for f in self.record_subfigure :
            self.add_latex_line("\subfigure["+f.caption+"]{%","SUBFIGURES")
            self.add_latex_line(f.subfigure_code(),"SUBFIGURES")
            self.add_latex_line("\label{%s}"%f.name,"SUBFIGURES")
            self.add_latex_line("}                  % Closing subfigure "+str(self.record_subfigure.index(f)+1),"SUBFIGURES")
            self.add_latex_line("%","SUBFIGURES")

            for pspict in f.record_pspicture:
                self.add_latex_line(pspict.write_and_label_separator_list["WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")
                self.add_latex_line(pspict.write_and_label_separator_list["CLOSE_WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")
        after_all=r"""\caption{%s}\label{%s}
            \end{figure}
            """%(self.caption,self.name)
        self.add_latex_line(after_all,"AFTER ALL")
        self.contenu = self.separator_list.code()
    def write_the_file(self):
        """
        Write the figure in the file.

        Does not write if we are testing.
        """
        to_be_written=self.contenu
        if not global_vars.perform_tests :
            self.fichier.open_file("w")
            self.fichier.file.write(to_be_written)
            self.fichier.file.close()
        print "--------------- For your LaTeX file ---------------"
        print self.LaTeX_lines()
        print "---------------------------------------------------"
            
class subfigure(object):
    """
    This is a subfigure.

    If no label are given, a default one will be set when included in the figure.
    
    EXAMPLES

    .. literalinclude:: phystricksSubFigure.py
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigFirstPICTFirstPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigSecondPICTSecondPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigThirdPICTthirdPoint-for_eps.png
    """
    def __init__(self,caption,name=None):
        self.caption = caption
        self.name = name
        self.record_pspicture=[]
        self.mother=None
    def add_latex_line(self,ligne,separator_name):
        self.mother.add_latex_line(ligne,separator_name)
    def new_pspicture(self,name=None):
        if name==None:
            number=len(self.record_pspicture)
            name="sub"+latinize(str(number))
        pspict=pspicture("FIG"+self.name+"PICT"+name)
        pspict.mother=self
        pspict.subfigure_mother=self
        self._add_pspicture(pspict)
        return pspict
    def subfigure_code(self):
        a=[]
        for pspict in self.record_pspicture :
            a.append(pspict.contenu())
        return "\n".join(a)
    def _add_pspicture(self,pspicture):
        self.record_pspicture.append(pspicture)
    def add_pspicture(self,pspicture):
        raise DeprecationWarning,"use subfigure.new_pspicture instead"

class PspictureToOtherOutputs(object):
    """
    contains the informations about the transformation of a pspicture into an eps/pdf file
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
        self.file_eps = SmallComputations.Fichier(self.file_dvi.chemin.replace(".dvi",".eps"))
        self.file_pdf = SmallComputations.Fichier(self.file_eps.chemin.replace(".eps",".pdf"))
        self.file_png = SmallComputations.Fichier(self.file_eps.chemin.replace(".eps",".png"))
        self.input_code_eps = "\includegraphics{%s}"%(self.file_eps.nom)
        self.input_code_pdf = "\includegraphics{%s}"%(self.file_pdf.nom)
        self.input_code_png = "\includegraphics{%s}"%(self.file_png.nom)
    def latex_code_for_eps(self):
        text = """\documentclass{article}
        \\usepackage{pstricks,pst-eucl,pstricks-add,pst-plot,pst-eps,calc,catchfile}
        \pagestyle{empty}
        """     # For some reasons with unicode_literals, not even the raw string can contain \u
        code=text.split("\n")
        # Allows to add some lines, like packages or macro definitions required. This is useful when one adds formulas in the picture
        # that need packages of personal commands.
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
        print commande_e
        os.system(commande_e)
        commande_e = "dvips -E %s -o %s -q"%(self.file_dvi.chemin,self.file_eps.chemin)
        print commande_e
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
        # TODO: check if inkscape is present. If not use convert. If convert
        # is not present, prendi la f-parola.
        self.create_eps_file()
        x_cmsize=100*numerical_approx(self.pspict.xsize*self.pspict.xunit)
        y_cmsize=100*numerical_approx(self.pspict.ysize*self.pspict.yunit)
        commande_e = "convert -density 1000 %s -resize %sx%s %s"%(self.file_eps.chemin,str(x_cmsize),str(y_cmsize),self.file_png.chemin)
        #commande_e = "inkscape -f %s -e %s -D -d 600"%(self.file_pdf.chemin,self.file_png.chemin)
        #inkscape -f test.pdf -l test.svg
        print commande_e
        os.system(commande_e)
    def create_pdf_file(self):
        """ Creates a pdf file by the chain latex/dvips/epstopdf """
        self.create_eps_file()
        commande_e = "epstopdf %s --outfile=%s"%(self.file_eps.chemin,self.file_pdf.chemin)
        print commande_e
        os.system(commande_e)

def add_latex_line_entete(truc,position=""):
    if position == "" :
        if isinstance(truc,pspicture):
            position="ENTETE PSPICTURE"
        if isinstance(truc,figure):
            position="ENTETE FIGURE"
    truc.add_latex_line("% This file is automatically generated by phystricks",position)
    truc.add_latex_line("% See the documentation ",position)
    truc.add_latex_line("% http://student.ulb.ac.be/~lclaesse/phystricks-doc.pdf ",position)
    truc.add_latex_line("% http://student.ulb.ac.be/~lclaesse/phystricks-documentation/_build/html/index.html ",position)
    truc.add_latex_line("% and the projects phystricks and phystricks-doc at ",position)
    truc.add_latex_line("% http://gitorious.org/~moky\n",position)

def DicoSeparatorToCode(separator_dico):
    raise DeprecationWarning,"Everything should use SeparatorList"
    """"takes a dictionary of Separator as argument and return the glued code"""
    list_separator = separator_dico.values()
    list_separator.sort()
    a = []
    for sep in list_separator :
        a.append(sep.code())
    return "".join(a)

class SeparatorList(object):
    """
    represent a dictionary of :class:`Separator`
    """
    def __init__(self):
        self.separator_list=[]
    def title_list(self):
        return [x.title for x in self.separator_list]
    def new_separator(self,title,number=None):
        for separator in self.separator_list :
            if separator.title == title :
                raise ValueError, "A new separator cannot have the same title as an old one: %s"%title
        separator=Separator(title)
        if number:
            self.separator_list.insert(number,separator)
        else:
            self.separator_list.append(separator)
    def code(self):
        return "".join(separator.code() for separator in self.separator_list)
    def fusion(self,title_list,new_title):
        """
        Remove of the list the separators whose names are in the `title_list`
        and add a new separator with the fusion code at the place
        where the *first* one was.

        INPUT :

        - ``title_list`` - a list of `str` that are name of separators
                           supposed to be part of `self.separator_list`

        - ``new_title`` - the title of the new separator that will be
                            created.

        Schematically,

        "ONE": "first code"
        "TWO": "second code"
        "THREE": "third code"
        "FOUR": "fourth code"

        If one fusion the second and third with the name "NEW", we get

        "ONE": "first code"
        "NEW" : "second code third code"
        "FOUR": "fourth code"

        NOTE:

        It respect the order. So if the `title_list` comes in the order `["THREE","TWO"]`, it first orders
        the list to `["TWO","THREE"]`

        """

        # One has to remove duplicates. If not the LaTeX code
        # will be written more than once.
        short_list=[]
        for title in title_list:
            if title not in short_list:
                short_list.append(title)

        # On has to sort the list in order the code to appear in
        # the right order. As an example, we want the axes first.
        # The order to be respected is basically the one furnished in
        # __init__ of pspicture and figure.
        short_list.sort(lambda x,y:(self.title_list().index(x)-self.title_list().index(y)))

        new_code=""
        new_place=len(self.separator_list)
        concerned_separators=[]
        for title in short_list:
            separator=self[title]
            concerned_separators.append(separator)
            new_code=new_code+separator.code()
            new_place=min(new_place,self.separator_list.index(separator))

        self.new_separator(new_title,new_place)
        self[new_title].add_latex_line(new_code)
        for sep in concerned_separators:
            self.separator_list.remove(sep)
        
    def __getitem__(self,i):
        """
        One can call a separator by its title or its number.
        """
        if isinstance(i,basestring):    # Test unicode and str in the same time
            for separator in self.separator_list :
                if separator.title == i :
                    return separator
            raise IndexError,"No separator with title %s"%i
        return self.separator_list[i]

class Separator(object):
    def __init__(self,title):
        self.title = title
        self.latex_code=[]
        self.add_latex_line("%"+self.title)
    def add_latex_line(self,line):
        if isinstance(line,Separator):
            text=line.code()
        else :
            text = "".join(line)        # Notice that "".join(x) also works when x is a string.
        self.latex_code.append(text+"\n")
    def code(self):
        return "".join(self.latex_code)

class DrawElement(object):
    # The attributes take_xxx are intended to say what we have to take into account in the element.
    # If you put take_graph=False, this element will not be drawn, but its bounding boxes are going to be taken into account.
    def __init__(self,graphe,separator_name,take_graph=True,take_BB=True,take_math_BB=True,*args):
        self.take_graph=take_graph
        self.take_BB=take_BB
        self.take_math_BB=take_math_BB
        self.graph=graphe
        self.separator_name=separator_name
        self.st_args=args

class pspicture(object):
    r"""
    Describe a pspicture

    METHODS:

    - `self.pstricks_code()` - contains the pstricks code of what has to be between \begin{pspicture} and \end{pspicture}. This is not the environment itself, neither the definition of xunit, yunit.

    - `self.contenu_pstricks` - is the whole code including the x/yunit and \begin{pspicture}...\end{pspicture}.
                                This is in fact a `lazy_attribute`.
                                
                                This has not to be used for creating other outputs than pure pstricks.
                               
    - `self.latex_code_for_eps()` - the LaTeX code that produces the eps file. This function calls `self.contenu_pstricks`

    - `self.latex_code_for_png()` - the same.

    - `self.latex_code_for_contenu_pdf()` - the same.

    EXAMPLES:

    Creating a new pspicture::

        sage: pspict=pspicture("ThisIsMyName")
        sage: pspict.name
        'ThisIsMyName'

    The name of the pspict is used to produce intermediate filesnames, and other names.
    """
    NomPointLibre = BasicGeometricObjects.PointsNameList()

    def __init__(self,name="CAN_BE_A_PROBLEM_IF_TRY_TO_PRODUCE_EPS_OR_PDF"):
        r"""
        A name is required for producing intermediate files. This is the case when one wants to produce eps/pdf files of one wants to
           make interactions with LaTeX (see pspict.get_counter_value).

        SOME INTERESTING ATTRIBUTES:

        - `self.BB` is the bounding box for LaTeX purpose.

        - `self.math_BB` is the bounding box of objects that are "mathematically relevant". This bounding box does not take into account
            marks of points and thinks like that. This is the bounding box that is going to be used for the axes and the grid.
            When a graph object has a method math_bounding_box, this is the one taken into account in the math_BB here.

        - `self.newwriteName` is the name that will be given to LaTeX in ``\newwrite{...}``. This is not the
                name of the file in which the data is written.

        - `self.interWriteFile` is the name of the file in which the data will be written.
        """
        self.name = name        # self.name is used in order to name the intermediate files when one produces the eps file.
        self.mother=None
        self.figure_mother=None
        self.pstricks_code_list = []
        self.specific_needs = ""    # See the class PspictureToOtherOutputs
        self.newwriteDone = False
        #self.interWriteFile = newwriteName()+".pstricks.aux"
        self.interWriteFile = self.name+".phystricks.aux"
        self.newwriteName = "writeOfphystricks"
        self.NomPointLibre = BasicGeometricObjects.PointsNameList()
        self.record_marks=[]
        self.record_bounding_box=[]
        self.record_draw_graph=[]
        self.record_force_math_bounding_box=[]
        #self.record_math_BB=[]
        #self.record_BB=[]
        self.counterDone = False
        self.newlengthDone = False
        self.listePoint = []
        self.xunit = 1
        self.yunit = 1
        self.LabelSep = 1
        self.BB = BasicGeometricObjects.BoundingBox()
        self.math_BB = BasicGeometricObjects.BoundingBox()     # self.BB and self.math_BB serve to add some objects by hand.
                                            # If you need the bounding box, use self.bounding_box()
                                            # or self.math_bounding_box()
        self.axes=BasicGeometricObjects.Axes(Point(0,0),BasicGeometricObjects.BoundingBox())
        self.single_axeX=self.axes.single_axeX
        self.single_axeY=self.axes.single_axeY

        self.single_axeX.pspict=self
        self.single_axeY.pspict=self

        self.grid = Grid(BasicGeometricObjects.BoundingBox())

        # The order of declaration is important, because it is recorded in the Separator.number attribute.
        self.separator_list = SeparatorList()
        self.separator_list.new_separator("ENTETE PSPICTURE")
        self.separator_list.new_separator("BEFORE PSPICTURE")
        self.separator_list.new_separator("BEGIN PSPICTURE")        # This separator is supposed to contain only \begin{pspicture}
        self.separator_list.new_separator("GRID")
        self.separator_list.new_separator("AXES")
        self.separator_list.new_separator("OTHER STUFF")
        self.separator_list.new_separator("DEFAULT")
        self.separator_list.new_separator("END PSPICTURE")
        self.separator_list.new_separator("AFTER PSPICTURE")

        # The separators corresponding to write and labels have to be apart 
        # because they have to be included differently following
        # 1. we are in a regular pspicture in a figure
        # 2. we are in a subfigure environment : in that case one cannot
        #    put the corresponding code between two subfigures
        # 3. we are building the pdf file.
        self.write_and_label_separator_list=SeparatorList()
        self.write_and_label_separator_list.new_separator("WRITE_AND_LABEL")
        self.write_and_label_separator_list.new_separator("CLOSE_WRITE_AND_LABEL")

    @lazy_attribute
    def contenu_pstricks(self):
        r"""
        The LaTeX of `self` including xunit,yunit and \begin{pspicture} ... \end{pspicture}

        This is a `lazy_attribute` because it has to be used more than once while it adds non
        trivial code to `self`.

        It also creates the attributes `xsize` and `ysize` that
        contain the size of the bounding box.


        NOTE :

        - You are not supposed to use `pspict.bounding_box().xsize()` in order to take
          the size of the picture.

        - One has to declare the xunit,yunit before to give the bounding box.
        
        - The value of LabelSep is the distance between an angle and the label of the angle. It is by default 1, but if there is a dilatation, the visual effect is bad.
        """
        self.create_pstricks_code
        if self.LabelSep == 1 :
            self.LabelSep = 2/(self.xunit+self.yunit)
        add_latex_line_entete(self)
        self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+",LabelSep="+str(self.LabelSep)+"}","BEFORE PSPICTURE")
        self.add_latex_line("\psset{PointSymbol=none,PointName=none,algebraic=true}\n","BEFORE PSPICTURE")
        self.add_latex_line("\\begin{pspicture}%s%s\n"%(self.bounding_box(self).SW().coordinates(numerical=True),self.bounding_box(self).NE().coordinates(numerical=True)),"BEGIN PSPICTURE")
        self.add_latex_line("\end{pspicture}\n","END PSPICTURE")
        self.add_latex_line(self.pstricks_code_list,"OTHER STUFF")

        self.xsize=self.bounding_box(self).xsize()
        self.ysize=self.bounding_box(self).ysize()

        return self.separator_list.code()

    @lazy_attribute
    def create_pstricks_code(self):
        """
        Fix the bounding box and create the separator "PSTRICKS CODE".


        NOTES :

        - This function is not supposed to be used twice. In fact, this is
          supposed to be called only from `lazy_attributes`

        """
        # Here we are supposed to be  sure of the xunit, yunit, so we can compute the BB's needed for the points with marks.
        # For the same reason, all the marks that were asked to be drawn are added now.
        # Most of the difficulty is when the user use pspicture.dilatation_X and Y with different coefficients.
        # TODO : take it into account.

        # Creating the bounding box
        list_to_be_drawn = [a.graph for a in self.record_draw_graph if a.take_graph]
        for graph in list_to_be_drawn:
            try :
                if graph.draw_bounding_box:
                    raise AttributeError,"I don't think that the attribute `draw_bounding_box` still exists"
                    # It seems to me that we can safely remove all this part. March, 29, 2011.
                    bb=graph.bounding_box(self)
                    rect = Rectangle(bb.SW(),bb.NE())
                    rect.parameters.color="cyan"
                    self.DrawGraph(rect)
            except AttributeError :
                pass

        list_to_be_drawn = [a for a in self.record_draw_graph if a.take_graph]

        # Produce the code in the sense that if writes everything in the separators.
        list_used_separators=[]
        for x in list_to_be_drawn:
            graph=x.graph

            # If the graph is a bounding box of a mark, we recompute it
            # because a dilatation of the figure could have
            # changed the bounding box.
            if isinstance(graph,BasicGeometricObjects.BoundingBox):
                if graph.parent:
                    if isinstance(graph.parent,BasicGeometricObjects.Mark):
                        graph=graph.parent.bounding_box(self)

            # If the graph is a mark, then one has to recompute
            # its position because of possible xunit,yunit.
            #if isinstance(graph,Mark):
            #    print "1651 central point",graph.central
            #    if graph.parent:
            #        graph = Mark(graph.parent,graph.dist,graph.angle,graph.text,graph.automatic_place)

            separator_name=x.separator_name
            try :
                self.BB.append(graph,self)
                self.add_latex_line(graph.pstricks_code(self),separator_name)
                list_used_separators.append(separator_name)
            except AttributeError,data:
                if not "pstricks_code" in dir(graph):
                    print "phystricks error: object %s has no pstricks_code method"%(str(graph))
                raise
        self.separator_list.fusion(list_used_separators,"PSTRICKS CODE")

    @lazy_attribute
    def pstricks_code(self):
        r"""
        Return the pstricks code that has to appears between \begin{pspicture} and \end{pspicture}.

        This is a lazy_attribute and perform non trivial task changing the state
        of many other attributes of `self`.
        Among other it changes the bounding box.

        This is called by :func:`contenu_pstricks`
        """
        self.create_pstricks_code
        return self.separator_list["PSTRICKS CODE"].code()

    def default_figure(self,name=None):
        """
        Create and return a Figure object that contains self.

        Example. If pspict is in class pspicture :
        fig=pspict.default_figure
        fig.conclude()
        fig.write_the_file()
        """
        if name == None :
            figname= "DefaultFig"+self.name
        else:
            figname = name
        fig=GenericFigure(figname)
        fig._add_pspicture(self)
        return fig
    def write_the_figure_file(self,name):
        """
        Produce a file that contains self in a default figure.

        To be used if you have a figure at hand and you just want to use it in a figure without particular needs.

        If you want to use the figure outside a figure, use self.write_the_file instead.
        """
        fig=self.default_figure(name+self.name)
        fig.conclude()
        fig.write_the_file()
    def new_separator(self,title):
        raise DeprecationWarning
        self.separator_number = self.separator_number + 1
        self.separator_dico[title]=Separator(title,self.separator_number)
    def initialize_newwrite(self):
        if not self.newwriteDone :
            code = r""" \makeatletter
                \@ifundefined{%s}
                {\newwrite{\%s}
                }
                \makeatother"""%(self.newwriteName,self.newwriteName)
            self.add_latex_line(code,"WRITE_AND_LABEL")

            # The following lines were creating the "TeX capacities exceeded" error.

            #code="""\CatchFileDef \phystricksContent {%s}{\endlinechar=10 }
            #    \immediate\openout\%s=%s
            #    \immediate\write\%s{\phystricksContent}
            #    """%(self.interWriteFile,self.newwriteName,self.interWriteFile,self.newwriteName)
            #self.add_latex_line(code,"WRITE_AND_LABEL")

            code="\immediate\openout\%s=%s"%(self.newwriteName,self.interWriteFile)
            self.add_latex_line(code,"WRITE_AND_LABEL")


            code=r"""\immediate\closeout\%s"""%self.newwriteName
            self.add_latex_line(code,"CLOSE_WRITE_AND_LABEL")

            #code = r"""\makeatletter
            #    \@ifundefined{phystricksAppendToFile}{
            #    \newcommand{\phystricksAppendToFile}[1]{
            #    \CatchFileDef \phystricksContent {%s}{\endlinechar=10 }
            #    \immediate\openout\%s=%s
            #    \immediate\write\%s{\phystricksContent}
            #    \immediate\write\%s{#1}
            #    \immediate\closeout\%s
            #    }
            #    }
            #    \makeatother"""%(self.interWriteFile,newwriteName(),self.interWriteFile,newwriteName(),newwriteName(),newwriteName())
            #self.add_latex_line(code,"WRITE_AND_LABEL")

            self.newwriteDone = True

            # Now we check that the file phystricks.aux exists. If not, we create it.
            exist_aux = os.path.isfile(self.interWriteFile)
            if not exist_aux:
                f=open(self.interWriteFile,"w")
                f.write("a:b-")
                f.close()
    def initialize_counter(self):
        if not self.counterDone:
            code = r""" \makeatletter
                \@ifundefined{c@%s}
                {\newcounter{%s}}
                \makeatother
                """%(counterName(),counterName())           # make LaTeX test if the counter exist before to create it.
            self.add_latex_line(code,"WRITE_AND_LABEL")
            self.counterDone = True
    def initialize_newlength(self):
        if not self.newlengthDone :
            code =r"""
            \makeatletter
            \@ifundefined{%s}{\newlength{\%s}}
            \makeatother
            """%(newlengthName(),newlengthName())
            self.add_latex_line(code,"WRITE_AND_LABEL")
            self.newlengthDone = True
    def add_write_line(self,Id,value):
        r"""Writes in the standard auxiliary file \newwrite an identifier and a value separated by a «:»"""
        interWriteName = self.newwriteName
        self.initialize_newwrite()
        self.add_latex_line(r"\immediate\write\%s{%s:%s-}"%(interWriteName,Id,value),"WRITE_AND_LABEL")
        #self.add_latex_line(r"\phystricksAppendToFile{%s:%s-}"%(Id,value),"WRITE_AND_LABEL")

    @lazy_attribute
    def id_values_dict(self):
        """
        Build the dictionary of stored values in the auxiliary file
        and rewrite that file.
        """
        d={}
        try :
            f=open(self.interWriteFile,"r")
        except IOError :
            print "Warning: the auxiliary file %s seems not to exist. Compile your LaTeX file."%self.interWriteFile
            if global_vars.perform_tests :
                raise ValueError,"I cannot say that a test succeed if I cannot determine the bounding box"
            if global_vars.create_formats["test"] :
                raise ValueError, "I cannot create a test file when I'm unable to compute the bounding box."
            return d
        idlist = f.read().replace('\n','').replace(' ','').replace('\\par','').split("-")
        f.close()

        for els in idlist[0:-1]:
            key=els.split(":")[0]
            value=els.split(':')[1]
            d[key]=value

        f=open(self.interWriteFile,"w")
        for k in d.keys():
            f.write("%s:%s-\n"%(k,d[k]))
        f.close()
        return d
    def get_Id_value(self,Id,counter_name="NO NAME ?",default_value=0):
            if Id not in self.id_values_dict.keys():
                if not global_vars.silent:
                    print "Warning: the auxiliary file %s does not contain the id «%s». Compile your LaTeX file."%(self.interWriteFile,Id)
                if global_vars.perform_tests :
                    raise ValueError, "I cannot tests a file if the auxiliary files are not yet produced."
                if global_vars.create_formats["test"] :
                    raise ValueError, "I cannot create a test file when I'm unable to compute the bounding box."
                return default_value
            return self.id_values_dict[Id]
    def get_counter_value(self,counter_name,default_value=0):
        """
        return the value of the (LaTeX) counter <name> at this point of the LaTeX file

        Makes LaTeX write the value of the counter in an auxiliary file, then reads the value in that file.
        (needs several compilations to work)

        NOTE :

        If you as for the page with for example  `page = pspict.get_counter_value("page")` the given page
        will be the one at which LaTeX think the figure is. I recall that a figure is a floating object;
        if you have 10 of them in a row, the page number could be incorrect.
        """
        # Make LaTeX write the value of the counter in a specific file
        interCounterId = "counter"+self.name+self.NomPointLibre.next()
        self.initialize_counter()
        self.add_write_line(interCounterId,r"\arabic{%s}"%counter_name)
        # Read the file and return the value
        return self.get_Id_value(interCounterId,"counter «%s»"%counter_name,default_value)
    def get_box_dimension(self,tex_expression,dimension_name):
        """
        Return the dimension of the LaTeX box corresponding to the LaTeX expression tex_expression.

        dimension_name is a valid LaTeX macro that can be applied to a LaTeX expression and that return a number. Like
        widthof, depthof, heightof, totalheightof
        """
        interId = dimension_name+self.name+self.NomPointLibre.next()
        self.initialize_newlength()
        self.add_latex_line(r"\setlength{\%s}{\%s{%s}}"%(newlengthName(),dimension_name,tex_expression),"WRITE_AND_LABEL")
        self.add_write_line(interId,r"\the\%s"%newlengthName())
        read_value =  self.get_Id_value(interId,"dimension %s"%dimension_name,default_value="0pt")
        dimenPT = float(read_value.replace("pt",""))
        return dimenPT/30           # 30 is the conversion factor : 1pt=(1/3)mm
    def get_box_size(self,tex_expression):
        """
        return as 2-uple the dimensions of a LaTeX box containing an expression.

        INPUT:
        - ``tex_expression`` - a valid LaTeX expression.

        OUTPUT:
        - ``width,height`` - the dimensions of the box in centimeter.

        EXAMPLE:
        Type the following  in a script :
        text = "$A_i=\int_a^bf_i$"
        dimx,dimy=pspict.get_box_size(text)
        print "The dimensions of the LaTeX text %s is (%s,%s)"%(text,str(dimx),str(dimy))

        After having LaTeX-compiled the document containing the pspicture, a second
        execution of the script should print :
        The dimensions of the LaTeX text $A_i=\int_a^bf_i$ is (1.66653833333,0.46667)

        NOTE:
        As far as the problem is concerned from a LaTeX point of view, it was discussed here:
        http://groups.google.fr/group/fr.comp.text.tex/browse_thread/thread/8431f21588b81530?hl=fr

        This functionality creates an intermediate file.
        """
        height = self.get_box_dimension(tex_expression,"totalheightof")
        width = self.get_box_dimension(tex_expression,"widthof")
        return width,height

    def dilatation(self,fact):
        self.dilatation_X(fact)
        self.dilatation_Y(fact)
    def dilatation_X(self,fact):
        self.xunit = self.xunit * fact
    def dilatation_Y(self,fact):
        self.yunit = self.yunit * fact
    def fixe_tailleX(self,l):
        self.dilatation_X(l/self.BB.tailleX())
    def fixe_tailleY(self,l):
        self.dilatation_Y(l/self.BB.tailleY())
    def AddPoint(self,P):
        self.add_latex_line(self.CodeAddPoint(P))
    def bounding_box(self,pspict=None):
        bb=self.BB
        for a in [x.graph.bounding_box(self) for x in self.record_draw_graph if x.take_math_BB or x.take_BB] :
            bb.AddBB(a)
        return bb
    def DrawBB(self):
        self.DrawBoundingBox(self.BB)
    def DrawBoundingBox(self,obj=None,color="cyan"):
        """Draw the bounding box of an object when it has a method bounding_box

        If not, assume that the object is the bounding box to be drawn.
        If no object are given, draw its own bounding box
        """
        if not obj:
            obj=self
        self.record_bounding_box.append(obj)
    #def TraceNuage_de_Points(self,nuage,symbol,params):
    #   self.add_latex_line("% ---------Nuage de point--------")
    #   for P in nuage.listePoints :
    #       self.DrawPoint(P,symbol,params)

    def MarqueAngle(self,A,B,C,label,params):
        self.add_latex_line("\pstMarkAngle["+params+"]{"+A.psName+"}{"+B.psName+"}{"+C.psName+"}{"+label+"}")
    def TraceCourbeParametrique(self,f,mx,Mx,params):
        raise AttributeError,"The method TraceCourbeParametrique is depreciated"
        self.BB.AddParametricCurve(f,mx,Mx)
        self.add_latex_line("\parametricplot[%s]{%s}{%s}{%s}" %(params,str(mx),str(Mx),f.pstricks()))
    def DrawGraphs(self,*args):
        for gr in args:
            try :
                for h in gr:
                    self.DrawGraph(h)
            except TypeError:
                self.DrawGraph(gr)
    def DrawGraph(self,graph,separator_name=None):
        """
        Draw an object of type `GraphOfASomething`.

        More generally, it can draw anything that has the methods

            1. bounding_box
            2. pstricks_code

        The first one should return a bounding box and the second one should return a valid pstricks code as string.
        If the pstricks code is not valid, LaTeX will get angry but no warning are given here.

        NOTE:

        More precisely, it does not draw the object now, but it add it (and its mark if applicable) to ``self.record_draw_graph``
        which is the list of objects to be drawn. Thus it is still possible to modify the object later (even if discouraged).
        """
        if separator_name==None:
            try :
                separator_name=graph.separator_name
            except AttributeError :
                separator_name="DEFAULT"
        x=DrawElement(graph,separator_name)
        self.record_draw_graph.append(x)
        try :
            if graph.marque:
                x=DrawElement(graph.mark,separator_name)
                self.record_draw_graph.append(x)
        except AttributeError,msg :
            pass            # This happens when the graph has no mark; that is most of the time.
    def DrawDefaultAxes(self):
        """
        This function computes the bounding box of the axes and add them to the list to be drawn.

        The length of the axes is computed here (via self.math_bounding_box).

        Sometimes you want the axes to be slightly larger. You can impose the length of the axes.

        EXAMPLE::

        .. literalinclude:: phystricksEnlargeAxes.py
        .. image:: Picture_FIGLabelFigEnlargeAxesPICTEnlargeAxes-for_eps.png

        """
        BB = self.math_bounding_box()
        BB.add_object(self.axes.C,self,fun="math_bounding_box")     # If you add the no-math bounding box, it adds 0.1
                                                                    # and it becomes ugly when dilating
                                                                    # Notice that we pass here too early to use self.xunit,self.yunit
        self.axes.BB.add_object(BB)
        #epsilonX=float(self.axes.Dx)/2
        #epsilonY=float(self.axes.Dy)/2
        #self.axes.BB.enlarge_a_little(self.axes.Dx,self.axes.Dy,epsilonX,epsilonY)
        self.axes.update()
        self.DrawGraph(self.axes)
    def DrawDefaultGrid(self):
        self.grid.BB = self.math_bounding_box()
        Dx=self.grid.Dx
        Dy=self.grid.Dy
        epsilonX=0
        epsilonY=0
        self.grid.BB.enlarge_a_little(Dx,Dy,epsilonX,epsilonY)  # Make the grid end on its "big" subdivisions.
        self.DrawGraph(self.grid)
    def add_latex_line(self,ligne,separator_name="DEFAULT"):
        """
        Add a line in the pstricks code. The optional argument <position> is the name of a marker like %GRID, %AXES, ...
        """
        if separator_name==None:
            separator_name="DEFAULT"
        if separator_name=="WRITE_AND_LABEL" or separator_name=="CLOSE_WRITE_AND_LABEL":
            self.write_and_label_separator_list[separator_name].add_latex_line(ligne)
        else:
            self.separator_list[separator_name].add_latex_line(ligne)
    def force_math_bounding_box(self,g):
        """
        Add an object to the math bounding box of the pspicture. This object will not be drawn, but the axes and the grid will take it into account.
        """
        self.record_force_math_bounding_box.append(g)
    def math_bounding_box(self):
        """
        Return the current BoundingBox, that is the BoundingBox of the objects that are currently in the list of objects to be drawn.
        """
        bb = self.math_BB.copy()
        for graphe in [x.graph for x in self.record_draw_graph if x.take_math_BB]:
            try :
                bb.add_math_object(graphe,pspict=self)
            except NoMathBoundingBox,message:
                bb.append(graphe,self)
        # These two lines are only useful if the size of the single axes were modified by hand
        # because the method self.math_bounding_box is called by self.DrawDefaultAxes that
        # update the size of the singles axes later.
        try:
            bb.add_object(self.axes.single_axeX,pspict=self)
            bb.add_object(self.axes.single_axeY,pspict=self)
        except ValueError,msg:
            if u"is not yet defined" not in msg.__unicode__():  # position 27319 see BasicGeometricObjects.GraphOfASingleAxe.segment
                raise
        return bb
    def contenu(self):              # pspicture
        r"""
        return the LaTeX code of the pspicture
        
        Also creates the files corresponding to the `exit_format`.

        This is of the form \begin{pspicture} ... \end{pspicture} if
        the global variable `exit_format` is "pstricks".

        In the other cases, this is \includegraphics{...}.
        """
        to_other = PspictureToOtherOutputs(self)
        create_dico=global_vars.create_formats
        # Create files for the requested formats, including tests
        for k in create_dico.keys():
            if create_dico[k] :
                to_other.__getattribute__("create_%s_file"%k)()
        # return the LaTeX code of self

        # This is for png or eps
        if global_vars.exit_format not in ["pstricks","pdf"]:
            return to_other.__getattribute__("input_code_"+global_vars.exit_format)
    
        # This is for pdf and pstricks.
        return "\ifpdf {0}\n \else {1}\n \\fi".format(to_other.input_code_pdf,self.contenu_pstricks)


    def write_the_file(self,f):
        """
        Writes the LaTeX code of the pspict.

        This function is almost never used because most of time we want to pspicture
        to be included in a figure.
        """
        self.fichier = SmallComputations.Fichier(f)
        self.fichier.file.write(self.contenu())
        self.fichier.file.close()

