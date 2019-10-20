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


#pylint: disable=invalid-name
#pylint: disable=missing-function-docstring
#pylint: disable=missing-module-docstring
#pylint: disable=too-many-arguments
#pylint: disable=fixme


from yanntricks.src.latex_to_be import pseudo_caption


# TODO : f=phyFunction(x**2+3*x-10), then  g=f/3 does not work.
# TODO : In figureHYeBZVj, the grid begins at negative numbers.
#        Why ? (see smath)
# TODO : waving functions behaves badly when X and Y
#        dilatations are different. See figureHYeBZVj


def latex_portion(failed_list, lstinputlisting=False):
    portion = []
    num = 0
    for a in failed_list:
        try:
            base = a[1].figure_mother.LaTeX_lines()
        except AttributeError as e:
            try:
                # In the case we are arriving here to
                # create the documentation.
                base = a[1].LaTeX_lines()
            except AttributeError as e:
                print(
                    "I cannot found the LaTeX lines corresponding to ", a[1])
                print(e)
        else:
            text = base.replace(pseudo_caption, str(a[0]))
            portion.append(text)
            if lstinputlisting:
                filename = "yanntricks"+str(a[1].script_filename)
                portion.append(r"\lstinputlisting{"+filename+".py}")
                portion.append(r"\clearpage")
            num = num+1
            if num == 5:
                portion.append(r"\clearpage\n")
                num = 0
    return "\n".join(portion)



def no_symbol(*arg):
    for l in arg:
        try:
            for P in l:
                no_symbol(P)
        except TypeError:
            l.parameters.symbol = ""




def function_list_to_figures_list(function_list):
    first = ",".join([a[0].__name__ for a in function_list])
    return "figures_list=[{0}]".format(first.replace("'", " "))


def GenericFigure(nom, script_filename=None):
    """
    This function returns a figure with some default values.
    It creates coherent label, file name and prints the lines
    to be appended in the LaTeX file to include the figure.
    """
    if not script_filename:
        script_filename = nom
    # This is also hard-coded in the function main.figure.LaTeX_lines
    caption = r"\CaptionFig"+nom
    # The string "LabelFig" is hard-coded in the function main.figure.LaTeX_lines
    label = "LabelFig"+nom
    filename = "Fig_"+nom+".pstricks"

    from yanntricks.src.Figure import Figure
    fig = Figure(caption, label, filename, script_filename)
    fig.figure_mother = fig   # I'm not sure that this line is useful.
    print(fig.LaTeX_lines())
    return fig


def SinglePicture(name, script_filename=None):
    """ Return the tuple of pspicture and figure that one needs in 90% of the cases. """
    fig = GenericFigure(name, script_filename)
    pspict = fig.new_pspicture(name)
    fig.child_pspictures.append(pspict)
    return pspict, fig


def MultiplePictures(name, n=None, pspicts=None, script_filename=None):
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

        sage: from yanntricks import *
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
        script_filename = name
    fig = GenericFigure(name, script_filename)

    if n is not None:
        pspictures_list = []
        for i in range(n):
            subfigure = fig.new_subfigure(
                "name"+str(i), "LabelSubFig"+name+str(i))
            picture = subfigure.new_pspicture(name+"pspict"+str(i))
            picture.figure_mother = fig
            fig.child_pspictures.append(picture)
            pspictures_list.append(picture)

    if pspicts is not None:
        pspictures_list = []
        n = len(pspicts)
        for i, psp in enumerate(pspicts):
            subfigure = fig.new_subfigure(
                "name"+str(i), "LabelSubFig"+name+str(i))
            subfigure.new_pspicture(pspict=psp)
            psp.figure_mother = fig
            fig.child_pspictures.append(psp)
            pspictures_list.append(psp)

    return pspictures_list, fig


def IndependentPictures(name, n):
    """
    Return a tuple of a list of 'n' pspictures and 'n' figures.
    """
    pspicts = []
    figs = []
    from yanntricks.src.Utilities import latinize
    for i in range(0, n):
        # One has to latinize to be in grade of making subfigures :
        # if not one gets things like
        # \newcommand{\CaptionFigFoo1}{blahblah}
        # which does not work in LaTeX because of the "1"
        pspict, fig = SinglePicture(name+"oo"+latinize(str(i)))
        pspicts.append(pspict)
        figs.append(fig)
    return pspicts, figs


def SubsetFigures(old_pspicts, old_fig, l):
    r"""
    Return a subset of a figure with subfigures.

    If you've prepared a figure with 10 subfigure
    but at the end of the day, you change your mind and
    decide to remove the subfigure 3 and 8
    """
    name = old_fig.name
    script_filename = old_fig.script_filename
    fig = GenericFigure(name, script_filename)
    pspict = []
    for i in l:
        subfigure = fig.new_subfigure("name"+str(i), "LabelSubFig"+name+str(i))
        subfigure.add_pspicture(old_pspicts[i])
        old_pspicts[i].figure_mother = fig
        pspict.append(old_pspicts[i])
    return pspict, fig
