#! /usr/bin/python
# -*- coding: utf8 -*-

from __future__ import unicode_literals

import LaTeXparser
import LaTeXparser.PytexTools

myRequest = LaTeXparser.PytexTools.Request("mesure")

myRequest.original_filename="phystricks-doc.tex"

myRequest.ok_filenames_list=["e_phystricks-doc"]
myRequest.ok_filenames_list.extend(["1_preparation"])
myRequest.ok_filenames_list.extend(["<++>"])
myRequest.ok_filenames_list.extend(["<++>"])


myRequest.new_output_filename="0-phystricks-doc.pdf"
