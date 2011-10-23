'''
Copyright (C) 2011  Mihnea Dobrescu-Balaur

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import os
from distutils.core import setup

setup(name='bugreporter',
        version='1.0',
        description='Bug reporting tool for openSUSE',
        author='Mihnea Dobrescu-Balaur',
        author_email='mihneadb@gmail.com',
        url='https://github.com/mihneadb/suse_bug_reporter/',
        packages=['bugreporter',
            'bugreporter.aid_user',
            'bugreporter.gathering_modules',
            'bugreporter.util'
            ],
        scripts=['bin/bugreporter'],
        #requires=['python-bugzilla (>=0.6.2)'],
        data_files=[('share/man/man1', ['bugreporter.1']),
                ('/etc/bash_completion.d', ['completion/bugreporter'])],
        platforms='linux',
        license='GPLv2+'
     )
