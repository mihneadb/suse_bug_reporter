#!/usr/bin/env python

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
