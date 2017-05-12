# -*- coding: utf8 -*-

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

# copyright (c) Laurent Claessens, 2010-2017
# email: laurent@claessens-donadello.eu


class AddedObjects(object):
    def __init__(self):
        self.dico={}
        self.dico[None]=[]          # The None list is the list of objects associated with all the pspicts. See the __getitem__ method.
    def append(self,pspict,obj):
        if not isinstance(pspict,list):
            pspict=[pspict]
        for psp in pspict:
            if psp not in self.dico.iterkeys():
                self.dico[psp]=[]
            self.dico[psp].append(obj)
    def extend(self,pspict,objs):
        for ob in objs :
            self.append(pspict,ob)
    def fusion(self,other):
        """
        other is an other AddedObjects instance.
        """
        if self is other :
            raise
        for psp,objs in other.dico.items():
            self.extend(psp,objs)
    def __getitem__(self,pspict):
        if pspict in self.dico.iterkeys():
            a = self.dico[pspict]
            a.extend(self.dico[None])
            return a
        return self[None]

