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

# copyright (c) Laurent Claessens, 2009-2016
# email: laurent@claessens-donadello.eu


from __future__ import division
from __future__ import unicode_literals

from sage.all import *
import sys

import BasicGeometricObjects
import SmallComputations as SmallComputations

from PointGraph import PointsNameList
from Exceptions import *

from phystricks import WrapperStr
var=WrapperStr(var)

from phystricks import *

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
        self.documentation_list=[]
        self.to_be_recompiled_list=[]

    def generate(self):
        """
        perform the tests
        """
        figure.send_noerror = True
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
    r"""
    This is not exactly the 'figure' in the LaTeX sense of the term since it also contains informations about bounding boxes.

    The method `figure.no_figure()` makes disappear the \begin{figure} ... \end{figure}. In this case the LaTeX code of the class figure contains the informations about the bounding boxes and a if/then for inclusion of pspicture or \includegraphics

    - `self.newwriteName` is the name that will be given to LaTeX in ``\newwrite{...}``. This is not the
                name of the file in which the data is written.
    - `self.interWriteFile` is the name of the file in which the data will be written.
    """
    def __init__(self,caption,name,nFich,script_filename):
        self.script_filename=script_filename
        self.caption = caption
        self.name = name
        self.xunit = 1
        self.yunit = 1
        self.figure_environment=True
        self.code = []
        self.record_subfigure = []
        self.record_pspicture=[]
        self.child_pspictures=[]

        self.send_noerror = False
        self.language="tikz"

        self.newwriteName = "writeOfphystricks"
        self.interWriteFile = self.name+".phystricks.aux"
        self.already_used_interId=[]

        self.specific_needs=""
        # TODO : specific_needs should be a list of specific_need that is a class.
        # The idea is to leave to the user the control if the command has to be included in the file 
        # which creates the png and in the "final" file independently.

        self.nFich=nFich
        self.fichier = SmallComputations.Fichier(self.nFich)
        self.comment_filename=self.nFich.replace(".pstricks",".comment")        # This intermediate file will contain the comment of the pspict(s)
                                                                                # for the sake of teses.

        # The order of declaration is important, because it is recorded in the Separator.number attribute.
        self.separator_list=SeparatorList()
        self.separator_list.new_separator("ENTETE FIGURE")
        self.separator_list.new_separator("SPECIFIC_NEEDS")
        self.separator_list.new_separator("OPEN_WRITE_AND_LABEL")
        self.separator_list.new_separator("WRITE_AND_LABEL")
        self.separator_list.new_separator("CLOSE_WRITE_AND_LABEL")
        self.separator_list.new_separator("HATCHING_COMMANDS")
        self.separator_list.new_separator("BEFORE SUBFIGURES")
        self.separator_list.new_separator("SUBFIGURES")
        self.separator_list.new_separator("AFTER SUBFIGURES")
        self.separator_list.new_separator("DEFAULT")
        self.separator_list.new_separator("BEFORE PSPICTURE")
        self.separator_list.new_separator("PSPICTURE")
        self.separator_list.new_separator("AFTER PSPICTURE")
        # the separators 'BEFORE SUBFIGURE' and 'AFTER ALL' will not be written in the case when self.figure_environment=False.
        self.separator_list.new_separator("AFTER ALL")  # caption and \end{figure}
        add_latex_line_entete(self)
        self.add_latex_line("\\begin{figure}[ht]","BEFORE SUBFIGURES")
        self.add_latex_line("\centering","BEFORE SUBFIGURES")
    def no_figure(self):
        self.figure_environment=False
    def rotation(self,angle):
        self.rotation_angle=angle
    def dilatation_X(self,fact):
        """ Makes a dilatation of the whole picture in the X direction. A contraction if the coefficient is lower than 1 """
        raise# It seem to me that one never use dilatation on the figure (always on the pspicture)
        self.xunit = self.xunit * fact
    def dilatation_Y(self,fact):
        raise   # It seem to me that one never use dilatation on the figure (always on the pspicture)
        self.yunit = self.yunit * fact
    def dilatation(self,fact):
        """ dilatations or contract that picture in both directions with the same coefficient """

        raise# It seem to me that one never use dilatation on the figure (always on the pspicture)
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
    def _append_subfigure(self,ssFig):
        self.record_subfigure.append(ssFig)
        suffixe = "ssFig"+str(len(self.record_subfigure))
        if not ssFig.name:
            ssFig.name=self.name+suffixe
        print r"See also the subfigure \ref{%s}"%ssFig.name
    def new_pspicture(self,name=None,pspict=None):
        if name==None:
            number=len(self.record_pspicture)
            name="sub"+latinize(str(number))
        if pspict==None:
            pspict=pspicture("FIG"+self.name+"PICT"+name)
        pspict.figure_mother=self
        self._add_pspicture(pspict)
        return pspict
    def add_latex_line(self,ligne,separator_name="DEFAULT"):
        self.separator_list[separator_name].add_latex_line(ligne)
    def _add_pspicture(self,pspict):
        pspict.mother=self
        pspict.figure_mother=self
        self.record_pspicture.append(pspict)
    def comments(self):
        a=[]
        for pspict in self.child_pspictures:
            comment=pspict.comment.decode('utf8')
            if comment != "":
                a.append("Comment : "+comment)
        return "\n".join(a)
    def LaTeX_lines(self):
        """
        Return the lines to be included in your LaTeX file.
        """
        a=[]
        a.append(self.comments())
        from latex_to_be import pseudo_caption
        if self.figure_environment:
            a.append("The result is on figure \\ref{"+self.name+"}. % From file "+self.script_filename)
            # The pseudo_caption is changed to the function name later.
            a.append("\\newcommand{"+self.caption+"}{"+pseudo_caption+"}")
            a.append("\\input{%s}"%(self.nFich))
        else :
            #text="""\\begin{wrapfigure}{r}{WIDTH}
