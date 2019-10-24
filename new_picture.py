#!/usr/bin/python3

"""
Helper for the end-user.

- Create a skel of the sage script
- Create dummy pdf and md5 files
- Say what to 'git add'.
"""

import sys
import os
import random
import string

from yanntricks.src.paths_keeper import PathsKeeper


def via_random(alphabet, length):
    """Return a random string from the given alphabet."""
    answer = ""
    for _ in range(0, length):
        answer += random.choice(alphabet)
    return answer


def get_code_skel():
    """Return a skeleton of file to be filled by the user."""
    return open("code_base.skel", 'r').read()


def create_file(filename, text):
    """Write a text in the given file if it does not exist."""
    if not os.path.isfile(filename.abspath()):
        with open(filename.abspath(), "w") as my_file:
            my_file.write(text)
    else:
        print(f"Le fichier {filename} existe déjà. Je ne fais rien")


def do_work():
    """Make the work."""
    try:
        figure_name = sys.argv[1]
    except IndexError:
        rand1 = via_random(string.ascii_uppercase, 4)
        rand2 = via_random(string.ascii_letters, 8)
        figure_name = rand1 + "oo" + rand2

    forbidden_symb = ["_", "1", "2", "3", "4", "5", "6",
                      "7", "8", "9", "0"]

    for char in forbidden_symb:
        if char in figure_name:
            raise ValueError(f"You should not use '{char}' in the name.")

        code_skel = get_code_skel().replace("XXXX", figure_name)

    paths_keeper = PathsKeeper()

    filename = paths_keeper.create("pictures_src",
                                   f"yanntricks{figure_name}.py")

    pstricksfilename = paths_keeper.create("pictures_tex",
                                           f"Fig_{figure_name}.pstricks")

    pdffilename = paths_keeper.create(
        "pictures_tikz",
        f"tikzFIGLabelFig{figure_name}PICT{figure_name}.pdf")

    md5filename = paths_keeper.create(
        "pictures_tikz",
        f"tikzFIGLabelFig{figure_name}PICT{figure_name}")

    for prod_file in [filename, pstricksfilename, pdffilename]:
        create_file(prod_file, code_skel)

    create_file(md5filename, "")

    print(f"from yanntricks{figure_name} import {figure_name}")
    print(f"git add {filename.from_sage()} "
          f"{pstricksfilename.from_sage} "
          f"{pdffilename.from_sage()} "
          f"{md5filename.from_sage()}")
    print(f"attach('{filename.from_sage()}'); "
          f"{figure_name}();exit()")


do_work()
