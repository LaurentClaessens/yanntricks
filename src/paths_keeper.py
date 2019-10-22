"""
PathsKeeper is a class which keeps the filesnames conventions.
"""

import importlib.util
from pathlib import Path

class PathsKeeper(object):
    """
    An object of this class keeps the paths.

    If the file "Directories.py" exists, read the directories inwhich the 
    tex files have to be put.
    In all cases if the file "Directories.py" is not found,
    everything will return the unmodified filename.
    """

    def __init__(self):
        """
        Initialize with some defaults or what we find in `Defaults.py`.
        """
        self.paths = {}
        self.initialize()
    def initialize(self):
        self["main_tex"] = Path('.')
        self["pictures_tizk"] = Path('.')
        self["pictures_tex"] = Path('.')
        self["pictures_src"] = Path('.')
        try:
            spec = importlib.util.spec_from_file_location(
                "Directories", "Directories.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except FileNotFoundError:
            # In this case we are left with the defaults
            return

        self["pictures_tex"] = module.PICTURES_TEX
        self.["pictures_src"] = module.PICTURES_SRC
        self.["pictures_tikz"] = module.PICTURES_TIKZ
        self.["main_tex"] = module.MAIN_TEX

    def __setitem__(self, path):
        """
        Add a path to self's path dictionary.

        The path is resolved.
        """
        self.paths.append(Path(path).resolve())
    def __getitem__(self, key):
        return self.paths[key]
