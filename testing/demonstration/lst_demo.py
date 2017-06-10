#! /usr/bin/python
# -*- coding: utf8 -*-

from __future__ import unicode_literals

import latexparser
import latexparser.PytexTools

myRequest = latexparser.PytexTools.Request("mesure")

myRequest.original_filename="demo.tex"

myRequest.ok_filenames_list=["e_pictures"]
myRequest.ok_filenames_list.extend(["1_demo"])
myRequest.ok_filenames_list.extend(["2_demo"])
myRequest.ok_filenames_list.extend(["3_demo"])
myRequest.ok_filenames_list.extend(["0_demo"])
myRequest.ok_filenames_list.extend(["<++>"])


myRequest.new_output_filename="0-demo.pdf"
