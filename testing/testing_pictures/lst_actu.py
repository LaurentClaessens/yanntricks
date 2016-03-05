#! /usr/bin/python
# -*- coding: utf8 -*-

from __future__ import unicode_literals

import LaTeXparser
import LaTeXparser.PytexTools
import plugins_agreg

myRequest = LaTeXparser.PytexTools.Request("mesure")

myRequest.add_plugin(plugins_agreg.set_isAgreg,"before_pytex")

myRequest.original_filename="testing.tex"

myRequest.ok_filenames_list=["e_testing"]
myRequest.ok_filenames_list.extend(["testing_body"])
myRequest.ok_filenames_list.extend(["<++>"])


myRequest.new_output_filename="0-actu.pdf"
