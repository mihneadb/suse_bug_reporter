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


def gather_from_release():
    ''' Generates a list of two strings which represent the openSUSE version
        number and architecture '''

    output = Popen(('cat', '/etc/SuSE-release'), stdout=PIPE).communicate()[0]

    # save only the first line (looks like "openSUSE 11.4 (x86_64)")
    output = output.splitlines()
    output = output[0]

    full_name = output

    # split the output and get the version number and the arch
    output = output.split()
    product = output[0] + ' ' + output[1]
    # because the arch string contains parantheses, I also remove them
    arch = output[2].replace('(', '').replace(')', '').replace('_', '-')

    release = (product, arch, full_name)
    return release

if __name__ == '__main__':
    test = gather_from_release()
    print test
