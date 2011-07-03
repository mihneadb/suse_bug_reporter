#!/usr/bin/env python

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
