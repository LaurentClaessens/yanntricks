
from yanntricks.src.Figure import Figure
from yanntricks.src.Exceptions import PhystricksTestError
from yanntricks.src.Exceptions import PhystricksNoError
from yanntricks.src.main import function_list_to_figures_list

class FigureGenerationSuite:
    """
    Generate the figures of a list.

    INPUT:

    - ``test_list`` - a list of functions that are supposed to produce pspictures

    - ``first`` - the position in `test_list` at which we begin the tests

    ATTRIBUTES:

    - ``failed_list`` - a list of tuple `(function,pspict)` where 
                        `function` is a function that produced a 
                        :class:`PhystricksTestError` and
                        pspict is the produced pspicture.

    """

    def __init__(self, test_list, first=0, title="My beautiful document"):
        from yanntricks.src.Defaults import LOGGING_FILENAME
        self.test_list = test_list
        self.first = first
        self.title = title
        self.failed_list = []
        self.documentation_list = []
        self.to_be_recompiled_list = []
        open(LOGGING_FILENAME, "w").close()

    def generate(self):
        """Perform the tests."""
        Figure.send_noerror = True
        print("")
        print("********************************************")
        print("*  This is the automatic figure generation")
        print("*  for %s" % self.title)
        print("********************************************")
        print("")
        for i in range(self.first, len(self.test_list)):
            print("--------------------------- %s : figure %s/%s (failed: %s) -------------------------------------" %
                  (self.title, str(i+1), str(len(self.test_list)), str(len(self.failed_list))))
            print(" ============= %s =============" % str(self.test_list[i]))
            try:
                try:
                    self.test_list[i]()
                except PhystricksTestError as e:
                    print("The test of pspicture %s failed. %s" %
                          (self.test_list[i], e.justification))
                    print(e)
                    self.failed_list.append((self.test_list[i], e.pspict))
                    if e.code == 2:
                        self.to_be_recompiled_list.append(
                            (self.test_list[i], e.pspict))
            except PhystricksNoError as e:
                pass

    def summary(self):
        """
        Print the list of failed tests and try to give the 
        lines to be included in the LaTeX file in order to
        visualize them.
        """
        all_tests_passed = True
        if len(self.failed_list) != 0:
            print("The list of function to visually checked :")
            print(function_list_to_figures_list(self.failed_list))
            all_tests_passed = False
        if len(self.to_be_recompiled_list) != 0:
            print("The list of function to recompiled :")
            print(function_list_to_figures_list(
                self.to_be_recompiled_list))
            all_tests_passed = False
        if all_tests_passed:
            print("All tests passes !")
            from yanntricks.src.Defaults import LOGGING_FILENAME
            with open(LOGGING_FILENAME, "r") as f:
                for l in f:
                    print(l)
        else:
            raise PhystricksTestError
