from subprocess import Popen, PIPE


def gather_from_cpu():
    ''' returns a string which represents the cpu model '''

    output = Popen(('cat', '/proc/cpuinfo'), stdout=PIPE).communicate()[0]

    # process the output
    output = output.splitlines()
    output = output[4]
    output = output.split()

    cpu = ' '.join(output[3:8])
    return cpu


if __name__ == '__main__':
    test = gather_from_cpuinfo()
    print test
