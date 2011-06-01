#!/usr/bin/env python

from subprocess import Popen, PIPE

def gather_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read().strip()

def gather_from_command(command):
    return Popen(command, stdout=PIPE).communicate()[0].strip()

def gather(gather_list):
    g_info = dict()
    for key, func, arg in gather_list:
        g_info[key] = func(arg)
    return g_info


gather_list = [
        ('os-version', gather_from_file, '/etc/issue'),
        ('uname', gather_from_command, ('uname', '-r', '-i')),
        ]

g = gather(gather_list)
print g
