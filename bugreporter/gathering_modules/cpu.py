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


def gather_from_cpu():
    ''' returns a string which represents the cpu model '''

    output = Popen(('cat', '/proc/cpuinfo'), stdout=PIPE).communicate()[0]

    # process the output
    output = output.splitlines()
    output = output[4]
    output = output.split()

    cpu = ' '.join(output[3:8])
    return cpu


if __name__ == '__main__':
    test = gather_from_cpuinfo()
    print test
