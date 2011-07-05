#!/usr/bin/env python

from subprocess import Popen, PIPE


def gather_from_release():
    ''' Generates a list of two strings which represent the openSUSE version
        number and architecture '''

    output = Popen(('cat', '/etc/SuSE-release'), stdout=PIPE).communicate()[0]

    # save only the first line (looks like "openSUSE 11.4 (x86_64)")
    output = output.splitlines()
    output = output[0]

    full_name = output

    # split the output and get the version number and the arch
    output = output.split()
    product = output[0] + ' ' + output[1]
    # because the arch string contains parantheses, I also remove them
    arch = output[2].replace('(', '').replace(')', '').replace('_', '-')

    release = (product, arch, full_name)
    return release

if __name__ == '__main__':
    test = gather_from_release()
    print test
