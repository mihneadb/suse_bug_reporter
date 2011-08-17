import os
from distutils.core import setup

setup(name='suse_bug_reporter',
        version='1.0',
        description='Bug reporting tool for openSUSE',
        author='Mihnea Dobrescu-Balaur',
        author_email='mihneadb@gmail.com',
        url='https://github.com/mihneadb/suse_bug_reporter/',
        packages=['suse_bug_reporter',
            'suse_bug_reporter.aid_user',
            'suse_bug_reporter.gathering_modules',
            'suse_bug_reporter.util'
            ],
        scripts=['bin/bugreporter.py'],
        #requires=['python-bugzilla (>=0.6.2)'],
        data_files=[('tests', [os.path.join('tests', f) for f in os.listdir('tests')
            if not f.endswith('.pyc')]),
            ('share/man/man1', ['bugreporter.1'])
            ]
     )
