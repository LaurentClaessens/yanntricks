#! /usr/bin/python
# -*- coding: utf8 -*-

from __future__ import unicode_literals

import LaTeXparser
import LaTeXparser.PytexTools

myRequest = LaTeXparser.PytexTools.Request("mesure")

myRequest.original_filename="demo.tex"

myRequest.ok_filenames_list=["e_pictures"]
myRequest.ok_filenames_list.extend(["2_functions"])
myRequest.ok_filenames_list.extend(["demo_body"])
myRequest.ok_filenames_list.extend(["<++>"])


myRequest.new_output_filename="0-demo.pdf"
