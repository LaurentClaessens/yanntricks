# docu

Deals with the documentation.

# debug

There are two non working test pictures. We are dealing with them here.

The problem is that for some reason the computation of the bounding box of the axes
is non deterministic.

# passes

In `figures_demo`, create three lists of figures instead of one.

- The first one contains all of them
- The second one contains only the pictures which need two compilation passes
- The third one contains only the pictures which need three compilation passes

Then the script `testing.sh` will launch `figures_demo` three times with 
a parameter indicating the list to be used.
The aim is to compile each picture only the right number of time. This should reduce the 
test duration.

# minmax

Make less use of the Sages'function `get_minmax_data` which leads to indeterministic results.

# newTests

Add to the test suite the pictures that do not compile in mazhe and smath.

# devel

The development branch.

# newTests

Create tests to catch the picture OMPA.

# deprecation

remove the deprecation warnings.

#prepa3

Take into account (some advices)[http://python3porting.com/preparing.html] to prepare a switch to python3.

# remove_al_bb

Remove the attribute 'already_computed_bb' of Picture.

If the picture itself keeps a list of already computed bounging boxes, the test
```
if ob in picture.already_computed_bb :
    pass
```
causes a serie of comparisons `ob==x` for x in picture.already_computed_bb. Sometimes, these comparisons crashes or are difficult.

So each object will keep its own list of bounding boxes.

# debug

Debugging some pictures that do not work anymore since the last change.

#remove_bloat

Remove some useless code : 
- the old "test" functionality that compares files "up to epsilon" in the numbers
- the class File
- the references to dvi, eps and so on.
