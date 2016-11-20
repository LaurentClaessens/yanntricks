#! /usr/bin/python
# -*- coding: utf8 -*-

from __future__ import unicode_literals

import latexparser
import latexparser.PytexTools
import plugins_agreg

myRequest = latexparser.PytexTools.Request("mesure")


myRequest.original_filename="testing.tex"

myRequest.ok_filenames_list=["e_testing"]
myRequest.ok_filenames_list.extend(["1_testing"])
myRequest.ok_filenames_list.extend(["<++>"])


myRequest.new_output_filename="0-actu.pdf"
