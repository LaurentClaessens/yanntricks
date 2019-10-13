

class DrawElement:
    """
    The attributes take_xxx are intended to say what we
    have to take into account in the element.
    If you put take_graph=False, this element will not be
    drawn, but its bounding boxes are going to be taken into account.
    """
    def __init__(self, graphe, separator_name, 
                 take_graph=True, 
                 take_BB=True, 
                 take_math_BB=True, *args):
        self.take_graph = take_graph
        self.take_BB = take_BB
        self.take_math_BB = take_math_BB
        self.graph = graphe
        self.separator_name = separator_name
        self.st_args = args
