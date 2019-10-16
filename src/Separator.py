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

# copyright (c) Laurent Claessens, 2009-2016, 2019
# email: laurent@claessens-donadello.eu


dprint = print


class Separator(object):
    def __init__(self, title):
        self.title = title
        self.latex_code = []
        self.add_latex_line("%"+self.title)

    def add_latex_line(self, line, add_line_jump=True):
        if isinstance(line, Separator):
            text = line.code()
        else:
            text = "".join(line)
        self.latex_code.append(text)
        if add_line_jump:
            self.latex_code.append(u"\n")

    def code(self):
        lc = self.latex_code
        return "".join(lc)
