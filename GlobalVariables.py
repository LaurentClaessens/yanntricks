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

import sys

class GlobalVariables(object):
    """
    Some global variables

    - ``perform_tests`` - (default=False) If True, perform the tests.

    The difference between `create_formats` and `exit_format` is that `create_format` says
    what files are going to be _produced_ while `exit_format` is the format that LaTeX will see.
    """
    def __init__(self):
        self.create_formats={"eps":False,"pdf":False,"png":False,"test":False}
        self.exit_format="png"
        self.create_formats["png"] = False
        self.perform_tests = False
        self.silent=False
        self.no_compilation=True
        self.create_documentation=False
    def special_exit(self):
        for sortie in self.create_formats.values():
            if sortie:
                return True
        return False

global_vars = GlobalVariables()
if "--silent" in sys.argv :
    global_vars.silent=True
if "--dvi" in sys.argv :
    global_vars.exit_format="pstricks"
    global_vars.create_formats["pdf"] = False
    global_vars.create_formats["png"] = False
if "--eps" in sys.argv :
    global_vars.exit_format="eps"
    global_vars.create_formats["eps"] = True
if "--png" in sys.argv :
    global_vars.create_formats["png"] = True
if "--create-png" in sys.argv :
    global_vars.create_formats["png"] = True
if "--create-pdf" in sys.argv :
    global_vars.create_formats["pdf"] = True
    global_vars.create_formats["png"] = False
    global_vars.exit_format="pdf"
if "--create-eps" in sys.argv :
    global_vars.create_formats["eps"] = True
if "--create-tests" in sys.argv :
    global_vars.create_formats["test"] = True
    global_vars.create_formats["pdf"] = False
if "--tests" in sys.argv :
    global_vars.perform_tests = True
    global_vars.create_formats["pdf"] = False
if "--no-compilation" in sys.argv:
    global_vars.no_compilation=True
    for k in [x for x in global_vars.create_formats.keys() if x!="test" ]:
        global_vars.create_formats[k]=False
if "--documentation" in sys.argv:
    global_vars.create_documentation=True
