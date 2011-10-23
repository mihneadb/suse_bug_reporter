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

import sys
from subprocess import Popen, PIPE, STDOUT


def find_app(resp=None):
    '''Returns a tupla of two items: the first is the string that's printable
    to the user; The second is the actual app name'''

    print "Please click on the window of which you want to find the app name."

    if resp != None:
        output = resp

    else:
        output = Popen(('xprop', 'WM_CLASS'), stdout=PIPE, stderr=STDOUT).communicate()[0]
        if 'xprop' in output:
            print 'find_app not working! Error message: ' + output
            sys.exit(1)

    output = output.split()
    output = output[3].lower()
    output = output.replace('"', '')

    msg = "The app's name is " + output + "."
    return (msg, output)

if __name__ == '__main__':
    print find_app()
