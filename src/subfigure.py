

class SubFigure(object):
    """
    This is a subfigure.

    If no label are given, a default one will be set when included in the figure.

    EXAMPLES

    .. literalinclude:: phystricksSubFigure.py
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigFirstPICTFirstPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigSecondPICTSecondPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigThirdPICTthirdPoint-for_eps.png
    """

    def __init__(self, caption, name=None):
        self.caption = caption
        self.name = name
        self.record_pspicture = []
        self.mother = None

    def add_latex_line(self, ligne, separator_name):
        self.mother.add_latex_line(ligne, separator_name)

    def new_pspicture(self, name=None, pspict=None):
        if name == None:
            number = len(self.record_pspicture)
            name = "sub"+latinize(str(number))
        if pspict is None:
            pspict = Picture("FIG"+self.name+"PICT"+name)
        pspict.mother = self
        # The mother of a pspict inside a subfigure is the figure (not the subfigure)
        pspict.figure_mother = self.mother
        pspict.subfigure_mother = self
        self.add_pspicture(pspict)
        return pspict

    def subfigure_code(self):
        a = []
        for pspict in self.record_pspicture:
            a.append(pspict.latex_code())
        return "\n".join(a)

    def add_pspicture(self, pspicture):
        self.record_pspicture.append(pspicture)
