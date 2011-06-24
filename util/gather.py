#!/usr/bin/env python

from subprocess import Popen, PIPE
import sys
import os

# path fix
cmd_folder = os.path.join(os.path.dirname(__file__), '..')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# gathering modules package name
pkg = 'gathering_modules'

# where to gather the information from
gather_from = ['lsmod', 'uname', 'release', 'cpu', 'vga', 'mem', 'cmdline']

def gather_data(gather_list):
    ''' returns a dictionary with keys the sources from where the data was
        gathered (i.e. 'lsmod') and values the actual data that was found '''

    data = dict()

    for prop in gather_list:
        exec('import %s.%s' % (pkg, prop))
        module = sys.modules[pkg + '.' + prop]
        data[prop] = getattr(module, 'gather_from_%s' % prop)()

    return data


if __name__ == '__main__':
    test = gather_data(gather_from)
    print test
