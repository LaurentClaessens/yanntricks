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

# copyright (c) Laurent Claessens, 2016-2017, 2019
# email: laurent@claessens-donadello.eu

# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-instance-attributes

"""
Describe an auxiliary file in which we make LaTeX write some informations.
"""

from yanntricks.src.Utilities import newlengthName
from yanntricks.src.NoMathUtilities import logging
from yanntricks.src.paths_keeper import PathsKeeper
from yanntricks.src.NoMathUtilities import text_to_hexdigest


class AuxFile:
    """
    The auxiliary file serves to make a 'dialog' between LaTeX
    and yanntricks.
    We ask LaTeX to write the box sizes therein.

    Each `Picture` has an auxiliary file.
    """

    def __init__(self, name, picture):
        self.paths = PathsKeeper()
        self.name = name
        self.picture = picture
        self.newwriteName = "writeOfyanntricks"
        self.interWriteFile = self.paths.create(
            "main_tex",
            f"{self.name}.yanntricks.aux")

        self._latex_line_list = []
        self.already_used_interId = []
        self.already_warned_CompileYourLaTeXFile = False

        # Able to retrieve the tex expression from the hash. See 2576-2197
        # Be careful : this dictionary stores 'unicode' objects as values,
        # while hashlib wants 'str' and some functions are passing 'str'.
        self.interId_to_tex_expression = {}

    def CounterId(self, counter_name):
        return f"Counter{self.name}{counter_name}"

    def open_latex_code(self):
        a = []
        code = r"""\ifthenelse{\isundefined{\NWN}}{\newwrite{\NWN}}{}""".replace(
            "NWN", self.newwriteName)
        a.append(code)
        code = r"""\ifthenelse{\isundefined{\NLN}}{\newlength{\NLN}}{}"""
        code = code.replace("NLN", newlengthName())
        a.append(code)
        code = r"\immediate\openout\AAA=BBB%"
        code = code.replace("AAA", self.newwriteName)
        code = code.replace("BBB", str(self.interWriteFile.from_main()))
        a.append(code)
        return "\n".join(a)

    def close_latex_code(self):
        code = r"\immediate\closeout\{}%".format(self.newwriteName)+"\n"
        return code

    def latex_code(self):
        return "\n".join(self._latex_line_list)

    def add_latex_line(self, line):
        self._latex_line_list.append(line)

    def makeWriteValue(self, Id, value):
        r""" Make LaTeX write `value` in the auxiliary file.

        Ask LaTeX to write the result of `value` into
        the standard auxiliary file with identifier `Id`

        @param{str} `Id`
            Some string that identifies what we will
            write (for reading the file later). Preferably ASCII string.

        @param{str} `value`
            A LaTeX code that returns something; that something
            will be written. Typically this is a string
            like `\arabic{\thesection}`
        """
        self.add_latex_line(
            r"\immediate\write\{}{{{}:{}-}}".format(self.newwriteName, Id, value))

    def id_values_dict(self):
        """
        Build the dictionary of stored values in the auxiliary file
        and rewrite that file.
        """
        d = {}
        try:
            f = open(self.interWriteFile.from_sage(), "r")
        except IOError:
            if not self.already_warned_CompileYourLaTeXFile:
                logging(f"Warning: the auxiliary file "
                        f"{self.interWriteFile.from_main()} does not "
                        f"seem to exist. Compile your LaTeX file.",
                        pspict=self.picture)
                self.already_warned_CompileYourLaTeXFile = True
            return d
        idlist = f.read().replace('\n', '').replace(
            ' ', '').replace('\\par', '').split("-")
        f.close()

        for els in idlist[0:-1]:
            key = els.split(":")[0]
            value = els.split(':')[1]
            d[key] = value

        with open(self.interWriteFile.from_sage(), "w") as f:
            for k in d:
                f.write("%s:%s-\n" % (k, d[k]))

        return d

    def get_Id_value(self, Id, default_value=0):
        if Id not in self.id_values_dict():

            if not self.already_warned_CompileYourLaTeXFile:
                logging(self.picture.name+"-----")
                logging(f"Warning: the auxiliary file "
                        f"{self.interWriteFile.from_main()} does not "
                        f"contain the id «{Id}». Compile your LaTeX file.",
                        pspict=self.picture)
                try:
                    logging("Concerned tex expression : "
                            f"{self.interId_to_tex_expression[Id]}")
                except KeyError:
                    pass    # when asking for a counter, not a box size.

                self.already_warned_CompileYourLaTeXFile = True
            return default_value
        value = self.id_values_dict()[Id]
        return value

    def get_counter_value(self, counter_name, default_value=0):
        """
        Return the value of the (LaTeX) counter <name>.

        Makes LaTeX write the value of the counter in an auxiliary file,
        then reads the value in that file.
        (needs several compilations to work)

        So we get the value at this point of the LaTeX file.

        If you ask for the page with for example
        ```
        page = pspict.get_counter_value("page")
        ```
        the given page will be the one at which LaTeX thinks the figure lies.
        Since a figure is a floating object, if you have many of them in a row,
        the page number could be incorrect.
        """
        interCounterId = self.CounterId(counter_name)
        s = r"\arabic{%s}" % counter_name
        self.makeWriteValue(interCounterId, s)

        # Read the file and return the value
        ans = self.get_Id_value(interCounterId, default_value)
        return float(ans)

    def get_box_dimension(self, tex_expression, dimension_name, default_value="0pt"):
        """
        Return the dimension of the LaTeX box corresponding to the LaTeX
        expression `tex_expression`.

        dimension_name is a valid LaTeX macro that can be applied to
        a LaTeX expression and that return a number. Like
        widthof, depthof, heightof, totalheightof
        """
        hexdigest = text_to_hexdigest(tex_expression)

        interId = dimension_name+hexdigest

        # 2576-2197
        self.interId_to_tex_expression[interId] = tex_expression
        if interId not in self.already_used_interId:
            s = r"\setlength{\AAA}{\BBB{CCC}}%"
            s = s.replace("AAA", newlengthName())
            s = s.replace("BBB", dimension_name)
            s = s.replace("CCC", tex_expression)
            self.add_latex_line(s)
            value = r"\the\{}".format(newlengthName())

            self.add_latex_line(
                r"\immediate\write\{}{{{}:{}-}}".format(self.newwriteName, interId, value))

            self.already_used_interId.append(interId)
        read_value = self.get_Id_value(interId, default_value=default_value)
        dimenPT = float(read_value.replace("pt", ""))
        # 30 is the conversion factor : 1pt=(1/3)mm
        return (dimenPT)/30

    def get_box_size(self, tex_expression, default_value="0pt"):
        r"""
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
        height = self.get_box_dimension(
            tex_expression, "totalheightof", default_value=default_value)
        width = self.get_box_dimension(
            tex_expression, "widthof", default_value=default_value)
        return width, height
