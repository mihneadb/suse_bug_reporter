#!/usr/bin/env python
 
import sys
import argparse
 
# name of the main package
pkg = 'suse_bug_reporter'

# name of the util package
u_pkg = 'util'

# name of the aid user package
a_pkg = 'aid_user'


def do_aid(args):

    aid = args.choice

    print 'Please click on the window to which you want to find the app name.'
    
    exec 'from %s.%s import %s' % (pkg, a_pkg, aid)
    exec 'output = %s.%s()' % (aid, aid)
    print "The app's name is " + output + '.'

def do_gather(args):
    print 'Gathering relevant system information...'

    exec 'from %s.%s import gather' % (pkg, u_pkg)
    data = gather.gather_data(gather.gather_from)

    import pprint
    pprint.pprint(data)

 
def main():
 
    # creating the parser for the arguments
    parser = argparse.ArgumentParser(description='Bugzilla interactions')
    commands = parser.add_subparsers()
    
    aid = commands.add_parser('aid', help='aid users')
    aid.set_defaults(func=do_aid)
    aid.add_argument('choice', type=str, choices=['find_app'])
    
    gather = commands.add_parser('gather', help='gather')
    gather.set_defaults(func=do_gather)

 
    args = parser.parse_args()
    args.func(args)
 
    #print(args)
 
 
if __name__ == '__main__':
    main()
