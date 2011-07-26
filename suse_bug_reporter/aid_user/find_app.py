#!/usr/bin/env python

import sys
from subprocess import Popen, PIPE, STDOUT


def find_app(resp=None):
    ''' returns a string that represents the name of the application
        clicked by the user '''

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
    return msg

if __name__ == '__main__':
    print find_app()
