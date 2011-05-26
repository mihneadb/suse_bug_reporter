#!/usr/bin/env python

import os

# you can define the output file name here
sysinfo_file_name = 'sysinfo'


sysinfo_file = open('%s' % sysinfo_file_name, 'w')

sysinfo_file.write('OS version:\n\n')
sysinfo_file.close()
os.system('cat /etc/SuSE-release >> %s' % sysinfo_file_name)
sysinfo_file = open('%s' % sysinfo_file_name, 'a')
sysinfo_file.write('\n------------------------------------------' \
        '-------------------------------------\n\n')

sysinfo_file.write('Uname output:\n\n')
sysinfo_file.close()
os.system('uname -a >> %s' % sysinfo_file_name)
sysinfo_file = open('%s' % sysinfo_file_name, 'a')
sysinfo_file.write('\n------------------------------------------' \
        '-------------------------------------\n\n')

sysinfo_file.write('CPU info:\n\n')
sysinfo_file.close()
os.system('cat /proc/cpuinfo >> %s' % sysinfo_file_name)
sysinfo_file = open('%s' % sysinfo_file_name, 'a')
sysinfo_file.write('\n------------------------------------------' \
        '-------------------------------------\n\n')

sysinfo_file.write('lspci output:\n\n')
sysinfo_file.close()
os.system('lspci >> %s' % sysinfo_file_name)
sysinfo_file = open('%s' % sysinfo_file_name, 'a')
sysinfo_file.write('\n------------------------------------------' \
        '-------------------------------------\n\n')

sysinfo_file.write('lsmod output:\n\n')
sysinfo_file.close()
os.system('lsmod >> %s' % sysinfo_file_name)
sysinfo_file = open('%s' % sysinfo_file_name, 'a')
sysinfo_file.write('\n------------------------------------------' \
        '-------------------------------------\n\n')

sysinfo_file.close()
