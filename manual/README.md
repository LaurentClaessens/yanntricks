# PHYSTRICKS -- DOCUMENTATION

This is the documentation for `phystricks`. You can download a PDF [here](http://laurent.claessens-donadello.eu/pdf/phystricks-doc.pdf)

## Compilation

First clean up the directory :
```bash
rm *.pyc && rm *.pstricks&& rm *.comment&& rm LabelFig*.aux && rm tikzFIGLabel*
```

Compile the documentation doing twice the following :
```bash
time ./figure_manual.py
pytex lst_documentation.py --all --no-external
```


