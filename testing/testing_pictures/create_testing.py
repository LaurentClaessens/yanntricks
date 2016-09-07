#! /usr/bin/python3
# -*- coding: utf8 -*-

import os
import shutil

HOME=os.path.expanduser("~")

import configuration

class OnePicture(object):
    latex_skel="""
    %\lstinputlisting{CODE_FILENAME}

    \\newcommand{\CaptionFigPICTURE_NAME}{This is an automatically generated default caption; do not change.}
    \\begin{center}
        \input{Fig_PICTURE_NAME.pstricks}
    \end{center}
    FILE_NAME

    COMMENT

    \\clearpage
    """
    # The following files have some particularities (like having two different functions inside) and will not
    # be included in the 'all' document.

    def __init__(self,f,dirname):
        self.filename=f
        self.module_name=os.path.splitext(f)[0]
        self.real_origin_path=os.path.expanduser(os.path.join(dirname,f))
        self.real_here_path=os.path.realpath(f)
        self.function_name=f.replace("phystricks","").replace(".py","")
        self.comment_filename="Fig_"+self.function_name+".comment"
    def importLine(self):
        return "from "+self.module_name+" import "+self.function_name
    def functionAppendLine(self):
        return "figures_list.append("+self.function_name+")"
    def latex(self):
        comment_input=r"""\input{FN}""".replace("FN",self.comment_filename)
        return self.latex_skel.replace("CODE_FILENAME",self.filename).replace("PICTURE_NAME",self.function_name).replace("COMMENT",comment_input).replace("FILE_NAME",self.filename)
    def isToDo(self):
        return (self.function_name not in configuration.not_to_be_done)

def getFromDirectory(_dirname):
    """
    Argument : 
        - the directory name of a document that uses 'phystricks' with a right naming convention.
    """

    dirname=os.path.expanduser(_dirname)
    selected=[]
    for f in os.listdir(dirname):
        if f.startswith("phystricks") and f.endswith(".py"):
            selected.append( OnePicture(f,_dirname)  )
    return selected

def analyseSelected(selected):
    """
    Return
        - a tuple of string (import,function_append)
    """
    import_list=[]
    function_append_list=[]
    latex_code_list=[]
    for pict in selected:
        if pict.isToDo():
            import_list.append(pict.importLine())
            function_append_list.append(pict.functionAppendLine())
            latex_code_list.append(pict.latex())

            shutil.copyfile(pict.real_origin_path,pict.real_here_path)
            configuration.not_to_be_done.append(pict.function_name)             # avoid doublon.

    return ("\n".join(import_list)+"\n","\n".join(function_append_list)+"\n","\n".join(latex_code_list))

import_string=""
function_append_string=""
latex=""

selected=[]
for d in configuration.document_directories :
    selected.extend(getFromDirectory(d))

selected=selected[:]
import_string,function_append_string,latex=analyseSelected(selected)


skel=open("figures_testing_skel.py",'r').read()
code_all=skel.replace("IMPORT_LIST",import_string).replace("APPEND_LIST",function_append_string)
file_all=open("figures_testing.py",'w')
file_all.write(code_all)
file_all.close()

skel=open("testing_body-skel.tex").read()
code_latex=skel.replace("LATEX_CODE",latex)
file_all=open("testing_body.tex",'w')
file_all.write(code_latex)
file_all.close()
