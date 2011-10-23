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

import os
import osc.conf

home = os.path.expanduser('~') # path to home folder
home += '/'


def getCredsFromOscrc():
    ''' obsolete '''

    #try to get username & password from ~/.oscrc
    try:
        oscrc = open(home + '.oscrc', 'r')
        lines = oscrc.readlines()
        oscrc.close()
        for line in lines:
            if 'user' in line:
                words = line.split()
                if words[0] == 'user':
                    username = words[2]
                continue
            if 'pass' in line:
                words = line.split()
                if words[0] == 'pass':
                    password = words[2]
                    print 'Found username & password in ~/.oscrc.'
                    return (username, password)

    except IOError:
        # no oscrc file
        print 'Please setup your osc / oscrc file. Exiting.'
        sys.exit(1)


def getCreds():
    try:
        osc.conf.get_config()
        username = osc.conf.config['api_host_options']['https://api.opensuse.org']['user']
        password = osc.conf.config['api_host_options']['https://api.opensuse.org']['pass']
        
        print 'The user has stored credentials.'
        return (username, password)
    
    except osc.oscerr.NoConfigfile:
        print 'You have to have a valid .oscrc file. Please do so by running osc'
        sys.exit(1)
