#!/usr/bin/env python


import os
import subprocess
import sys
import tempfile


def print_list(a_list, attr_list=None, columns=1, msg=None):
    ''' formats the options list on one or two columns with an index
    associated to each entry;
    Works also for objects that have attributes to be printed '''

    assert columns == 1 or columns == 2

    if msg != None:
        print msg

    for i in range(len(a_list)):
        s = ''
        if attr_list != None:
            for attr in attr_list:
                if attr == 'id':
                    s += '(#' + repr(getattr(a_list[i], attr)) + ') '
                    continue
                s += repr(getattr(a_list[i], attr)) + ' '

        print '%3d. %-40s' % (i + 1, a_list[i] if attr_list == None else s),
        if columns == 1 or i % 2 == 1:
            print ''

    print ''


def fitString(s, cols):
    ''' returns a fraction + [...] of a string if it doesnt fit cols, or
    the whole string if it fits '''

    length = len(s)
    if length >= cols:
        return s[:cols-7] + ' [...]'
    return s

def pager(a_list, attr_list=None, columns=1, msg=None):
    '''Outputs the provided list similar to more / less. Provides the possibility
    of selecting a _valid_ index (checks it). Also, if nothing is selected, it returns
    None'''
    
    length = len(a_list)
    printed_lines = 0

    while printed_lines < length:
        sizes = os.popen('stty size', 'r').read().split()
        rows = int(sizes[0])
        cols = int(sizes[1])
        nr = rows - 2
        if msg != None:
            nr -= len(msg) / cols + 2
            print msg
            print ''
        lines_left = length - printed_lines
        for i in range(nr if nr < lines_left else lines_left):
            s = ''
            if attr_list != None:
                for attr in attr_list:
                    if attr == 'id':
                        s += '(#' + repr(getattr(a_list[printed_lines + i], attr)) + ') '
                        continue
                    s += repr(getattr(a_list[printed_lines + i], attr)) + ' '
            line = '%3d. %-40s' % (printed_lines + i + 1,
                    a_list[printed_lines + i] if attr_list == None else s)
            print fitString(line, cols),
            if columns == 1 or i % 2 == 1:
                print ''
        printed_lines += nr
        print "[n]ext page    [r]eturn (select nothing)"
        while True:
            ans = raw_input('Answer--> ')
            if ans in ('r', 'R'):
                return None
            if ans in ('n', 'N'):
                if printed_lines >= length:
                    print 'No more entries to display. Please select [r]eturn or an index.'
                    continue
                break
            try:
                idx = int(ans)
                assert idx > 0
                assert idx <= length
            except (ValueError, AssertionError):
                print 'Invalid index, please try again.'
            else:
                return idx - 1


def choice(msg, *options):
    ''' prompts the user with a multiple choice question;
        if the options passed are for example 'contribute' and 'new',
        it will show '[c]ontribute' and '[n]' and it will only accept
        'c' and 'n' (or their uppercase equivalents) as valid input

        returns the index of the selected option from the argument tuple '''

    print msg

    # generate the list of valid inputs and print the choices
    opts = []
    for opt in options:
        firstChar = opt[0].lower()
        opts.append(firstChar)
        print '[' + firstChar + ']' + opt[1:] + ' ',

    print ''

    # get (and check) the input
    resp = raw_input('Answer: ')
    while resp.lower() not in opts:
        print 'Invalid answer!'
        resp = raw_input('Try again: ')

    # get the index and return it
    return opts.index(resp.lower())


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

    print 'Enter a valid index number between 1 and ' + str(length) + ':'

    while True:
        try:
            idx = int(raw_input('Index: '))
            assert idx > 0
            assert idx <= length
        except (ValueError, AssertionError):
            print 'Not a valid index, try again.'
        else:
            break

    return idx - 1


def custom_input(msg='', preselect=''):
    ans = raw_input(msg + "[preselected: %s] " % preselect)
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
                              'a)bort, c)ontinue, e)dit: ')
            if input in 'aA':
                os.unlink(filename)
                sys.exit(1)
            elif input in 'cC':
                os.unlink(filename)
                return ''
            elif input in 'eE':
                pass
