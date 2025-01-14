"""
****************************************************************************************************
:copyright (c) 2019 URBANopt, Alliance for Sustainable Energy, LLC, and other contributors.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions
and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions
and the following disclaimer in the documentation and/or other materials provided with the
distribution.

Neither the name of the copyright holder nor the names of its contributors may be used to endorse
or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
****************************************************************************************************
"""

import logging
import os
import shutil

_log = logging.getLogger(__name__)


class ModelicaPath(object):
    """
    Class for storing Modelica paths. This allows the path to point to
    the model directory and the resources directory.
    """

    def __init__(self, name, root_dir, overwrite=False):
        """
        Create a new modelica-based path with name of 'name'

        :param name: Name to create
        """
        self.name = name
        self.root_dir = root_dir

        # create the directories
        if root_dir is not None:
            check_path = os.path.join(self.files_dir)
            self.clear_path(check_path, overwrite=overwrite)
            check_path = os.path.join(self.resources_dir)
            self.clear_path(check_path, overwrite=overwrite)

    def clear_path(self, path, overwrite=False):
        if os.path.exists(path):
            if overwrite:
                raise Exception("Directory already exists and overwrite is false for %s" % path)
            else:
                shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    @property
    def files_dir(self):
        if self.root_dir is None:
            return self.name
        else:
            return os.path.join(self.root_dir, self.name)

    @property
    def resources_dir(self):
        if self.root_dir is None:
            return os.path.join('Resources', 'Data', self.name)
        else:
            return os.path.join(self.root_dir, 'Resources', 'Data', self.name)
