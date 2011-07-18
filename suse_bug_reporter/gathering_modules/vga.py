#!/usr/bin/env python

from subprocess import Popen, PIPE


def gather_from_vga():
    ''' Returns a string that represents the graphic adapter's name, as
        told by the lspci output '''

    lspci = Popen('/sbin/lspci', stdout=PIPE)
    grep = Popen(('grep', 'VGA'), stdin=lspci.stdout, stdout=PIPE)
    lspci.stdout.close()
    output = grep.communicate()[0]

    output = output.split()

    vga = ' '.join(output[4:])
    return vga


if __name__ == '__main__':
    test = gather_from_vga()
    print test
