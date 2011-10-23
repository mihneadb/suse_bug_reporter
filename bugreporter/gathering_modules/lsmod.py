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


def gather_from_lsmod():
    ''' Generates a list of strings which represent the modules loaded
        at the moment '''

    modules_list = list()

    output = Popen('/sbin/lsmod', stdout=PIPE).communicate()[0]
    output = output.splitlines()
    del output[0]

    for line in output:
        modules_list.append(line.split()[0])

    return modules_list


if __name__ == '__main__':
    modules = gather_from_lsmod()
    print modules
