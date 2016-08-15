# The demonstrative pictures

This document is only for testing and demonstration purpose. 

## Compiling using [*pytex*](https://github.com/LaurentClaessens/pytex)


Clean the directory :
```bash
rm *.pyc &&  rm *.pstricks&& rm *.comment&& rm LabelFig*.aux
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

