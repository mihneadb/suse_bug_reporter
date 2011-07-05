#!/usr/bin/env python


import os
import pprint

from suse_bug_reporter.gathering_modules.release import gather_from_release
from suse_bug_reporter.util import console, packageInfo
from suse_bug_reporter.util import FSM_def


class BugReport(FSM_def.FSM):

    END_STATES = ('ERROR', 'EXIT', 'NYI')

    def __init__(self, bz, pkg, pkg_info, summary, data={}):

        super(BugReport, self).__init__()

        self.bz = bz
        self.data = data
        self.data['package'] = pkg
        self.pkg_info = pkg_info
        self.data['summary'] = summary
    

    def _resp(self, suffix=''):
        if self.data:
            return self.data.get(self._state + suffix)
        return None


    def getHeader(self):
        return """Package: %s
Summary: %s
Product: %s
Platform: %s
Component: %s
Severity: %s
Assigned to: %s
CC: %s""" % (self.data['package'],
        self.data['summary'],
        self.data['product'],
        self.data['rep_platform'],
        self.data['component'],
        self.data['severity'],
        self.data['assigned_to'],
        ', '.join(self.data['cc'])
        )


    def save(self, file_name=None):
        import tempfile
        if not file_name:
            (fd, file_name) = tempfile.mkstemp(
                    prefix = 'susebugreport',
                    suffix = '.save',
                    dir = '/tmp'
                    )
        else:
            fd = open(file_name, 'w')

        os.write(fd, self.getHeader())
        os.write(fd, '\n\n')
        os.write(fd, self.data['description'])
        os.write(fd, '\n')
        os.close(fd)

        return file_name


    def do_START(self):
        print ''
        print 'Starting the collecting data for the report process..'
        
        return "PRE_ASK_PRODUCT_PLATFORM"


    def do_PRE_ASK_PRODUCT_PLATFORM(self):
        print ''
        product, platform, full_name = gather_from_release()
        print 'Found %s.' % full_name
        correct = console.yes_no('Is that the correct product & platform? yes/no')

        if correct:
            self.data['product'] = product
            self.data['rep_platform'] = platform
            return 'TEST_PRODUCT_PLATFORM'

        return 'ASK_PRODUCT_PLATFORM'


    def do_ASK_PRODUCT_PLATFORM(self):
        print ''
        msg = 'Enter the name + version of the openSUSE product, or enter s'\
                ' if you want to  select it from a list.'
        ans = raw_input(msg)

        if ans in ('s', 'S'):
            return 'SELECT_PRODUCT_PLATFORM'

        self.data['product'] = ans
        return 'GET_PLATFORM'


    def do_GET_PLATFORM(self):
        print ''
        aux1, platform, aux2 = gather_from_release()
        msg = 'Enter your platform. Hint: %s was found.' % platform
        
        ans = console.custom_input(msg=msg, preselect=platform)
        data['rep_platform'] = ans

        return 'TEST_PRODUCT_PLATFORM'


    def do_SELECT_PRODUCT_PLATFORM(self):
        print ''
        print 'Getting list of products from Bugzilla...'

        tmp = self.bz.getproducts()
        product_list = [p['name'] for p in tmp]
        product_list.sort()

        console.print_list(product_list, columns=2, msg='Available products:')
        idx = console.get_index(len(product_list), msg='Which one?')

        self.data['product'] = product_list[idx]
        return 'do_GET_PLATFORM'


    def do_TEST_PRODUCT_PLATFORM(self):
        print ''
        if self.data['rep_platform'] == '':
            self.data['rep_platform'] = 'All'

        if self.data['product'] == '':
            print 'You have to select a product!'
            return 'SELECT_PRODUCT_PLATFORM'

        return 'GET_COMPONENT'


    def do_GET_COMPONENT(self):
        print ''
        print 'Getting list of components from Bugzilla for product %s.' % self.data['product']
        comp_list = self.bz.getcomponents(self.data['product'])

        # list is already sorted
        console.print_list(comp_list, columns=2, msg='Available components:')
        idx = console.get_index(len(comp_list), msg='Which one?')

        print 'Using component %s.' % comp_list[idx]
        self.data['component'] = comp_list[idx]

        return 'GET_VERSION'


    def do_GET_VERSION(self):
        print ''
        VERSIONS = ('Final', 'Factory', 'unspecified')
        print 'Please select the version of the OS you are using.'

        console.print_list(VERSIONS, msg='Available choices:')
        idx = console.get_index(len(VERSIONS), msg='Which one?')

        self.data['version'] = VERSIONS[idx]
        return 'LOAD_ASSIGNEE'


    def do_LOAD_ASSIGNEE(self):
        print ''
        assignee, cc = packageInfo.getAssignedPersons(self.pkg_info)

        print 'This/these address(es) were found:'
        print 'assignee: ' + assignee
        print 'cc: ',
        pprint.pprint(cc)

        yes = console.yes_no('Do you want to change the assignee? Yes/No')
        if yes:
            assignee = console.custom_input('New assignee:', preselect=assignee)

        yes = console.yes_no('Do you want to add another cc(s)? Yes/No')
        if yes:
            print 'Enter their e-mail addresses, one at a time.'
            print "To stop, enter something that does not contain '@'."
            ans = raw_input('Cc: ')
            while '@' in ans:
                cc.append(ans)
                ans = raw_input('Cc: ')

        self.data['assigned_to'] = assignee
        self.data['cc'] = cc

        return 'TEST_SUMMARY'


    def do_TEST_SUMMARY(self):
        print ''
        if self.data['summary'].strip() == '':
            return 'GET_SUMMARY'
        
        return 'GET_SEVERITY'


    def do_GET_SUMMARY(self):
        print ''
        print "Summary can't be empty! Please enter a concise description"\
                    "of the bug you are reporting"
        ans = raw_input('--> ')
        self.data['summary'] = ans

        return 'TEST_SUMMARY'


    def do_GET_SEVERITY(self):
        print ''
        SEVERITIES = ('Blocker', 'Critical', 'Major', 'Normal', 'Minor', 'Enhancement')
        DESCRIPTIONS = ('Blocker - blocks development and/or testing work',
                'Critical - crash, loss of data, corruption of data, severe memory leak',
                'Major - major loss of function',
                'Normal - regular issue, some loss of functionality under specific circumstances',
                'Minor - issue that can be viewed as trivial (e.g. cosmetic, UI, easily documented',
                'Enhancement - request for enhancement (do not use it, use features.opensuse.org !)'
                )

        print 'Please describe the impact of the bug, choose a severity for the issue.'
        console.print_list(SEVERITIES, msg='Available severities:')

        yes = console.yes_no('Would you like to see their descriptions? Yes/No')
        if yes:
            console.print_list(DESCRIPTIONS)

        print ''
        idx = console.get_index(len(SEVERITIES), 'Which one?')

        sev = SEVERITIES[idx]
        if sev == 'Enhancement':
            print 'Enhancement is tracked in features.opensuse.org!'
            return 'GET_SEVERITY'

        self.data['severity'] = sev
        return 'GET_DESCRIPTION'


    def do_GET_DESCRIPTION(self):
        print ''
        self.data['description'] = console.edit_message(self.getHeader())
        return 'ASK_SUBMIT'


    def do_ASK_SUBMIT(self):
        print '--------------------------------------------------------------'
        print ''
        print self.getHeader()
        print ''
        print self.data['description']
        print '--------------------------------------------------------------'
        print ''

        yes = console.yes_no('Do you want to submit this report? Yes/No')
        if yes:
            return 'SUBMIT'

        yes = console.yes_no('Bug will not be reported. Do you want to save the report? Yes/No')
        if yes:
            try:
                file_name = self.save()
                print 'Report was saved into %s.' % file_name
            except OSError, oe:
                print oe.args[0]

        return 'EXIT'


    def do_SUBMIT(self):
        print ''
        print 'Submitting the bug report...'
        bug = self.bz.createbug(**self.data)

        print 'You have submitted bug report number %d at %s.' % (bug.id, bug.url)
        return 'EXIT'
