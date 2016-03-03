# The demonstrative pictures

This document is only for testing and demonstration purpose.

## Compiling *a mano*

* Create the pictures :
    ```bash
    ./figures_demo.py --all
    ```
* Patch `demo.tex` in order to have the counter `useexternal` equals zero.
* Launch `pdflatex` on `demo.tex` with `-shell-escape`


## Compiling using *pytex*

Launch twice the following commands.
```bash
./figures_demo.py --all
pytex lst_actu.py --no-external
```
The program `pytex` makes the patching for you.
