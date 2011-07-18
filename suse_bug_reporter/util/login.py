#!/usr/bin/env python

import os

home = os.path.expanduser('~') # path to home folder
home += '/'


def getCreds():

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
