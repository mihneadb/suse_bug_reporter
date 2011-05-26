#!/usr/bin/env python

import os

sysinfo_file_name = 'sysinfo'
sysinfo_file = open('%s' % sysinfo_file_name, 'w')

sysinfo_file.write('OS version:\n')
os.system('cat /etc/SuSE-release > %s' % sysinfo_file_name)
sysinfo_file.write('\n------------------------------------------\n')

sysinfo_file.write('CPU info:\n')
os.system('cat /proc/cpuinfo > %s' % sysinfo_file_name)
sysinfo_file.write('\n------------------------------------------\n')

sysinfo_file.write('lspci output:\n')
os.system('lspci > %s' % sysinfo_file_name)
sysinfo_file.write('\n------------------------------------------\n')

sysinfo_file.write('lsmod output:\n')
os.system('lsmod > %s' % sysinfo_file_name)
sysinfo_file.write('\n------------------------------------------\n')


sysinfo_file.close()
