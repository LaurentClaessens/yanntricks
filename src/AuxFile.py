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

# copyright (c) Laurent Claessens, 2016-2017
# email: laurent@claessens-donadello.eu

from Utilities import newlengthName
from NoMathUtilities import logging
from NoMathUtilities import ensure_unicode
from NoMathUtilities import SubdirectoryFilenames

## \brief Creates a name for a counter in LaTeX
# 
# Suppose you need to ask for the value of the counter `page`. What you do is
# ```
# page=pspict.auxiliary_file.get_counter_value("page")
# ```
# What `phystricks` do is to add such a line in the 'pstricks' file :
# ```
# \immediate\write\writeOfphystricks{_some_id_:\arabic{page}-}
# ```
# where `some_id` is what we furnish here. This is the identifiant which whose
# we are going to search for the answer in the dedicated `.aux` file.
#
# It has to be
# - different for each thing that we are going to write in the `.aux` file
# - deterministic because we are getting him back during a second pass of
#   `phustricks`.
class CounterId(object):
    counter={}
    def __call__(self,counter_name):
        try:
            return self.counter[counter_name]
        except KeyError :
            pass
        s="Counter"+counter_name
        self.counter[counter_name]=s
        return s

class AuxFile(object):
    """
    The auxiliary file serves to make a 'dialog' between LaTeX and phystricks. 
    We ask LaTeX to write the box sizes therein.

    Each `Picture` has an auxiliary file.
    """
    def __init__(self,name,picture):
        self.name=name
        self.picture=picture
        self.newwriteName = "writeOfphystricks"
        self.interWriteFile = SubdirectoryFilenames(self.name+".phystricks.aux",position="main")

        self._latex_line_list=[]
        self.already_used_interId=[]
        self.already_warned_CompileYourLaTeXFile=False

        # Able to retrieve the tex expression from the hash. See 2576-2197
        # Be careful : this dictionary stores 'unicode' objects as values,
        # while hashlib wants 'str' and some functions are passing 'str'.
        self.interId_to_tex_expression = {}     
    def open_latex_code(self):
        a=[]
        code = r"""\ifthenelse{\isundefined{\NWN}}{\newwrite{\NWN}}{}""".replace("NWN",self.newwriteName)
        a.append(code)
        code = r"""\ifthenelse{\isundefined{\NLN}}{\newlength{\NLN}}{}""".replace("NLN",newlengthName())
        a.append(code)
        code = "\immediate\openout\{}={}%".format(self.newwriteName,self.interWriteFile.from_main())
        a.append(code)
        return "\n".join(a)
    def close_latex_code(self):
        code=r"\immediate\closeout\{}%".format(self.newwriteName)+"\n"
        return code
    def latex_code(self):
        return "\n".join(self._latex_line_list)
    def add_latex_line(self,line):
        self._latex_line_list.append(line)
    def makeWriteValue(self,Id,value):
        r"""Ask LaTeX to write the result of `value` into the standard auxiliary file with identifier `Id`

            - `Id` some string that identifies what we will write (for reading the file later). Preferably ASCII string.

            - `value` a LaTeX code that returns something; that something will be written. Typically this is a string like 
                    \arabic{\thesection}
        """
        self.add_latex_line(r"\immediate\write\{}{{{}:{}-}}".format(self.newwriteName,Id,value))

    def id_values_dict(self):
        """
        Build the dictionary of stored values in the auxiliary file and rewrite that file.
        """
        d={}
        try :
            f=open(self.interWriteFile.from_here(),"r")
        except IOError :
            if not self.already_warned_CompileYourLaTeXFile:
                logging("Warning: the auxiliary file %s does not seem to exist. Compile your LaTeX file."%self.interWriteFile.from_main(),pspict=self.picture)
                self.already_warned_CompileYourLaTeXFile=True
            return d
        idlist = f.read().replace('\n','').replace(' ','').replace('\\par','').split("-")
        f.close()

        for els in idlist[0:-1]:
            key=els.split(":")[0]
            value=els.split(':')[1]
            d[key]=value

        f=open(self.interWriteFile.from_here(),"w")
        for k in d.iterkeys():
            f.write("%s:%s-\n"%(k,d[k]))
        f.close()
        return d
    def get_Id_value(self,Id,default_value=0):
        if Id not in self.id_values_dict().iterkeys():

            if not self.already_warned_CompileYourLaTeXFile:
                logging(self.picture.name+"-----")
                logging("Warning: the auxiliary file {} does not contain\
                        the id «{}». Compile your LaTeX file.".format(
                            self.interWriteFile.from_main(),Id),pspict=self.picture)
                try :
                    logging(u"Concerned tex expression : "+\
                                self.interId_to_tex_expression[Id])
                except KeyError:
                    pass    # when asking for a counter, not a box size.

                self.already_warned_CompileYourLaTeXFile=True
            return default_value
        value = self.id_values_dict()[Id]
        return value


    ##   \brief return the value of the (LaTeX) counter <name>
    #    at this point of the LaTeX file.
    #
    # Makes LaTeX write the value of the counter in an auxiliary file,
    # then reads the value in that file.  (needs several compilations to work)
    #
    # \return a float.
    #
    #
    # If you ask for the page with for example
    # ```page = pspict.get_counter_value("page")```
    # the given page will be the one at which LaTeX thinks the figure lies. 
    # Since a figure is a floating object, if you have many of them in a row,
    # the page number could be incorrect.
    def get_counter_value(self,counter_name,default_value=0):
        # Make LaTeX write the value of the counter in a specific file
        interCounterId=CounterId()(counter_name)
        s=r"\arabic{%s}"%counter_name
        self.makeWriteValue(interCounterId,s)

        # Read the file and return the value
        ans = self.get_Id_value(interCounterId,default_value)
        return float(ans)

    def get_box_dimension(self,tex_expression,dimension_name,default_value="0pt"):
        """
        Return the dimension of the LaTeX box corresponding to the LaTeX
        expression `tex_expression`.

        dimension_name is a valid LaTeX macro that can be applied to
        a LaTeX expression and that return a number. Like
        widthof, depthof, heightof, totalheightof
        """
        from NoMathUtilities import text_to_hexdigest
        tex_expression=ensure_unicode(tex_expression)
        hexdigest=text_to_hexdigest(tex_expression)

        interId=dimension_name+hexdigest

        # 2576-2197
        self.interId_to_tex_expression[interId]=tex_expression
        if interId not in self.already_used_interId :
            self.add_latex_line(ur"\setlength{{\{}}}{{\{}{{{}}}}}%".format(newlengthName(),dimension_name,tex_expression))
            value=r"\the\{}".format(newlengthName())

            self.add_latex_line(r"\immediate\write\{}{{{}:{}-}}".format(self.newwriteName,interId,value))

            self.already_used_interId.append(interId)
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
