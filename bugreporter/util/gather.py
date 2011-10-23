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

from subprocess import Popen, PIPE

# where to gather the information from
gather_from = ['lsmod', 'uname', 'release', 'cpu', 'vga', 'mem', 'cmdline']

# name of the main package
pkg = 'bugreporter'

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

