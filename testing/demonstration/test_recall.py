#! /usr/bin/python3
# -*- coding: utf8 -*-


# This script compares the files "*.pstricks" with the corresponding one 
# "*.pstricks.recall" and prints a warning if they are not equal (up to 
# numerical acceptation)

import os

def pstricks_files_iterator():
    for f in os.listdir():
        if f.endswith(".pstricks"):
            yield f

def text_to_skel(text):
    start=text.find("\\begin{tikzpicture}")
    end=text.find("\\end{tikzpicture}")
    text=text[start:end]

    skel=""

    op = text.find("(")
    cp = text.find(")")
    while op != -1 :
        if cp < op :
            print("There is a closing before an opening. Strange.")
            raise
        skel=skel+text[:op]
        text=text[cp+1:]
        op = text.find("(")
        cp = text.find(")")
    print(skel)

        
    


for filename in pstricks_files_iterator():
    print("Working on "+filename)
    with open(filename,'r') as f:
        text=f.read()
        text_to_skel(text)


