#!/usr/bin/env python

import rpm

from subprocess import Popen, PIPE

def find_package(pr=True):

    print "Which binary's package do you want to find?"
    name = raw_input('--> ')
    name = name.strip()

    ts = rpm.TransactionSet()
    
    if '/' not in name:
        output = Popen(('which', name), stdout=PIPE, stderr=PIPE).communicate()

        if output[0] == '':
            print 'Nothing named %s was found in your $PATH. '\
                'Maybe add /sbin and /usr/sbin to it?' % name
            return None

        name = output[0].strip()

    match = ts.dbMatch('basenames', name)
    for header in match:
        pkg = header['name']
    
    if pr:
        msg = 'The package that gives %s is %s.' % (name, pkg)
        print msg
    else:
        return pkg
