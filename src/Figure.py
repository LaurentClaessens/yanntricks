#########################################################################
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
#########################################################################

# copyright (c) Laurent Claessens, 2009-2017, 2019
# email: laurent@claessens-donadello.eu


# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=fixme


import os
import codecs

from sage.all import numerical_approx  # pylint:disable=import-error

from yanntricks.src.Picture import Picture
from yanntricks.src.subfigure import SubFigure
from yanntricks.src.Utilities import latinize
from yanntricks.src.latex_to_be import pseudo_caption
from yanntricks.src.Utilities import add_latex_line_entete
from yanntricks.src.Utilities import init_figure_separator_list
from yanntricks.src.NoMathUtilities import SubdirectoryFilenames
from yanntricks.src.Exceptions import PhystricksNoError


dprint = print


class Figure:
    r"""
    Describe a figure: the LaTeX figure with some more informations.

    This is not exactly the 'figure' in the LaTeX sense of the
    term since it also contains informations about bounding boxes.

    The method `figure.no_figure()` makes disappear the
    \begin{figure} ... \end{figure}. In this case the LaTeX code of
    the class figure contains the informations about the bounding boxes
    and a if/then for inclusion of pspicture or \includegraphics

    - `self.newwriteName`
            The name that will be given to LaTeX in
            ``\newwrite{...}``. This is not the name of the file
            in which the data is written.
    - `self.interWriteFile`
            The name of the file in which the data will be written.
    """

    def __init__(self, caption, name, filename, script_filename):
        self.script_filename = script_filename
        self.caption = caption
        self.name = name
        self.xunit = 1
        self.yunit = 1
        self.figure_environment = True
        self.code = []
        self.record_subfigure = []
        self.record_pspicture = []
        self.child_pspictures = []
        self.contenu = None
        self.rotation_angle = None

        self.send_noerror = False
        self.language = "tikz"

        self.specific_needs = ""
        # TODO : specific_needs should be a list of specific_need that is a class.
        # The idea is to leave to the user the control if the command has to be included in the file
        # which creates the png and in the "final" file independently.

        # Filenames
        # filename.from_here() is the filename of the produced file
        # given relatively to the current directory, that is
        # relatively to the directory where the picture source is.

        # filename.from_main() is the filename of the produced file
        # given relatively to the main latex directory, that is
        # relatively to where LaTeX will see it.

        self.filename = SubdirectoryFilenames(filename, "pictures_tex")

        # This intermediate file will contain the comment of the pspict(s) for the sake of tests.
        self.comment_filename = self.filename.from_here().replace(".pstricks", ".comment")

        # The order of declaration is important, because it
        # is recorded in the Separator.number attribute.
        # the separators 'BEFORE SUBFIGURE' and 'AFTER ALL' will not
        # be written in the case when self.figure_environment=False.

        self.separator_list = init_figure_separator_list()
        self.entete_position = "ENTETE FIGURE"

        # "AFTER ALL" is for caption and \end{figure}
        self.separator_list.new_separator("AFTER ALL")
        add_latex_line_entete(self)
        self.add_latex_line("\\begin{figure}[ht]", "BEFORE SUBFIGURES")
        self.add_latex_line(r"\centering", "BEFORE SUBFIGURES")

    def no_figure(self):
        self.figure_environment = False

    def rotation(self, angle):
        self.rotation_angle = angle

    def new_subfigure(self, caption, name=None):
        """
        Create a subfigure in the figure and return it.

        The end-user should use this instead of `_append_subfigure`.
        """
        if name is None:

            dprint("Je fais une sous-figure")
            number = len(self.record_subfigure)
            dprint(f"numéro {number}")
            name = "sub"+latinize(str(number))
            dprint(f"nom {name}")

        ssfig = SubFigure(caption, self.name+"ss"+name)
        ssfig.mother = self
        ssfig.figure_mother = self
        self._append_subfigure(ssfig)
        return ssfig

    def _append_subfigure(self, ssFig):
        self.record_subfigure.append(ssFig)
        suffixe = "ssFig"+str(len(self.record_subfigure))
        if not ssFig.name:
            ssFig.name = self.name+suffixe
        print(r"See also the subfigure \ref{%s}" % ssFig.name)

    def new_pspicture(self, name=None, pspict=None):
        if name is None:
            number = len(self.record_pspicture)
            name = "sub"+latinize(str(number))
        if pspict is None:
            pspict = Picture(name)

        pspict.figure_mother = self
        self._add_pspicture(pspict)
        return pspict

    def add_latex_line(self, ligne, separator_name="DEFAULT"):
        self.separator_list[separator_name].add_latex_line(ligne)

    def _add_pspicture(self, pspict):
        pspict.mother = self
        pspict.figure_mother = self
        self.record_pspicture.append(pspict)

    def comments(self):
        a = []
        for pspict in self.child_pspictures:
            comment = pspict.comment
            if comment != "":
                a.append("Comment : "+comment)
        return "\n".join(a)

    def LaTeX_lines(self):
        """
        Return the lines to be included in your LaTeX file.
        """
        a = []
        a.append(self.comments())
        if self.figure_environment:
            a.append(
                "The result is on figure \\ref{"+self.name+"}. % From file "+self.script_filename)
            # The pseudo_caption is changed to the function name later.
            a.append("\\newcommand{"+self.caption+"}{"+pseudo_caption+"}")
            a.append("\\input{%s}" % (self.filename.from_main()))
        else:
            text = r"""\\begin{center}
   INCLUSION
\end{center}""".replace("INCLUSION", "\\input{%s}" % (self.filename.from_main()))
            if len(self.record_pspicture) == 1:
                pspict = self.record_pspicture[0]
                # By the way, this is a reason why we cannot do this before to have
                visual_xsize = pspict.visual_xsize()
                # concluded the picture.
                text = text.replace("WIDTH", str(
                    numerical_approx(visual_xsize, digits=3))+"cm")
            a.append(text)
        text = "\n".join(a)
        return text

    def conclude(self):
        for pspict in self.record_pspicture:
            inter_file = pspict.auxiliary_file.interWriteFile.from_here()
            if not os.path.isfile(inter_file):
                with open(inter_file, "w") as f:
                    f.write("default:content-")

            pspict.add_latex_line(
                pspict.auxiliary_file.open_latex_code(), "OPEN_WRITE_AND_LABEL")
            self.add_latex_line(pspict.latex_code(), "PSPICTURE")

            # For the following big stuff, see the position 170321508
            def_length_tex = r"""                 \makeatletter
% If hatchspread is not defined, we define it
\ifthenelse{\value{defHatch}=0}{
\setcounter{defHatch}{1}
\newlength{\hatchspread}%
\newlength{\hatchthickness}%
}{}
               \makeatother               """

            def_pattern_tex = r"""               \makeatletter
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

            if pspict.language == "tikz":
                self.add_latex_line(def_length_tex, "HATCHING_COMMANDS")
                self.add_latex_line(def_pattern_tex, "HATCHING_COMMANDS")

        self.add_latex_line(self.specific_needs, "SPECIFIC_NEEDS")

        for f in self.record_subfigure:
            self.add_latex_line(r"\subfigure["+f.caption+"]{%", "SUBFIGURES")
            self.add_latex_line(f.subfigure_code(), "SUBFIGURES")
            self.add_latex_line(r"\label{%s}" % f.name, "SUBFIGURES")
            self.add_latex_line("}                  % Closing subfigure " +
                                str(self.record_subfigure.index(f)+1), "SUBFIGURES")
            self.add_latex_line("%", "SUBFIGURES")

            for pspict in f.record_pspicture:
                pspict.add_latex_line(
                    pspict.auxiliary_file.open_latex_code(), "OPEN_WRITE_AND_LABEL")
                pspict.add_latex_line(
                    pspict.auxiliary_file.latex_code(), "WRITE_AND_LABEL")
                pspict.add_latex_line(
                    pspict.auxiliary_file.close_latex_code(), "CLOSE_WRITE_AND_LABEL")

        after_all = r"""\caption{%s}\label{%s}
            \end{figure}
            """ % (self.caption, self.name)
        self.add_latex_line(after_all, "AFTER ALL")
        if self.figure_environment:
            self.contenu = self.separator_list.code().replace("\n\n", "\n")
        else:
            self.contenu = self.separator_list.code(
                not_to_be_used=["BEFORE SUBFIGURES", "AFTER ALL"]).replace("\n\n", "\n")

    def write_the_file(self):
        """
        Write the figure in the file.

        Do not write if we are testing.
        It also remove the tikz externalize file.
        """
        to_be_written = self.contenu              # self.contenu is created in self.conclude
        with codecs.open(self.filename.from_here(), "w", encoding="utf8") as f:
            f.write(to_be_written)
        print("--------------- For your LaTeX file ---------------")
        print(self.LaTeX_lines())
        print("---------------------------------------------------")
        # One only sends the "no error" signal
        # if we are performing a list of tests.

        with codecs.open(self.comment_filename, "w", encoding='utf8') as f:
            f.write(self.comments())

        if self.send_noerror:
            raise PhystricksNoError(self)
