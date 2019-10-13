###########################################################################
#   This is part of the module phystricks
#
#   phystricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   phystricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with phystricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu


class Options(object):
    """
    Describe the drawing options of an objects.

    ATTRIBUTES :
        self.DicoOptions : dictionnary which contains the options
    METHODS :
        self.merge_options(opt) : opt is an other object of the class Options. The method merges the two in the sense that opt is not
                        changed, but 
                        1. if opt contains a key more, it is added to self
                        2. if a key of opt is different of the one of self, self is changed
    """

    def __init__(self):
        self.DicoOptions = {}
    # One adds an option using for example
    # LineColor=blue,LineStyle=dashed
    # or via a dictionary :
    # {"Dx":1,"Dy":3}

    def add_option(self, opt):
        if opt:            # If the argument is empty.
            try:
                for op in opt.split(","):
                    s = op.split("=")
                    self.DicoOptions[s[0]] = s[1]
            except AttributeError:
                for op in opt:      # iterate over the keys
                    self.DicoOptions[op] = opt[op]

    def remove_option(self, opt):
        del(self.DicoOptions[opt])

    def merge_options(self, opt):
        for op in opt.DicoOptions:
            self.add_option({op: opt[op]})

    def extend_options(self, Opt):
        for opt in Opt.DicoOptions:
            self.add_option(opt+"="+Opt.DicoOptions[opt])
    # Afiter est une liste de noms d'options, et cette méthode retourne une instance de Options qui a juste ces options-là, avec les valeurs de self.

    def sousOptions(self, AFiter):
        O = Options()
        for op in self.DicoOptions:
            if op in AFiter:
                O.add_option(op+"="+self.DicoOptions[op])
        return O

    def style_ligne(self):
        return self.sousOptions(OptionsStyleLigne())

    def code(self, language=None):
        a = []
        if language == "tikz":
            a = []
            for at in ["linecolor", "linestyle"]:
                k = self.DicoOptions[at]
                if k and k != "none":
                    a.append(k)
            return ",".join(a)

    def __getitem__(self, opt):
        return self.DicoOptions[opt]
