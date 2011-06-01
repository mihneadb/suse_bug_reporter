#!/usr/bin/env python

from subprocess import Popen, PIPE


def gather_from_lsmod():
    ''' Generates a list of strings which represent the modules loaded
        at the moment '''

    output = Popen('lsmod', stdout=PIPE).communicate()[0]
    output = output.splitlines()
    del output[0]

    modules = list()

    for line in output:
        modules.append(line.split()[0])

    return modules

if __name__ == '__main__':
    modules = gather_from_lsmod()
    print modules
