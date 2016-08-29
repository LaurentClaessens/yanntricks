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

from Utilities import PointsNameList
from Separator import SeparatorList

class Picture(object):
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

    The name of the pspict is used to produce intermediate filesnames, and other names.
    """
    NomPointLibre = PointsNameList()

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
        from Constructors import BoundingBox,Axes,Grid,Point
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

        self.NomPointLibre = PointsNameList()
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
        self.BB = BoundingBox(mother=self)
        self.math_BB = BoundingBox(math=True)     # self.BB and self.math_BB serve to add some objects by hand.
                                            # If you need the bounding box, use self.bounding_box()
                                            # or self.math_bounding_box()
        self.axes=Axes(Point(0,0),BoundingBox(),pspict=self)
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

        self.grid = Grid(BoundingBox())

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
    def contenu_tikz(self):
        """
        It also remove the tikz externalize file.
        """
        self.create_latex_code(language="tikz",pspict=self)
        add_latex_line_entete(self)
        self.add_latex_line("\\tikzsetnextfilename{{{0}}}".format(self.tikzfilename),"BEGIN PSPICTURE")
        self.add_latex_line("\\begin{{tikzpicture}}[xscale={0},yscale={1},inner sep=2.25pt,outer sep=0pt]".format(1,1),"BEGIN PSPICTURE")
        self.add_latex_line("\\end{tikzpicture}","END PSPICTURE")

        self.xsize=self.bounding_box(self).xsize()
        self.ysize=self.bounding_box(self).ysize()
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
    def initialize_counter(self):
        if not self.counterDone:
            # make LaTeX test if the counter exist before to create it. 
            code = r"""\makeatletter\@ifundefined{{c@{}}}{{\newcounter{{{}}}}}{{}}\makeatother%""".format(counterName(),counterName())       
            self.add_latex_line(code,"WRITE_AND_LABEL")
            self.counterDone = True

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
        Build the dictionary of stored values in the auxiliary file and rewrite that file.
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

    def get_box_dimension(self,tex_expression,dimension_name,default_value="0pt"):
        """
        Return the dimension of the LaTeX box corresponding to the LaTeX expression tex_expression.

        dimension_name is a valid LaTeX macro that can be applied to a LaTeX expression and that return a number. Like
        widthof, depthof, heightof, totalheightof
        """
        import hashlib
        from Utilities import newlengthName
        h=hashlib.new("sha1")
        h.update(tex_expression.encode("utf8"))
        interId=dimension_name+h.hexdigest()
        if interId not in self.figure_mother.already_used_interId :
            self.figure_mother.add_latex_line(r"\setlength{{\{}}}{{\{}{{{}}}}}%".format(newlengthName(),dimension_name,tex_expression),"WRITE_AND_LABEL")
            value=r"\the\%s"%newlengthName()

            self.figure_mother.add_latex_line(r"\immediate\write\{}{{{}:{}-}}".format(self.figure_mother.newwriteName,interId,value),"WRITE_AND_LABEL")

            self.figure_mother.already_used_interId.append(interId)
        read_value=self.get_Id_value(interId,default_value=default_value)
        dimenPT=float(read_value.replace("pt",""))
        return (dimenPT)/30           # 30 is the conversion factor : 1pt=(1/3)mm
    def get_box_size(self,tex_expression,default_value="0pt"):
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
        height = self.get_box_dimension(tex_expression,"totalheightof",default_value=default_value)
        width = self.get_box_dimension(tex_expression,"widthof",default_value=default_value)
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
    def deal_with_graph(self,gr,separator_name):
        from ObjectGraph import AddedObjects
        from ObjectGraph import ObjectGraph
        import collections
        if isinstance(gr,AddedObjects):
            self.DrawGraphs(gr[self])
            return None
        if isinstance(gr,collections.Iterable):
            for h in gr:
                self.DrawGraphs(h,separator_name=separator_name)
            return None
        self._DrawGraph(gr,separator_name=separator_name)
        
        # This is for testing purpose only. To be removed in production.
        if not isinstance(gr,ObjectGraph):
            print("ooKQKUooAxpKXr -- What are you drawing ?")
            raise 

    def DrawGraphs(self,*args,**arg):
        """
        The function DrawGraphs basically takes a list of objects and performs
        different kind of operation following the type of each "object" :

        If the object it iterable, its elements are re-passed to DrawGraphs
        If the object is an instance of "ObjectGraph", it is passed to _DrawGraph
        If the object is 'AddedObject', the list corresponding to 'self' is re-passed to DrawGraphs.

    """
        if "separator_name" not in arg.keys():
            separator_name="DEFAULT"
        else:
            separator_name=arg["separator_name"]

        # Here is why objects intended to be drawn cannot be iterable. Position 30282-11562 
        for gr in args:
            self.deal_with_graph(gr,separator_name)

    def _DrawGraph(self,graph,separator_name=None):
        """
        Draw an object of type `<Something>Graph`.

        More generally, it can draw anything that has the methods

            1. bounding_box
            2. tikz_code

        The first one should return a bounding box and the second one should return a valid tikz code as string.

        NOTE:

        More precisely, it does not draw the object now, but it add it (and its mark if applicable) to ``self.record_draw_graph`` which is the list of objects to be drawn. Thus it is still possible to modify the object later (even if extremely discouraged).
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

        # If an object has a mark, it the latter is already in the 'added_objects' list and the mark is already passed to a DrawGraph.
        # Adding here the mark to the "record_draw_graph" list make pass twice by the computation of its bounding box (and draw it twice)
        # Augustus 8, 2016
        # See position 3598-30738

        self.math_BB.append(graph,self)
        graph._draw_added_objects(self)
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
        self.DrawGraphs(self.grid)
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
