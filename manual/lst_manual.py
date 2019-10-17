#! /usr/bin/python
# -*- coding: utf8 -*-

from __future__ import unicode_literals

import latexparser
import latexparser.PytexTools

myRequest = latexparser.PytexTools.Request("mesure")

myRequest.original_filename="yanntricks-manual.tex"

myRequest.ok_filenames_list=["e_yanntricks-manual"]
myRequest.ok_filenames_list.extend(["1_preparation"])
myRequest.ok_filenames_list.extend(["0_tests"])
myRequest.ok_filenames_list.extend(["<++>"])


myRequest.new_output_filename="0-yanntricks-manual.pdf"
