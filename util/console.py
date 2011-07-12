#!/usr/bin/env python


import os
import subprocess
import sys
import tempfile


def print_list(a_list, attr=None, columns=1, msg=None):
    ''' formats the options list on one or two columns with an index
    associated to each entry;
    Works also for objects that have an attribute to be printed '''

    assert columns == 1 or columns == 2

    if msg != None:
        print msg

    for i in range(len(a_list)):
        print '%3d. %-40s' % (i,
                a_list[i] if attr == None else getattr(a_list[i], attr)),
        if columns == 1 or i % 2 == 1:
            print ''
       
    print ''


def reply(msg, *options):
    ''' prompts the user with a multiple choice question
        if the options passed are for example 'contribute' and 'new',
        it will show '[c]ontribute' and '[n]' and it will only accept
        'c' and 'n' (or their uppercase equivalents) as valid input '''

        print msg
        opts = list()
        for opt in options:

def yes_no(msg, yes=None, no=None):
    ''' prompts the user with a yes / no question and returns True or False '''

    print msg
    if yes != None:
        print 'Yes: ' + yes
    if no != None:
        print 'No: ' + no

    print ''
    response = raw_input('Answer: ')
    while response.lower() != 'yes' and response.lower() != 'no':
        print 'Invalid answer: yes/no only!'
        response = raw_input('Try again: ')

    if response.lower() == 'yes':
        return True

    return False


def get_index(length, msg=None):
    ''' prompts the user for a valid index and returns it '''

    if msg != None:
        print msg

    print 'Enter a valid index number between 0 and ' + str(length - 1) + ':'

    while True:
        try:
            idx = int(raw_input('Index: '))
            assert idx >= 0
            assert idx < length
        except (ValueError, AssertionError):
            print 'Not a valid index, try again.'
        else:
            break

    return idx


def custom_input(msg='', preselect=''):
    ans = raw_input(msg)
    if ans == '':
        return preselect

    return ans


def get_editor():
    ''' Author: Michal Vyskocil <mvyskocil@suse.cz> '''
    default = 'vim'
    if sys.platform[:3] == 'win':
        default = 'notepad'

    return os.getenv('EDITOR', default=default)


def edit_message(template, prefix="", resp=None):
    ''' Author: Michal Vyskocil <mvyskocil@suse.cz> '''
    if resp:    return prefix + resp
    
    delim = '#Write a description below.'

    editor = get_editor()

    (fd, filename) = tempfile.mkstemp(prefix = 'susereport-description', suffix = '.txt', dir = '/tmp')
    f = os.fdopen(fd, 'w')
    if template != '':
        f.write(template)
    f.write('\n\n')
    if prefix != '':
        f.write(prefix)
    f.write('\n\n')
    f.write(delim)
    f.write('\n\n')
    f.flush()
    f.close()
    mtime_orig = os.stat(filename).st_mtime

    line = len(template.split('\n')) + len(prefix.split('\n'))+4
    while 1:
        subprocess.call('%s +%d %s' % (editor, line, filename), shell=True)
        mtime = os.stat(filename).st_mtime
        if mtime_orig < mtime:
            msg = open(filename).read()
            os.unlink(filename)

            lmsg = msg.split(delim)
            if len(lmsg) > 1:
                return prefix + '\n' + lmsg[1].lstrip()
            return prefix + '\n\n' + msg

        else:
            input = raw_input('Log message unchanged or not specified\n'
                              'a)bort, c)ontinue, e)dit: ', 'a')
            if input in 'aA':
                os.unlink(filename)
                sys.exit(1)
            elif input in 'cC':
                os.unlink(filename)
                return ''
            elif input in 'eE':
                pass
