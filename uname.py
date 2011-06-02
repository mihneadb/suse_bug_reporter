#!/usr/bin/env python

from subprocess import Popen, PIPE


def gather_from_uname():
    ''' generates a dictionary that contains three keys:
    kernel_release, kernel_version and hw_platform '''

    uname = dict()

    output = Popen(('uname', '-r'), stdout=PIPE).communicate()[0]
    uname['kernel_release'] = output.strip()

    output = Popen(('uname', '-v'), stdout=PIPE).communicate()[0]
    uname['kernel_version'] = output.strip()

    output = Popen(('uname', '-i'), stdout=PIPE).communicate()[0]
    uname['hw_platform'] = output.strip()

    return uname


if __name__ == '__main__':
    data = gather_from_uname()
    print data

