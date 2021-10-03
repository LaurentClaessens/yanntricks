# The demonstrative pictures

This document is only for testing and demonstration purpose. 


## Add a new picture

Create a new file like this one:
```
from yanntricks import *
def FIPLooZoxgfT():
    pspict,fig = SinglePicture("FIPLooZoxgfT")

    A = Point(3, 4)

    pspict.DrawGraphs(A)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
```

Add it to `figures_demo.py`.

In a sage terminal:
```
attach("yanntricksFIPLooZoxgfT.py");FIPLooZoxgfT()
```

Add the given LaTeX code in `demo.tex`.



## Compiling using [*pytex*](https://github.com/LaurentClaessens/pytex)


Clean the directory :
```bash
rm *.pyc &  rm *.pstricks & rm *.comment & rm FIGLabelFig*.aux
```

Launch twice the following commands.
```bash
./figures_demo.py --all
pytex lst_demo.py --no-external --all
```
The program `pytex` makes the patching for you.

## Compiling *a mano*

* Create the pictures :
    ```bash
    ./figures_demo.py --all
    ```
* Patch `demo.tex` in order to have the counter `useexternal` equals zero.
* Launch `pdflatex` on `demo.tex` with `-shell-escape`
