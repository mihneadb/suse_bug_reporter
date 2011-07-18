#!/usr/bin/env python

from subprocess import Popen, PIPE

# where to gather the information from
gather_from = ['lsmod', 'uname', 'release', 'cpu', 'vga', 'mem', 'cmdline']

# name of the main package
pkg = 'suse_bug_reporter'

# name of the gathering modules package
g_pkg = 'gathering_modules'


def gather_data(gather_list):
    ''' returns a dictionary with keys the sources from where the data was
        gathered (i.e. 'lsmod') and values the actual data that was found '''

    data = dict()

    for prop in gather_list:
        try:
            module = __import__('%s.%s.%s' % (pkg, g_pkg, prop), fromlist=[prop])
            data[prop] = getattr(module, 'gather_from_%s' % prop)()
        except OSError:
            continue

    return data


if __name__ == '__main__':
    test = gather_data(gather_from)
    print test

