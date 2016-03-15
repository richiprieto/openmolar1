#! /usr/bin/python

# ########################################################################### #
# #                                                                         # #
# # Copyright (c) 2009-2016 Neil Wallace <neil@openmolar.com>               # #
# #                                                                         # #
# # This file is part of OpenMolar.                                         # #
# #                                                                         # #
# # OpenMolar is free software: you can redistribute it and/or modify       # #
# # it under the terms of the GNU General Public License as published by    # #
# # the Free Software Foundation, either version 3 of the License, or       # #
# # (at your option) any later version.                                     # #
# #                                                                         # #
# # OpenMolar is distributed in the hope that it will be useful,            # #
# # but WITHOUT ANY WARRANTY; without even the implied warranty of          # #
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           # #
# # GNU General Public License for more details.                            # #
# #                                                                         # #
# # You should have received a copy of the GNU General Public License       # #
# # along with OpenMolar.  If not, see <http://www.gnu.org/licenses/>.      # #
# #                                                                         # #
# ########################################################################### #

'''
This file contains the version number for openmolar
Do not edit this file manually, as it should be updated by make version
when git tag is updated.
'''

VERSION = "0.7.1"

# -------------------------- DEV CODE --------------------------------------- #
# this section of code is removed when making a release
#

import logging
import os
import re

LOGGER = logging.getLogger("openmolar")

LOGGER.warning("You are running a development version of OpenMolar!")

try:
    import git
    LOGGER.debug("checking to see if environment is a git repo")
    filepath = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(__file__))))
    repo = git.Repo(filepath)
    if repo.description == "openmolar1":
        try:
            git_version = repo.git.describe()
            VERSION = re.sub("v", "", git_version, 1)
        except git.exc.GitCommandError:
            LOGGER.exception("No git tags found?")

        if repo.is_dirty():
            VERSION += "-dirty"
    else:
        VERSION = "unofficial_build"
except ImportError:
    LOGGER.debug("unable to import git")
    VERSION = "Built without python-git"

# --------------------------END OF DEV CODE --------------------------------- #


if __name__ == '__main__':
    print("version = %s" % VERSION)
