#!/usr/bin/env python
 
import sys
import argparse
import re
import pprint
import osc.conf
 
# name of the main package
pkg = 'suse_bug_reporter'

# name of the util package
u_pkg = 'util'

# name of the aid user package
a_pkg = 'aid_user'

# relevance threshold for similar bug search
rel_threshold = 0.75

# custom imports
import bugzilla
from suse_bug_reporter.util.console import print_list, yes_no, get_index
from suse_bug_reporter.util import packageInfo, gather, login
from suse_bug_reporter.util.sortByKeywords import sortByKeywords
from suse_bug_reporter.util.bugReport import BugReport




def do_aid(args):

    aid = args.choice

    # safety precaution for exec
    ns = dict()

    exec 'from %s.%s import %s' % (pkg, a_pkg, aid) in ns
    exec 'output = %s.%s()' % (aid, aid) in ns
    print ns['output']

def do_gather(args):

    print 'Gathering relevant system information...'

    data = gather.gather_data(gather.gather_from)

    pprint.pprint(data)

def initBugzilla():

    # check login
    (username, password) = login.getCreds()

    print "Connecting to Novell's Bugzilla..."

    # instantiate the bugzilla object
    bugzillaURL = 'https://bugzilla.novell.com/xmlrpc.cgi'
    cls = bugzilla.getBugzillaClassForURL(bugzillaURL)
    bz = cls(url=bugzillaURL, user=username, password=password)

    return bz

def do_submit(args):

    # init osc
    try:
        osc.conf.get_config()
    except osc.oscerr.NoConfigfile:
        print 'You have to have a valid .oscrc file. Please do so by running osc.'
        sys.exit(1)

    # init bugzilla
    bz = initBugzilla()

    print ''
    print "If you don't know which package you want to file a bug to, you can"\
            " use the susebugreport aid command to get some help."
            
    print "Which is the package you want to file a report against?"
    print "If you are not sure, you can just type the beginning of the name and"\
            " use a '*' to invoke globbing."

    name = raw_input('Package name: ')
    if name.strip() == '':
        print 'Package name cannot be blank!'
        sys.exit(1)
    pkg_info = packageInfo.getInfo(name)

    if pkg_info == None:
        # no pkg found
        print "No installed package found, maybe try adding the '*' character?"
        sys.exit(1)

    name = pkg_info[3]

    print ''
    print "You have selected " +  name + "."
    print "Please enter the bug summary (should be concise!)"
    summary = raw_input('--> ')

    # check similar bug reports through query by package and then match keywords
    bug_list = bz.query({'summary': name})

    if len(bug_list) > 0:
        kw_list = re.findall(r'\w+', summary.lower())
        if name in kw_list:
            del kw_list[kw_list.index(name)]
        bug_list = sortByKeywords(bug_list, kw_list, rel_threshold)

    print ''

    if len(bug_list) > 0:
        # if there are still relevant bugs in the list
        # ask the user to modify a similar bug report or create a new one
        print_list(bug_list, attr='summary',
                msg='These are the similar bug reports found')

        print ''

        msg = 'Do you want to contribute to one of the bug reports above or'\
                ' submit a new one?  yes (contribute)/no (new one)'
        yes = yes_no(msg, yes='contribute', no='submit new')

        print ''
        if yes:
            idx = get_index(len(bug_list),
                    msg='Which report do you want to contribute to?')
            bug = bug_list[idx]
            print ''
            print 'You have selected bug #' + str(bug.id) + ' with the summary '\
                    + '"' + bug.summary + '"' + '.'
            print 'You can contribute to it at this URL: ' + bug.url

            sys.exit(0)

    else:
        print 'There were no similar bug reports found, you have to submit a new one.'

    # gather the rest of the required data and submit the bug
    print ''
    try:
        automat = BugReport(bz=bz, pkg=name, pkg_info=pkg_info, summary=summary)
        automat.main()
    except EOFError, eofe:
        return 0
    except (KeyboardInterrupt, SystemExit):
        return 1
    
    return 0


def do_query(args):

    bz = initBugzillaAndPkgInfo()

    name = args.package
    if name.strip() == '':
        print 'Package name cannot be blank!'
        sys.exit(1)
    pkg_info = packageInfo.getInfo(name)

    if pkg_info == None:
        # no pkg found
        print "No package found, maybe try adding the '*' character?"
        sys.exit(1)

    name = pkg_info[3]

    print ''
    print "You have selected " +  name + "."
    print "Please enter the bug summary (should be concise!)"
    print "You can leave blank to get _all_ the bugs matching that package"
    summary = raw_input()

    # check similar bug reports through query by package and then match keywords
    print ''
    print 'Searching Bugzilla...'
    bug_list = bz.query({'summary': name})

    if len(bug_list) > 0 and summary != '':
        kw_list = re.findall(r'\w+', summary.lower())
        if name in kw_list:
            del kw_list[kw_list.index(name)]
        bug_list = sortByKeywords(bug_list, kw_list, rel_threshold)

    print ''

    if len(bug_list) > 0:
        # if there are still relevant bugs in the list
        
        print_list(bug_list, attr='summary',
                msg='These are the similar bug reports found:')
        print ''
        
        idx = get_index(len(bug_list),
                msg='Which report are you interested in?')
        bug = bug_list[idx]
        print ''
        print 'You have selected bug #' + str(bug.id) + ' with the summary '\
                + '"' + bug.summary + '"' + '.'
        print 'You can contribute to it at this URL: ' + bug.url

    else:
        print "No bug report found. Why not create one?"

    sys.exit(0)
 


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

    query = commands.add_parser('query', help='get a list of reports')
    query.set_defaults(func=do_query)
    query.add_argument('package', type=str)

 
    args = parser.parse_args()
    args.func(args)
 
 
if __name__ == '__main__':
    main()
