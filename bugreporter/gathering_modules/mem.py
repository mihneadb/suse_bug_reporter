from subprocess import Popen, PIPE


def gather_from_mem():
    ''' returns a string which represents the amount of kB of RAM the
        machine has '''

    output = Popen(('cat', '/proc/meminfo'), stdout=PIPE).communicate()[0]

    # process the output
    output = output.splitlines()
    output = output[0]
    output = output.split()

    ram = output[1] + ' ' + output[2]
    return ram

if __name__ == '__main__':
    test = gather_from_mem()
    print test
