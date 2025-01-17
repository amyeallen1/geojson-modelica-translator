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

import distutils.cmd
import distutils.log
import glob
import os
import re

PYTHON_REGEX = re.compile(r'^""".\*{100}.*:copyright.*\*{100}."""$', re.MULTILINE | re.DOTALL)
PYTHON_LICENSE = '''"""
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
"""'''

EXCLUDE_FILES = ["__init__.py", ]
PATHS = [
    {"glob": 'geojson_modelica_translator/**/*.py', "license": PYTHON_LICENSE, "REGEX": PYTHON_REGEX},
    {"glob": 'management/**/*.py', "license": PYTHON_LICENSE, "REGEX": PYTHON_REGEX},
    {"glob": 'tests/**/*.py', "license": PYTHON_LICENSE, "REGEX": PYTHON_REGEX},

    # single files
    # { "glob": 'bin/resources/**/file.py', "license": PYTHON_LICENSE, "REGEX": PYTHON_REGEX },
]


class UpdateLicenses(distutils.cmd.Command):
    """Custom comand for updating the GeoJSON schemas on which this project depends."""

    description = 'Update the license/copyright headers'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def check_and_update_license(self, filename):
        """
        check if the license exists in the file, and if it does, then make sure it is up-to-date with
        the license defined in this file.

        :param filename: str, path of the file to update
        :return: None
        """
        s = open(filename, 'r').read()
        if PYTHON_REGEX.search(s):
            print('License already exists, updating')
            content = re.sub(PYTHON_REGEX, PYTHON_LICENSE, s)
            with open(filename, 'w') as f:
                f.write(content)
                f.close()
        else:
            print('Adding license')
            with open(filename, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(PYTHON_LICENSE.rstrip('\r\n') + '\n\n\n' + content)
                f.close()

    def run(self):
        for p in PATHS:
            gl = glob.glob(p['glob'], recursive=True)
            for g in gl:
                if os.path.basename(g) in EXCLUDE_FILES:
                    print(f'Skipping file {g}')
                else:
                    print(f'Checking license in file {g}')
                    self.check_and_update_license(g)
