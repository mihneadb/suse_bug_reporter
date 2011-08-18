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
        data_files=[('share/man/man1', ['bugreporter.1'])],
        platforms='linux',
        license='Unknown'
     )
