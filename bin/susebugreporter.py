#!/usr/bin/env python
 
import sys
import argparse
 
# name of the main package
pkg = 'suse_bug_reporter'

# name of the util package
u_pkg = 'util'

# name of the aid user package
a_pkg = 'aid_user'

# relevance threshold for similar bug search
rel_threshold = 0.75

# imports - using exec temporarily, as this is a dev project and the names could change
import bugzilla
exec 'from %s.%s import packageInfo' % (pkg, u_pkg) # from suse_bug_reporter import packageInfo




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

def initBugzillaAndPkgInfo():

    # check login
    exec 'from %s.%s import login' % (pkg, u_pkg)
    (username, password) = login.getCreds()

    print "Connecting to Novell's Bugzilla..."

    # instantiate the bugzilla object
    bugzillaURL = 'https://bugzilla.novell.com/xmlrpc.cgi'
    cls = bugzilla.getBugzillaClassForURL(bugzillaURL)
    bz = cls(url=bugzillaURL, user=username, password=password)

    return bz

def do_submit(args):

    bz = initBugzillaAndPkgInfo()

    print ''
    print "If you don't know which package you want to file a bug to, you can"\
            " use the susebugreport aid command to get some help."
            
    print "Which is the package you want to file a report against?"
    print "If you are not sure, you can just type the beginning of the name and"\
            " use a '*' to invoke globbing."

    name = raw_input('Package name: ')
    pkg_info = packageInfo.getInfo(name)

    if pkg_info == None:
        # no pkg found
        print "No package found, maybe try adding the '*' character?"
        sys.exit(1)

    name = pkg_info[3]

    print ''
    print "You have selected " +  name + "."
    print "Please enter the bug summary (should be concise!)"
    summary = raw_input()

    # check similar bug reports through query by package and then match keywords
    bug_list = bz.query({'summary': name})

    if len(bug_list) > 0:
        import re
        exec 'from %s.%s import sortByKeywords' % (pkg, u_pkg)
        kw_list = re.findall(r'\w+', summary.lower())
        if name in kw_list:
            del kw_list[kw_list.index(name)]
        bug_list = sortByKeywords.sortByKeywords(bug_list, kw_list, rel_threshold)

    print ''

    if len(bug_list) > 0:
        # if there are still relevant bugs in the list
        # ask the user to modify a similar bug report or create a new one
        print 'These are the similar bug reports found:'
        for i in range(len(bug_list)):
            print str(i) + '. ' + bug_list[i].summary
        print ''
        print 'Do you want to contribute to one of the bug reports above or'\
                ' submit a new one?  yes (contribute)/no (new one)'
        response = raw_input()
        while response.lower() != 'yes' and response.lower() != 'no':
            print 'Invalid answer: yes/no only!'
            response = raw_input('Try again: ')

        print ''
        if response.lower() == 'yes':
            print 'Which report do you want to contribute to?'
            print 'Enter a number between 0 and ' + str(len(bug_list) - 1) + ':'

            while True:
                try:
                    idx = int(raw_input('Number: '))
                    assert idx >= 0
                    assert idx < len(bug_list)
                except (ValueError, AssertionError):
                    print 'Not a valid index!'
                else:
                    break

            bug = bug_list[idx]
            print ''
            print 'You have selected bug #' + str(bug.id) + ' with the summary '\
                    + '"' + bug.summary + '"' + '.'
            print 'You can contribute to it at this URL: ' + bug.url

            sys.exit(0)

    else:
        print 'There were no similar bug reports found, you have to submit a new one.'

    # gather the rest of the required data
    print ''
    print 'Gathering necessary data..'
    # TODO
    

    # submit the bug
    # TODO


def do_query(args):

    bz = initBugzillaAndPkgInfo()

    name = args.package
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
    bug_list = bz.query({'summary': name})

    if len(bug_list) > 0 and summary != '':
        import re
        exec 'from %s.%s import sortByKeywords' % (pkg, u_pkg)
        kw_list = re.findall(r'\w+', summary.lower())
        if name in kw_list:
            del kw_list[kw_list.index(name)]
        bug_list = sortByKeywords.sortByKeywords(bug_list, kw_list, rel_threshold)

    print ''

    if len(bug_list) > 0:
        # if there are still relevant bugs in the list
        
        print 'These are the similar bug reports found:'
        for i in range(len(bug_list)):
            print str(i) + '. ' + bug_list[i].summary
        print ''
        
        print 'Which report are you interested in?'
        print 'Enter a number between 0 and ' + str(len(bug_list) - 1) + ':'

        while True:
            try:
                idx = int(raw_input('Number: '))
                assert idx >= 0
                assert idx < len(bug_list)
            except (ValueError, AssertionError):
                print 'Not a valid index!'
            else:
                break

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