#   \\vspace{-0.5cm}        % à adapter.
#   \centering
#   INCLUSION
#\end{wrapfigure}
#ou
            text="""\\begin{center}
   INCLUSION
\end{center}""".replace("INCLUSION","\\input{%s}"%(self.nFich))
            if len(self.record_pspicture)==1:
                pspict=self.record_pspicture[0]
                visual_xsize=pspict.visual_xsize()      # By the way, this is a reason why we cannot do this before to have
                                                        # concluded the pictute.
                text=text.replace("WIDTH",str(n(visual_xsize,3))+"cm")
            a.append(text)
        text = "\n".join(a)
        return text
        
    def conclude(self):
        code = r"""\makeatletter\@ifundefined{{{}}}{{\newwrite{{\{}}}}}{{}}\makeatother%""".format(self.newwriteName,self.newwriteName)
        self.add_latex_line(code,"OPEN_WRITE_AND_LABEL")

        code =r"""\makeatletter\@ifundefined{{{}}}{{\newlength{{\{}}}}}{{}}\makeatother%""".format(newlengthName(),newlengthName())
        self.add_latex_line(code,"OPEN_WRITE_AND_LABEL")

        code="\immediate\openout\{}={}%".format(self.newwriteName,self.interWriteFile)
        self.add_latex_line(code,"OPEN_WRITE_AND_LABEL")

        code=r"\immediate\closeout\{}%".format(self.newwriteName)+"\n"
        self.add_latex_line(code,"CLOSE_WRITE_AND_LABEL")

        # Now we check that the file phystricks.aux exists. If not, we create it.
        if not os.path.isfile(self.interWriteFile):
            f=open(self.interWriteFile,"w")
            #f.write("a:b-")
            f.write("default:content-")
            f.close()
        

        for pspict in self.record_pspicture :
            # Here we add the picture itself. What happens depends on --eps, --pdf, --png, ...
            self.add_latex_line(pspict.contenu(),"PSPICTURE")

            # What has to be written in the WRITE_AND_LABEL part of the picture is written now
            # This has to be done _after_ having called pspict.contenu().
            self.add_latex_line(pspict.write_and_label_separator_list["WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")

            # No more closing the write at each picture (Augustus 28, 2014)
            #self.add_latex_line(pspict.write_and_label_separator_list["CLOSE_WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")

            # For the following big stuff, see the position 170321508
            def_length_tex=r"""                 \makeatletter
% If hatchspread is not defined, we define it
\ifthenelse{\value{defHatch}=0}{
\setcounter{defHatch}{1}
\newlength{\hatchspread}%
\newlength{\hatchthickness}%
}{}
               \makeatother               """

            def_pattern_tex=r"""               \makeatletter
\ifthenelse{\value{defPattern}=0}{
\setcounter{defPattern}{1}
\pgfdeclarepatternformonly[\hatchspread,\hatchthickness]% variables
   {custom north west lines}% name
   {\pgfqpoint{-2\hatchthickness}{-2\hatchthickness}}% lower left corner
   {\pgfqpoint{\dimexpr\hatchspread+2\hatchthickness}{\dimexpr\hatchspread+2\hatchthickness}}% upper right corner
   {\pgfqpoint{\hatchspread}{\hatchspread}}% tile size
   {% shape description
    \pgfsetlinewidth{\hatchthickness}
    \pgfpathmoveto{\pgfqpoint{0pt}{\hatchspread}}
    \pgfpathlineto{\pgfqpoint{\dimexpr\hatchspread+0.15pt}{-0.15pt}}
        \pgfusepath{stroke}
   }
   }{}
   \makeatother               """

            if pspict.language=="tikz":
                self.add_latex_line(def_length_tex,"HATCHING_COMMANDS")
                self.add_latex_line(def_pattern_tex,"HATCHING_COMMANDS")


            if global_vars.perform_tests:
                TestPspictLaTeXCode(pspict).test()
        self.add_latex_line(self.specific_needs,"SPECIFIC_NEEDS")
        if not global_vars.special_exit() :
            if self.language=="pstricks":
                self.add_latex_line("\psset{xunit=1,yunit=1}","BEFORE SUBFIGURES")
        for f in self.record_subfigure :
            self.add_latex_line("\subfigure["+f.caption+"]{%","SUBFIGURES")
            self.add_latex_line(f.subfigure_code(),"SUBFIGURES")
            self.add_latex_line("\label{%s}"%f.name,"SUBFIGURES")
            self.add_latex_line("}                  % Closing subfigure "+str(self.record_subfigure.index(f)+1),"SUBFIGURES")
            self.add_latex_line("%","SUBFIGURES")

            for pspict in f.record_pspicture:
                self.add_latex_line(pspict.write_and_label_separator_list["WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")
                #self.add_latex_line(pspict.write_and_label_separator_list["CLOSE_WRITE_AND_LABEL"].code(),"WRITE_AND_LABEL")
        after_all=r"""\caption{%s}\label{%s}
            \end{figure}
            """%(self.caption,self.name)
        self.add_latex_line(after_all,"AFTER ALL")
        if self.figure_environment:
           self.contenu = self.separator_list.code().replace("\n\n","\n")
        else :
           self.contenu = self.separator_list.code(not_to_be_used=["BEFORE SUBFIGURES","AFTER ALL"]).replace("\n\n","\n")
    def write_the_file(self):
        """
        Write the figure in the file.

        Do not write if we are testing.
        It also remove the tikz externalize file.
        """
        to_be_written=self.contenu              # self.contenu is created in self.conclude
        if not global_vars.perform_tests :
            self.fichier.open_file("w")
            self.fichier.file.write(to_be_written)
            self.fichier.file.close()
        print "--------------- For your LaTeX file ---------------"
        print(self.LaTeX_lines())
        print "---------------------------------------------------"
        # One only sends the "no error" signal if we are performing a list of tests.

        import codecs
        f=codecs.open(self.comment_filename,"w",encoding='utf8')
        f.write(self.comments())
        f.close()

        if self.send_noerror :
            raise PhystricksNoError(self)
            
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
        pspict.figure_mother=self.mother    # The mother of a pspict inside a subfigure is the figure (not the subfigure)
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
    truc.add_latex_line("% https://github.com/LaurentClaessens/phystricks",position)

class SeparatorList(object):
    """
    Represent a dictionary of :class:`Separator`
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
    def code(self,not_to_be_used=[]):
        return "".join(separator.code() for separator in self.separator_list if separator.title not in not_to_be_used)
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
    def add_latex_line(self,line,add_line_jump=True):
        if isinstance(line,Separator):
            text=line.code()
        else :
            try :
                text = "".join(line)        # Notice that "".join(x) also works when x is a string.
            except TypeError :
                print("IYLooHnThmX WOW")
                print type(line)
                print dir(line)
                raise
        self.latex_code.append(text)
        if add_line_jump :
            self.latex_code.append("\n")
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

    - `self.latex_code()` - contains the tikz code of what has to be between \begin{tikz} and \end{tikz}. This is not the environment itself, neither the definition of xunit, yunit.

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
    NomPointLibre = PointGraph.PointsNameList()

    def __init__(self,name="CAN_BE_A_PROBLEM_IF_TRY_TO_PRODUCE_EPS_OR_PDF"):
        r"""
        A name is required for producing intermediate files. This is the case when one wants to produce eps/pdf files of one wants to
           make interactions with LaTeX (see pspict.get_counter_value).

        SOME INTERESTING ATTRIBUTES:

        - `self.BB` is the bounding box for LaTeX purpose.

        - `self.math_BB` is the bounding box of objects that are "mathematically relevant". This bounding box does not take into account
            marks of points and thinks like that. This is the bounding box that is going to be used for the axes and the grid.
            When a graph object has a method math_bounding_box, this is the one taken into account in the math_BB here.


        """
        self.name = name        # self.name is used in order to name the intermediate files when one produces the eps file.
        self.comment=""         # A comment. This is not used to create the picture; the purpose is to remember a specific feature to be
                                #            tested when recompiling.
        self.tikzfilename="tikz"+self.name
        self.mother=None
        self.figure_mother=None
        self.language="tikz"
        self.pstricks_code_list = []
        self.newwriteDone = False

        # self.interWriteFile is redefined in MultiplePictures

        self.NomPointLibre = PointGraph.PointsNameList()
        self.record_marks=[]
        self.record_bounding_box=[]
        self.record_draw_graph=[]
        self.record_draw_bb=[]
        self.record_force_math_bounding_box=[]
        #self.record_math_BB=[]
        #self.record_BB=[]
        self.counterDone = False
        self.newlengthDone = False
        self.listePoint = []
        self.xunit = 1
        self.yunit = 1
        self.rotation_angle=None
        self.LabelSep = 1
        self.BB = BasicGeometricObjects.BoundingBox(mother=self)
        self.math_BB = BasicGeometricObjects.BoundingBox(math=True)     # self.BB and self.math_BB serve to add some objects by hand.
                                            # If you need the bounding box, use self.bounding_box()
                                            # or self.math_bounding_box()
        self.axes=BasicGeometricObjects.Axes(Point(0,0),BasicGeometricObjects.BoundingBox(),pspict=self)
        self.single_axeX=self.axes.single_axeX
        self.single_axeY=self.axes.single_axeY
        self.single_axeX.pspict=self
        self.single_axeY.pspict=self
        self.draw_default_axes=False
        self._bounding_box=None

        self.mx_acceptable_BB=-100
        self.my_acceptable_BB=-100
        self.Mx_acceptable_BB=100
        self.My_acceptable_BB=100

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

        # In fact now WRITE_AND_LABEL is managed by the figure.

        self.write_and_label_separator_list=SeparatorList()
        self.write_and_label_separator_list.new_separator("WRITE_AND_LABEL")

        self.already_warned_CompileYourLaTeXFile=False

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
        raise DeprecationWarning
        self.create_latex_code(self,language="pstricks")
        if self.LabelSep == 1 :
            self.LabelSep = 2/(self.xunit+self.yunit)
        add_latex_line_entete(self)

        self.add_latex_line("\psset{xunit=1,yunit=1,LabelSep="+str(self.LabelSep)+"}","BEFORE PSPICTURE")
        self.add_latex_line("\psset{PointSymbol=none,PointName=none,algebraic=true}","BEFORE PSPICTURE")
        self.add_latex_line("\\begin{pspicture}%s%s"%(self.bounding_box(self).SW().coordinates(numerical=True),self.bounding_box(self).NE().coordinates(numerical=True)),"BEGIN PSPICTURE")

        self.add_latex_line("\end{pspicture}","END PSPICTURE")

        # It seems to me that "OTHER STUFF" is never used, June 23 2014
        #self.add_latex_line(self.pstricks_code_list,"OTHER STUFF")

        self.xsize=self.bounding_box(self).xsize()
        self.ysize=self.bounding_box(self).ysize()
        return self.separator_list.code()
    @lazy_attribute
    def contenu_tikz(self):
        """
        It also remove the tikz externalize file.
        """
        self.create_latex_code(language="tikz",pspict=self)
        add_latex_line_entete(self)
        self.add_latex_line("\\tikzsetnextfilename{{{0}}}".format(self.tikzfilename),"BEGIN PSPICTURE")
        self.add_latex_line("\\begin{{tikzpicture}}[xscale={0},yscale={1},inner sep=2.25pt,outer sep=0pt]".format(1,1),"BEGIN PSPICTURE")
        #self.add_latex_line("\pgfmathdeclarefunction{radsin}{1}{\pgfmathparse{sin(deg(#1))}}","BEFORE PSPICTURE")
        #self.add_latex_line("\pgfmathdeclarefunction{radcos}{1}{\pgfmathparse{cos(deg(#1))}}","BEFORE PSPICTURE")
        self.add_latex_line("\\end{tikzpicture}","END PSPICTURE")

        self.xsize=self.bounding_box(self).xsize()
        self.ysize=self.bounding_box(self).ysize()
    
        # We do no more remove the pdf file because tikz has its md5 stuff that make the work. (December 6, 2014)
        #import os
        #print(self.tikzfilename)
        #tikz_pdf_filename=self.tikzfilename+".pdf"
        #if os.path.isfile(tikz_pdf_filename):
        #    print("The tikz file {0} exists. I remove it.".format(tikz_pdf_filename))
        #    import shutil
        #    shutil.os.remove(tikz_pdf_filename)

        return self.separator_list.code()

    def visual_xsize(self):
        return numerical_approx(self.xsize*self.xunit)
    def visual_ysize(self):
        return numerical_approx(self.ysize*self.yunit)
    def create_latex_code(self,language=None,pspict=None):
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
        list_to_be_drawn = [a for a in self.record_draw_graph if a.take_graph]

        list_used_separators=[]
        # STEP : update the bounding box
        for x in list_to_be_drawn :
            self.BB.append(x.graph,self)

            # The math_BB is updated in DrawGraph    February 21, 2015
            # This allow to enlarge the BB by hand with something like
            #    pspict.math_BB.ymax+=1
            # placed after DrawGraph
            #if not isinstance(x.graph,BasicGeometricObjects.Mark):
            #    self.math_BB.append(x.graph,self)


        # STEP : add the axes
        if self.draw_default_axes:
            self.axes.add_bounding_box(self.math_BB,self)     # Here the axes take into account the content of pspict.
            graph=self.axes
            if self.axes.do_enlarge :
                self.axes.enlarge_a_little(self.axes.enlarge_size,pspict=self)  # This should be the only call to enlarge_a_little

            separator_name=graph.separator_name
            self.add_latex_line(graph.latex_code(language=language,pspict=self),separator_name)
            list_used_separators.append(separator_name)

            self.BB.append(self.axes,pspict=self)                   # Here the pspict takes into account the enlarging of the axes

            for single in [self.axes.single_axeX,self.axes.single_axeY]:
                if single.marque:
                    self.BB.append(single.mark,self)                     # Here the marks on the axes are taken into account in
                                                                    # the bounding box of the pspicture.

        # STEP : release the bounding box
        self._bounding_box=self.BB      # At this point the bounding box of the pspict is known.

        # STEP : add the LaTeX code of each element
        for x in list_to_be_drawn:
            graph=x.graph

            # If the graph is a bounding box of a mark, we recompute it
            # because a dilatation of the figure could have
            # changed the bounding box.
            # Same for the bounding box of the pspicture, since it is not know before now
            if isinstance(graph,BasicGeometricObjects.BoundingBox):
                if graph.mother:
                    print "I'm drawing the bounding box of ",graph.mother
                    graph=graph.mother.bounding_box(self)
            separator_name=x.separator_name
            try :
                self.add_latex_line(graph.latex_code(language=self.language,pspict=self),separator_name)
                list_used_separators.append(separator_name)
            except AttributeError,data:
                if not "latex_code" in dir(graph):
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
        raise DeprecationWarning
        self.create_language_code
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
    def initialize_newwrite(self):
        raise DeprecationWarning    # Augustus, 28, 2014
        if not self.newwritedone :
            code = r"""\makeatletter\@ifundefined{{{}}}{{\newwrite{{\{}}}}}{{}}\makeatother%""".format(self.newwriteName,self.newwriteName)
            self.add_latex_line(code,"WRITE_AND_LABEL")

            code="\immediate\openout\{}={}%".format(self.newwriteName,self.interWriteFile)
            self.add_latex_line(code,"OPEN_WRITE_AND_LABEL")

            code=r"\immediate\closeout\{}%".format(self.newwriteName)+"\n"
            self.add_latex_line(code,"CLOSE_WRITE_AND_LABEL",add_line_jump=False)
            self.newwriteDone = True

            # Now we check that the file phystricks.aux exists. If not, we create it.
            exist_aux = os.path.isfile(self.interWriteFile)
            if not exist_aux:
                f=open(self.interWriteFile,"w")
                #f.write("a:b-")
                f.write("default:content-")
                f.close()

    def initialize_counter(self):
        if not self.counterDone:
            # make LaTeX test if the counter exist before to create it. 
            code = r"""\makeatletter\@ifundefined{{c@{}}}{{\newcounter{{{}}}}}{{}}\makeatother%""".format(counterName(),counterName())       
            self.add_latex_line(code,"WRITE_AND_LABEL")
            self.counterDone = True
    def initialize_newlength(self):
        raise DeprecationWarning   # Augustus, 28, 2014
        if not self.newlengthDone :
            code =r"""\makeatletter\@ifundefined{{{}}}{{\newlength{{\{}}}}}{{}}\makeatother%""".format(newlengthName(),newlengthName())
            self.add_latex_line(code,"OPEN_WRITE_AND_LABEL")
            self.newlengthDone = True
    def makeWriteValue(self,Id,value):
        r"""Ask LaTeX to write the result of `value` into the standard auxiliary file with identifier `Id`

            - `Id` some string that identifies what we will write (for reading the file later). Preferably ASCII string.

            - `value` a LaTeX code that returns something; that something will be written. Typically this is a string like 
                    \arabic{\thesection}
        """
        self.figure_mother.add_latex_line(r"\immediate\write\{}{{{}:{}-}}".format(self.figure_mother.newwriteName,Id,value),"WRITE_AND_LABEL")

    @lazy_attribute
    def id_values_dict(self):
        """
        Build the dictionary of stored values in the auxiliary file
        and rewrite that file.
        """
        d={}
        try :
            f=open(self.figure_mother.interWriteFile,"r")
        except IOError :
            if not self.already_warned_CompileYourLaTeXFile:
                print "Warning: the auxiliary file %s seems not to exist. Compile your LaTeX file."%self.figure_mother.interWriteFile
                self.already_warned_CompileYourLaTeXFile=True
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

        f=open(self.figure_mother.interWriteFile,"w")
        for k in d.keys():
            f.write("%s:%s-\n"%(k,d[k]))
        f.close()
        return d
    def get_Id_value(self,Id,default_value=0):
        if Id not in self.id_values_dict.keys():
            if not global_vars.silent:
                if not self.already_warned_CompileYourLaTeXFile:
                    print "Warning: the auxiliary file %s does not contain the id «%s». Compile your LaTeX file."%(self.figure_mother.interWriteFile,Id)
                    self.already_warned_CompileYourLaTeXFile=True
            if global_vars.perform_tests :
                raise PhystricksTestError(justification="No tests file found.",pspict=self)
            if global_vars.create_formats["test"] :
                raise ValueError, "I cannot create a test file when I'm unable to compute the bounding box."
            return default_value
        value = self.id_values_dict[Id]
        return value
    def get_counter_value(self,counter_name,default_value=0):
        """
        return the value of the (LaTeX) counter <name> at this point of the LaTeX file

        Makes LaTeX write the value of the counter in an auxiliary file, then reads the value in that file.  (needs several compilations to work)

        RETURN : float

        NOTE :

        If you ask for the page with for example  `page = pspict.get_counter_value("page")` the given page will be the one at which LaTeX thinks the figure is. I recall that a figure is a floating object; if you have 10 of them in a row, the page number could be incorrect.
        """

        # Make LaTeX write the value of the counter in a specific file
        interCounterId = "counter"+self.name+self.NomPointLibre.next()
        self.initialize_counter()
        s=r"\arabic{%s}"%counter_name
        self.makeWriteValue(interCounterId,s)


        # Read the file and return the value
        s = self.get_Id_value(interCounterId,default_value)
        return float(s)

    def get_box_dimension(self,tex_expression,dimension_name):
        """
        Return the dimension of the LaTeX box corresponding to the LaTeX expression tex_expression.

        dimension_name is a valid LaTeX macro that can be applied to a LaTeX expression and that return a number. Like
        widthof, depthof, heightof, totalheightof
        """
        import hashlib
        h=hashlib.new("sha1")
        h.update(tex_expression.encode("utf8"))
        interId=dimension_name+h.hexdigest()
        if interId not in self.figure_mother.already_used_interId :
            self.figure_mother.add_latex_line(r"\setlength{{\{}}}{{\{}{{{}}}}}%".format(newlengthName(),dimension_name,tex_expression),"WRITE_AND_LABEL")
            value=r"\the\%s"%newlengthName()

            self.figure_mother.add_latex_line(r"\immediate\write\{}{{{}:{}-}}".format(self.figure_mother.newwriteName,interId,value),"WRITE_AND_LABEL")

            self.figure_mother.already_used_interId.append(interId)
        #read_value=self.get_Id_value(interId,"dimension %s"%dimension_name,default_value="0pt")
        read_value=self.get_Id_value(interId,default_value="0pt")
        dimenPT=float(read_value.replace("pt",""))
        return (dimenPT)/30           # 30 is the conversion factor : 1pt=(1/3)mm
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
    def rotation(self,angle):
        self.rotation_angle=angle
    def fixe_tailleX(self,l):
        self.dilatation_X(l/self.BB.tailleX())
    def fixe_tailleY(self,l):
        self.dilatation_Y(l/self.BB.tailleY())
    def AddPoint(self,P):
        self.add_latex_line(self.CodeAddPoint(P))
    def bounding_box(self,pspict=None):
        if not self._bounding_box:
            print "Warning : this will be an approximation. In particular the enlarging of the axes will not be taken into account"
            # the bounding box of the figure is not know before the end of `create_language_code`
            # because we have to know the content of the pspicture and the enlarging of the axes.
            bb=self.BB
            for a in [x.graph.bounding_box(self) for x in self.record_draw_graph if x.take_math_BB or x.take_BB] :
                bb.AddBB(a)
            return bb
        return self._bounding_box
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
    def DrawGraphs(self,*args,**arg):
        if "separator_name" not in arg.keys():
            separator_name="DEFAULT"
        else:
            separator_name=arg["separator_name"]
        for gr in args:
            try :
                for h in gr:
                    self.DrawGraphs(h,separator_name=separator_name)
            except TypeError:
                self.DrawGraph(gr,separator_name=separator_name)
    def DrawGraph(self,graph,separator_name=None):
        """
        Draw an object of type `<Something>Graph`.

        More generally, it can draw anything that has the methods

            1. bounding_box
            2. tikz_code

        The first one should return a bounding box and the second one should return a valid tikz code as string.

        NOTE:

        More precisely, it does not draw the object now, but it add it (and its mark if applicable) to ``self.record_draw_graph`` which is the list of objects to be drawn. Thus it is still possible to modify the object later (even if discouraged).
        """
        from phyFunctionGraph import phyFunctionGraph
        if isinstance(graph,phyFunctionGraph):
            if graph.mx==None or graph.Mx==None:
                raise TypeError,"You cannot draw phyFunction but only graph."
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
            pass   # Happens when the graph has no mark (most of time)

        self.math_BB.append(graph,self)
        graph.action_on_pspict(self)
    def DrawDefaultAxes(self):
        """
        This function computes the bounding box of the axes and add them to the list to be drawn.

        The length of the axes is computed here (via self.math_bounding_box).

        Sometimes you want the axes to be slightly larger. You can impose the length of the axes.

        EXAMPLE::

        .. literalinclude:: phystricksEnlargeAxes.py
        .. image:: Picture_FIGLabelFigEnlargeAxesPICTEnlargeAxes-for_eps.png

        """
        BB = self.math_bounding_box(pspict=self)
        BB.add_object(self.axes.C,self,fun="math_bounding_box")     # If you add the no-math bounding box, it adds 0.1
                                                                    # and it becomes ugly when dilating
                                                                    # Notice that we pass here too early to use self.xunit,self.yunit
        self.axes.BB.add_object(BB)
        self.draw_default_axes=True
    def DrawDefaultGrid(self):
        self.grid.BB = self.math_bounding_box()
        Dx=self.grid.Dx
        Dy=self.grid.Dy
        # Make the grid end on its "big" subdivisions.
        self.grid.BB.xmin=SmallComputations.MultipleLower(self.grid.BB.xmin,Dx)
        self.grid.BB.xmax=SmallComputations.MultipleBigger(self.grid.BB.xmax,Dx)
        self.grid.BB.ymin=SmallComputations.MultipleLower(self.grid.BB.ymin,Dy)
        self.grid.BB.ymax=SmallComputations.MultipleBigger(self.grid.BB.ymax,Dy)
        self.DrawGraph(self.grid)
    def add_latex_line(self,ligne,separator_name="DEFAULT",add_line_jump=True):
        """
        Add a line in the pstricks code. The optional argument <position> is the name of a marker like %GRID, %AXES, ...
        """
        if separator_name==None:
            separator_name="DEFAULT"
        if separator_name=="WRITE_AND_LABEL" or separator_name=="CLOSE_WRITE_AND_LABEL":
            self.write_and_label_separator_list[separator_name].add_latex_line(ligne,add_line_jump=add_line_jump)
        else:
            self.separator_list[separator_name].add_latex_line(ligne,add_line_jump=add_line_jump)
    def force_math_bounding_box(self,g):
        """
        Add an object to the math bounding box of the pspicture. This object will not be drawn, but the axes and the grid will take it into account.
        """
        self.record_force_math_bounding_box.append(g)
    def math_bounding_box(self,pspict=None):
        """
        Return the current BoundingBox, that is the BoundingBox of the objects that are currently in the list of objects to be drawn.
        """
        bb = self.math_BB.copy()
        for obj in self.record_force_math_bounding_box :
            bb.add_math_object(obj)
        for graphe in [x.graph for x in self.record_draw_graph if x.take_math_BB]:
            try :
                bb.add_math_object(graphe,pspict=self)
            except NoMathBoundingBox,message:
                bb.append(graphe,self)
        # These two lines are only useful if the size of the single axes were modified by hand
        # because the method self.math_bounding_box is called by self.DrawDefaultAxes that
        # updates the size of the singles axes later.
        try:
            bb.add_object(self.axes.single_axeX,pspict=self)
            bb.add_object(self.axes.single_axeY,pspict=self)
        except ValueError,msg:
            if u"is not yet defined" not in msg.__unicode__():  # position 27319 see BasicGeometricObjects.SingleAxeGraph.segment
                raise
        return bb
    def test_if_test_file_is_present(self):
        test_file=SmallComputations.Fichier("test_pspict_LaTeX_%s.tmp"%(self.name))
        return os.path.isfile(test_file.filename)
    def contenu(self):              # pspicture
        r"""
        return the LaTeX code of the pspicture
        
        Also creates the files corresponding to the `exit_format`.

        It produces an "ifpdf" that choice a pspicture or an \includegraphics
        """
        to_other = PspictureToOtherOutputs(self)
        create_dico=global_vars.create_formats
        # Create files for the requested formats, including tests

        for k in create_dico.keys():
            if create_dico[k] :
                to_other.__getattribute__("create_%s_file"%k)()

        # return the LaTeX code of self

        if not global_vars.no_compilation :
            a = to_other.__getattribute__("input_code_"+global_vars.exit_format)
            try:
                size=numerical_approx(self.xsize,5)*numerical_approx(self.xunit,5)   
            except ValueError :
                print("self.xsize",self.xsize)
                print("Approximation :",numerical_approx(self.xsize))
                print("self.xunit",self.xunit)
                print("Approximation : ",numerical_approx(self.xunit))
                raise
            include_line = a.replace('WIDTH',str(size)+"cm")
        else:
            include_line="\\includegraphicsSANSRIEN"    # If one does not compile, the inclusion make no sense

        if self.language=="tikz":
            return self.contenu_tikz
        else:
            return "\ifpdf {0}\n \else {1}\n \\fi".format(include_line,self.contenu_pstricks)
