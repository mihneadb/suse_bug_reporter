#!/usr/bin/env python

from subprocess import Popen, PIPE


def gather_from_cmdline():
    ''' returns a list of strings which represent the kernel boot arguments '''

    output = Popen(('cat', '/proc/cmdline'), stdout=PIPE).communicate()[0]

    # process the output
    output = output.split()
    output = output[3:]

    return output

if __name__ == '__main__':
    test = gather_from_cmdline()
    print test
