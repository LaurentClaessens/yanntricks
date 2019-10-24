"""PathsKeeper is a class which keeps the filesnames conventions."""

import importlib.util
from pathlib import Path

from yanntricks.src.relative_file import RelativeFile


dprint = print  #pylint: disable=invalid-name


class PathsKeeper:
    """
    An object of this class keeps the paths.

    If the file "Directories.py" exists, read the directories in
    which the tex files have to be put.
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
        """
        Provide some defaults paths, or read in `Directory.py`.
        """
        self["main_tex"] = Path('.')
        self["pictures_tizk"] = Path('.')
        self["pictures_tex"] = Path('.')
        self["sage_dir"] = Path('.')
        try:
            spec = importlib.util.spec_from_file_location(
                "Directories", "Directories.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except FileNotFoundError:
            # In this case we are left with the defaults
            return

        self["pictures_tex"] = module.PICTURES_TEX
        self["pictures_src"] = module.PICTURES_SRC
        self["pictures_tikz"] = module.PICTURES_TIKZ
        self["main_tex"] = module.MAIN_TEX
        self["sage_dir"] = module.SAGE_DIR

    def create(self, key, path):
        """Return the `RelativeFile` corresponding to the given path."""
        abs_file = self[key] / path
        return RelativeFile(abs_file, self)

    def __setitem__(self, key, path):
        """
        Add a path to self's path dictionary.

        The path is resolved.
        """
        abs_path = Path('.') / path
        if not abs_path.exists():
            raise ValueError(f"The directory {abs_path} does not exist.")
        self.paths[key] = Path(path).resolve()

    def __getitem__(self, key):
        """Return the saved path under the given key."""
        return self.paths[key]
