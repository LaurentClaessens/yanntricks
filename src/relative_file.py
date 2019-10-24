#######################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

# copyright (c) Laurent Claessens, 2019
# email: laurent@claessens-donadello.eu

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

# pylint: disable = too-few-public-methods

import os
from pathlib import Path

dprint = print  #pylint: disable=invalid-name


class RelativeFile:
    """Wrap around a `pathlib.Path`."""

    def __init__(self, path, paths_keeper):
        """
        Initialize with a paths and a `PathsKeeper`.

        @param {pathlib.Path} `paths`
            Assumed to be relative to the main LaTeX directory
        @param {PathsKeeper} `paths`
        """
        self.paths_keeper = paths_keeper
        self.path = path

        self.abs_path = self.paths_keeper["main_tex"] / path
        self.abs_path = self.abs_path.resolve()

    def from_sage(self):
        """
        Return the path of `self` relative to the Sage's directory.

        The Sage's directory is the directory in which Sage is
        launched.
        """
        sage_dir = self.paths_keeper["sage_dir"]
        return Path(os.path.relpath(self.abs_path, sage_dir))

    def from_main(self):
        """
        Return the path of `self` relative to the main directory.

        The main directory is the one from which LaTeX is launched.
        """
        main_tex = self.paths_keeper["main_tex"]
        return Path(os.path.relpath(self.abs_path, main_tex))
