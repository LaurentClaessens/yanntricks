# All the examples for phystricks


This is a big document containing (more or less) all the pictures I designed with phystricks. This is a direct sum of the pictures in [mazhe](https://github.com/LaurentClaessens/mazhe) and [smath](https://github.com/LaurentClaessens/smath)


### Hypothesis

The script `create_all.py` relies on some naming conventions :

* the phystricks filename has the form `phystricksSOMETHING.py`
* the function inside is named `SOMETHING`.
* `SOMETHING` does not contain `.py` or `phystricks`
* Each file contains only one picture that has the same name as the function (I do exclude the files that create two pictures at once).

In fact, I always create my pictures using an automatic script that choose the function name as a random sequence of ten ASCII letters.

### Testing

rm *.pyc && rm phystricks*.py && rm *.pstricks&& rm *.comment&& rm LabelFig*.aux

./create_testing.py
time ./figures_testing.py --all


### Make your big document

Create your `documentation.py` module defining the following lists :

* document_directories.  The list of directories in which you have pictures.
* not_to_be_done. The list of function names that have not to be testes.

### Bulding the documentation with sphynx

Launch a shell with Sage's configuration files :

    $ sage -sh
the, inside :

    $ make html

