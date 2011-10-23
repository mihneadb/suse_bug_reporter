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


def gather_from_vga():
    ''' Returns a string that represents the graphic adapter's name, as
        told by the lspci output '''

    lspci = Popen('/sbin/lspci', stdout=PIPE)
    grep = Popen(('grep', 'VGA'), stdin=lspci.stdout, stdout=PIPE)
    lspci.stdout.close()
    output = grep.communicate()[0]

    output = output.split()

    vga = ' '.join(output[4:])
    return vga


if __name__ == '__main__':
    test = gather_from_vga()
    print test
