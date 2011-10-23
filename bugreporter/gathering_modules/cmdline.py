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


def gather_from_cmdline():
    ''' returns a list of strings which represent the kernel boot arguments '''

    output = Popen(('cat', '/proc/cmdline'), stdout=PIPE).communicate()[0]

    # process the output
    output = output.split()
    output = output[3:]

    return output

if __name__ == '__main__':
    test = gather_from_cmdline()
    print test
