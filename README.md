# phystricks : use python to create your pictures to be inserted in LaTeX

## General introduction

The purpose of this module is to produce pictures to be inserted in your LaTeX document using only python and [Sage](http://sagemath.org) techniques. The motto is :

«*if Sage can compute it, LaTeX can draw it*» 


### What problem do we solve ?

Including complex figures in LaTeX is always difficult because you 

* want use an external program because LaTeX as "programming language" is by far too complicated,
* want add labels that contains mathematical formulas; and these labels should be compiled by LaTeX, not by your external program,
* for some reasons, don't (want to) know ps stuff like psfrag.

### How do we solve ?

*phystricks* is a python (Sage in fact) module defining classes like point, segment, parametric curve, ... and many geometric relations between them. You describe your picture using Python and *phystricks* creates the `tikz` code to be included in your LaTeX file.



```python
# -*- coding: utf8 -*-
from phystricks import *
def TRJEooPRoLnEiG():
    pspict,fig = SinglePicture("TRJEooPRoLnEiG")
    pspict.dilatation(1)

    O=Point(0,0)

    circle=Circle( O,2  )
    tg=circle.get_tangent_vector(30)
    A=circle.get_point(130)
    B=circle.get_point(220)

    textA="$ \lim_{s} (F\circ\gamma')  $"
    textB="$ K $"
    A.put_mark(dist=0.3,angle=None,text=textA,automatic_place=(pspict,""))
    B.put_mark(dist=0.3,angle=None,text=textB,automatic_place=(pspict,""))

    pspict.DrawGraphs(circle,A,tg,B)

    pspict.comment="A circle with a point and a mark : "+textA+" and on other point with the mark "+textB

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
```


<img src="pictures/example1.png" alt="Drawing" style="width: 100px;"/>

![Alt text](pictures/example1.png)

![Alt text](pictures/example1.png =250x)






### Create your own picture

In order to be tested, the naming scheme is quite rigid. Do whatever you want, but the script `new_picture.py` will pick a random name and create all the skeleton files you need.

