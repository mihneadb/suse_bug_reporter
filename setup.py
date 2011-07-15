from distutils.core import setup
from glob import glob

setup(name='suse_bug_reporter',
        version='0.1',
        description='Bug reporting tool for openSUSE',
        author='Mihnea Dobrescu-Balaur',
        author_email='mihneadb@gmail.com',
        url='https://github.com/mihneadb/suse_bug_reporter/',
        packages=['suse_bug_reporter'],
        scripts=['bin/susebugreporter.py'],
     )
