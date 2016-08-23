# PHYSTRICKS -- DOCUMENTATION

This is the documentation for `phystricks`. 

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


