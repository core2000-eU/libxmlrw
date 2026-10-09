#Copyright (c) 2026 Benjamin Winter
#This file is part of libxmlrw which is released under the MIT License.
#See file LICENSE or go to https://github.com/core2000-eU/libxmlrw for full license details.

#DESCRIPTION
#libxmlrw, a pythonic high-level XML parser to read and write XML files and structures.

import                          setuptools
from pathlib import             Path

parent_dir = Path(__file__).parent
long_description = (parent_dir / "README.md").read_text(encoding="utf-8")

setuptools.setup (
    name =                      "libxmlrw", 
    version =                   '0.0.1',
    author =                    "Benjamin Winter",
    license=                    "MIT",
    description =               "libxmlrw, a pythonic high-level XML parser to read and write XML files and structures",
    long_description =                  long_description,
    long_description_content_type =     "text/markdown",
    keywords =                  ['python', 'XML', 'read', 'write', 'syntax', 'parser'],
    classifiers =               [
                                    "Development Status :: 4 - Beta",
                                    "Programming Language :: Python :: 3",
                                    "Operating System :: OS Independent"
                                ],
    packages =                  setuptools.find_namespace_packages(where="src/P"),
    package_dir =               {"": "src/P"},
    install_requires =          [],
    package_data =              {},
)
