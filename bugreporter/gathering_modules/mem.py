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


def gather_from_mem():
    ''' returns a string which represents the amount of kB of RAM the
        machine has '''

    output = Popen(('cat', '/proc/meminfo'), stdout=PIPE).communicate()[0]

    # process the output
    output = output.splitlines()
    output = output[0]
    output = output.split()

    ram = output[1] + ' ' + output[2]
    return ram

if __name__ == '__main__':
    test = gather_from_mem()
    print test
