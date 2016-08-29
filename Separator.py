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
