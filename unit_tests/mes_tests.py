#! /usr/bin/python3
# -*- coding: utf8 -*-

from __future__ import division
from __future__ import unicode_literals

import sys
import os
import shutil
import codecs

"""
Before to use this, you should
- rm *.png
- rm *.pdf
- rm Fig_*
- rm *.phystricks
- rm phystricks*

rm *.png&& rm *.pdf&& rm Fig_*&& rm *.phystricks &&rm phystricks*
cp ~/Documents_sources/Unif/mazhe/phystricksCommuns.py .

ATTENTION : il y a un bogue d'encodage au moment de créer le fichier de documentation. À tester sur une petite partie d'abord. (17 mars 2013)


./figures_tests.py --all --no-compilation --documentation
latex documentation.tex (several times)
./figures_tests.py --all --no-compilation --tests 

Pour regarder, virer les images qui fonctionnent, puis recréer les pdf :
./figures_tests.py --all --create-pdf
pytex lst_to_be_checked.py --all
Puis quand ça marche :
./figures_tests.py --no-compilation --create-tests --all
"""

class ImportItem(object):
    def __init__(self,dirname,module_name,fun_name):
        self.module_name=module_name
        self.fun_name=fun_name
        self.module_filename=os.path.join(dirname,module_name)+".py"
        self.from_import_statement = "from {0} import {1}".format(self.module_name,self.fun_name).replace("\n","")

def get_figures_list(module_filename):
    """
    module_filename is the full path to the module.
    """
    dirname=os.path.split(module_filename)[0]
    fromimport = []
    f=codecs.open(module_filename,encoding="utf8")
    for a in f:
        l=a.split(" ")
        if l[0]=="from" and l[2]=="import" and l[3] != "*" and l[1] != "phystricks":
            module_name=l[1]
            fun_name=l[3].replace("\n","")
            fromimport.append(ImportItem(dirname,module_name,fun_name))
    f.close()
    return fromimport

item_list=[]
item_list.extend(get_figures_list("/home/moky/Documents_sources/LaTeX/smath/figures_smath.py"))
item_list.extend(get_figures_list("/home/moky/Documents_sources/Unif/mazhe/figures_mazhe.py"))
item_list.extend(get_figures_list("/home/moky/Documents_sources/Unif/analyseCTU/figures_analyseCTU.py"))
item_list.extend(get_figures_list("/home/moky/Manuels/phystricks-doc/figures_doc.py"))  # Je le mets ici pour que InteractWithLaTeX ne soit pas en première page.

repeated=False
for i,item in enumerate(item_list):
    if item.fun_name in [x.fun_name for x in item_list[i+1:]]:
        print("==========")
        print(item.fun_name,"is repeated")
        for it in item_list :
            if it.fun_name==item.fun_name :
                print(it.module_filename)
        repeated = True

if repeated:
    raise

# copie des fichiers. Il ne faut pas le faire à chaque fois.
for item in item_list:
    shutil.copy(item.module_filename,".")

fromimport_statement="\n".join([item.from_import_statement for item in item_list])

#figures_list=",".join([item.fun_name for item in item_list ]).replace("\n","")
l=[]
for item in item_list:
    l.append("figures_list.append({})".format(item.fun_name))
figures_list="\n".join(l)

latex_list=[]
for item in item_list :
    latex_list.append("Et maintenant "+item.fun_name)
    latex_list.append("\\newcommand{{\CaptionFig{0}}}{{{0}}}".format(item.fun_name))
    latex_list.append("\\begin{center}")
    latex_list.append("\input{Fig_"+item.fun_name+".pstricks}")
    latex_list.append("\end{center}")
    latex_list.append("\clearpage")

latex_code="\n".join(latex_list)

code=codecs.open("figures_tests.skel",encoding="utf8").read()
code_py=code.replace("FROMIMPORT",fromimport_statement)
code_py=code_py.replace("FIGURES_LIST",figures_list)

print(code_py)

code=codecs.open("document_tests.skel",encoding="utf8").read()
code_tex=code.replace("FIGURE_LIST",latex_code)

print(code_tex)
