"""
Wrapper around a file path for LaTex.

The problem is that we have to write some paths in the aux file,
and in the tikz files.
These paths have to be relative to the correct directory: sometimes
the main directory for LaTeX (the one at pdflatex-time) and sometimes
at yanntricks-time.

We cannot provide absolute paths because the file `*.yanntricks` could
be git-tracked (this is the case for mazhe) and interpreted by
other people.
"""

class RelativeFile:
    """Wrap around a `pathlib.Path`."""
    def __init__(self, path, path_keeper):
        """
        Initialize with a paths and a `PathsKeeper`.

        @param {pathlib.Path} `paths`
            Assumed to be an absolute path.
        @param {PathsKeeper} `paths`
        """
        self.path = path
        self.paths_keeper = paths_keeper
    def for_sage(self):
        """
        Return the path of `self` relative to the Sage's directory.

        The Sage's directory is the directory in which Sage is
        launched.
        """
        return self.path.relative_to(self.path_keeper["sage_dir"])
