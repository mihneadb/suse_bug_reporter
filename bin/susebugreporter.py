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

    # safety precaution for exec
    ns = dict()

    exec 'from %s.%s import %s' % (pkg, a_pkg, aid) in ns
    exec 'output = %s.%s()' % (aid, aid) in ns
    print ns['output']

def do_gather(args):

    print 'Gathering relevant system information...'

    exec 'from %s.%s import gather' % (pkg, u_pkg)
    data = gather.gather_data(gather.gather_from)

    import pprint
    pprint.pprint(data)

def do_submit(args):

    # check login
    # TODO

    # instantiate the bugzilla object
    # TODO

    exec 'from %s.%s import packageInfo' % (pkg, u_pkg)

    print "If you don't know which package you want to file a bug to, you can"\
            " use the susebugreport aid command to get some help."
            
    print "which is the package you want to file a report against?"
    print "If you are not sure, you can just type the beginning of the name and"\
            " use a '*' to invoke globbing."

    name = raw_input()
    pkg_info = packageInfo.getInfo(name)

    if pkg_info == None:
        # no pkg found
        print "No package found, maybe try adding the '*' character?"
        sys.exit(1)

    name = pkg_info[3]

    print "You have selected " +  name + "."
    print "Please enter the bug summary (should be concise!)"
    summary = raw_input()

    # check similar bug reports through query by package and then match keywords
    # TODO

    # gather the rest of the required data
    # TODO

    # submit the bug
    # TODO


 
def main():
 
    # creating the parser for the arguments
    parser = argparse.ArgumentParser(description='Bugzilla interactions')
    commands = parser.add_subparsers()
    
    aid = commands.add_parser('aid', help='aid users to find the relevant app')
    aid.set_defaults(func=do_aid)
    aid.add_argument('choice', type=str, choices=['find_app'])
    
    gather = commands.add_parser('gather', help='gather relevant system info')
    gather.set_defaults(func=do_gather)

    submit = commands.add_parser('submit', help='submit a new bug')
    submit.set_defaults(func=do_submit)

 
    args = parser.parse_args()
    args.func(args)
 
    #print(args)
 
 
if __name__ == '__main__':
    main()
