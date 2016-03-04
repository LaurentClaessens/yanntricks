#! /usr/bin/python3
# -*- coding: utf8 -*-

import os
import shutil

HOME=os.path.expanduser("~")

import configuration

class OnePicture(object):
    latex_skel="""
    \lstinputlisting{CODE_FILENAME}

    \\newcommand{\CaptionFigNAME}{<+Type your caption here+>}
    \\begin{center}
        \input{Fig_NAME.pstricks}
    \end{center}

    COMMENT

    \\clearpage
    """
    # The following files have some particularities (like having two different functions inside) and will not
    # be included in the 'all' document.
    not_to_be_done=configuration.not_to_be_done

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
        comment=""
        try:
            comment="Comment : "+open(self.comment_filename).read()
        except FileNotFoundError:
            print("Pas de commentaires pour "+self.comment_filename)
        return self.latex_skel.replace("CODE_FILENAME",self.filename).replace("NAME",self.function_name).replace("COMMENT",comment)
    def isToDo(self):
        return (self.function_name not in self.not_to_be_done)


def getFromDirectory(_dirname):
    """
    Argument : 
        - the directory name of a document that uses 'phystricks' with a right naming convention.
    Return
        - a tuple of string (import,function_append)
    """
    dirname=os.path.expanduser(_dirname)
    import_list=[]
    function_append_list=[]
    latex_code_list=[]
    for f in os.listdir(dirname):
        if f.startswith("phystricks") and f.endswith(".py"):
            pict=OnePicture(f,_dirname)
            if pict.isToDo():

                import_list.append(pict.importLine())
                function_append_list.append(pict.functionAppendLine())
                latex_code_list.append(pict.latex())

                shutil.copyfile(pict.real_origin_path,pict.real_here_path)

    return ("\n".join(import_list)+"\n","\n".join(function_append_list)+"\n","\n".join(latex_code_list))

import_string=""
function_append_string=""
latex=""

for d in configuration.document_directories :
    imp,fun,lat=getFromDirectory(d)
    import_string+=imp
    function_append_string+=fun
    latex+=lat


skel=open("figures_testing_skel.py",'r').read()
code_all=skel.replace("IMPORT_LIST",import_string).replace("APPEND_LIST",function_append_string)
file_all=open("figures_testing.py",'w')
file_all.write(code_all)
file_all.close()

skel=open("skel_pack.tex").read()
code_latex=skel.replace("LATEX_CODE",latex)
file_all=open("pack.tex",'w')
file_all.write(code_latex)
file_all.close()
