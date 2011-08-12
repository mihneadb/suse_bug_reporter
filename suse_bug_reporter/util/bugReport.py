#!/usr/bin/env python


import os
import pprint
import re

from suse_bug_reporter.gathering_modules.release import gather_from_release
from suse_bug_reporter.util import console, packageInfo, gather
from suse_bug_reporter.util import FSM_def


class BugReport(FSM_def.FSM):

    END_STATES = ('ERROR', 'EXIT', 'NYI')

    def __init__(self, bz, pkg, pkg_info, summary, data={}, interact=1):

        super(BugReport, self).__init__()

        self.bz = bz
        self.data = data
        self.pkg = pkg
        self.pkg_info = pkg_info
        self.data['summary'] = summary
        self.prj = pkg_info[2]
        self.ver = pkg_info[0]
        self.apiurl = pkg_info[1]
        self.interact = interact
        self.products = None
        self.components = None
        self.check_prod = False
        self.check_comp = False


    def _resp(self, suffix=''):
        if self.data:
            return self.data.get(self._state + suffix)
        return None


    def getHeader(self):
        return """Package: %s
Project: %s
Version: %s
Apiurl: %s
Summary: %s
Product: %s
Platform: %s
Component: %s
Severity: %s
Assigned to: %s
CC: %s""" % (self.pkg,
        self.prj,
        self.ver,
        self.apiurl,
        self.data['summary'],
        self.data['product'],
        self.data['rep_platform'],
        self.data['component'],
        self.data['severity'],
        self.data['assigned_to'],
        ', '.join(self.data['cc'])
        )


    def getSysData(self):
        data = gather.gather_data(gather.gather_from)
        return 'Automatically gathered system data:\n' + pprint.pformat(data)


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
        
        if not self.interact:
            self.data['product'] = console.custom_input(msg="Product (or '?' for a list): ", preselect=product).strip()
            if self.data['product'] == '?':
                return "SELECT_PRODUCT_PLATFORM"
            self.data['rep_platform'] = console.custom_input(msg="Platform: ", preselect=platform)
            return "TEST_PRODUCT_PLATFORM"
        
        print 'Found %s.' % full_name
        correct = console.yes_no('Is that the correct product & platform? yes/no')

        if correct:
            self.data['product'] = product
            self.data['rep_platform'] = platform
            return 'TEST_PRODUCT_PLATFORM'

        return 'ASK_PRODUCT_PLATFORM'


    def do_ASK_PRODUCT_PLATFORM(self):
        print ''
        print "Enter the name + version of the openSUSE product, or enter 's'"\
                " if you want to  select it from a list."
        ans = raw_input('Answer: ')

        if ans in ('s', 'S'):
            return 'SELECT_PRODUCT_PLATFORM'

        self.data['product'] = ans
        return 'GET_PLATFORM'


    def do_GET_PLATFORM(self):     
        print ''
        aux1, platform, aux2 = gather_from_release()
        ans = console.custom_input(msg='Platform: ', preselect=platform)
        self.data['rep_platform'] = ans

        return 'TEST_PRODUCT_PLATFORM'


    def do_SELECT_PRODUCT_PLATFORM(self):
        print ''
        print 'Getting list of products from Bugzilla...'

        if self.products is None:
            tmp = self.bz.getproducts()
            self.products = [p['name'] for p in tmp]
            self.products.sort()

        console.print_list(self.products, columns=2, msg='Available products:')
        idx = console.get_index(len(self.products), msg='Which one?')

        self.data['product'] = self.products[idx]

        return 'GET_PLATFORM'


    def do_TEST_PRODUCT_PLATFORM(self):
        print ''
        if self.data['rep_platform'] == '':
            self.data['rep_platform'] = 'All'

        if self.data['product'] == '':
            print 'You have to select a product!'
            return 'SELECT_PRODUCT_PLATFORM'

        if self.check_prod:
            return 'CHECK'
        return 'GET_COMPONENT'


    def do_GET_COMPONENT(self, components=None):
        if not self.interact and self.components is None:
            ans = raw_input("Component (or '?' for a list): ").strip()
            if ans is '':
                print 'Component cannot be blank.'
            if ans != '?' and ans is not '':
                self.data['component'] = ans
                if self.data['component'] == 'Security':
                    return 'GET_SECURITY_PREFIX'
                return 'GET_VERSION'

        if self.components is None:
            try:
                print ''
                print 'Getting list of components from Bugzilla for product %s.' % self.data['product']
                self.components = self.bz.getcomponents(self.data['product'])
            except ValueError:
                print 'The product you have entered is invalid. Please select a correct one.'
                return 'SELECT_PRODUCT_PLATFORM'

        # list is already sorted
        console.print_list(self.components, columns=2, msg='Available components:')
        print ''
        try:
            idx = self.components.index('Security')
            print "If it's a security problem, please select index %d (Security)." % (idx + 1)
        except ValueError:
            pass
        idx = console.get_index(len(self.components), msg='Which one?')

        print 'Using component %s.' % self.components[idx]
        self.data['component'] = self.components[idx]

        if self.data['component'] == 'Security':
            return 'GET_SECURITY_PREFIX'

        if self.check_comp:
            return 'CHECK'
        return 'GET_VERSION'


    def do_GET_SECURITY_PREFIX(self):
        print ''
        msg = "Is this needed to be fixed now, or on the next main update?"
        idx = console.choice(msg, 'urgently', 'next_update')
        if idx == 0:
            self.data['summary'] = 'VUL-0 ' + self.data['summary']
        else:
            self.data['summary'] = 'VUL-1 ' + self.data['summary']
        
        if self.check_comp:
            return 'CHECK'
        return 'GET_VERSION'


    def do_GET_VERSION(self):
        if not self.interact:
            ans = raw_input("Product version (or '?' for a list): ").strip()
            if ans != '?' and ans is not '':
                self.data['version'] = ans
                return 'LOAD_ASSIGNEE'
            if ans is '':
                print 'Version cannot be blank!'
        
        print ''
        VERSIONS = ('Final', 'Factory', 'unspecified')
        print 'Please select the version of the OS you are using.'

        console.print_list(VERSIONS, msg='Available choices:')
        idx = console.get_index(len(VERSIONS), msg='Which one?')

        self.data['version'] = VERSIONS[idx]
        
        return 'LOAD_ASSIGNEE'


    def do_LOAD_ASSIGNEE(self):
        print ''
        print 'Getting assignee & cc list, please wait...'
        assignee, cc = packageInfo.getAssignedPersons(self.pkg_info)

        if self.data['component'] == 'Security':
            cc.append('security-team@suse.de')
        
        if not self.interact:
            assignee = console.custom_input(msg='Assignee: ', preselect=assignee)
            cc = re.split(r',* *', console.custom_input(msg="CC (separated by ','): ", preselect=", ".join(cc)))
            self.data['assigned_to'] = assignee
            self.data['cc'] = cc
            return 'TEST_SUMMARY'
        
        print 'This/these address(es) were found:'
        print 'assignee: ' + assignee
        print 'cc: ',
        pprint.pprint(cc)

        yes = console.yes_no('Do you want to change the assignee? Yes/No')
        if yes:
            assignee = console.custom_input('New assignee: ', preselect=assignee)
            print 'Chose %s as assignee.' % assignee

        print ''
        if len(cc) > 0:
            yes = console.yes_no('Do you want to remove anybody from the cc list'\
                                 ' (one at a time)? Yes/No')
            while yes:
                console.print_list(cc, msg='Available choices')
                idx = console.get_index(len(cc), msg='Which one?')
                del cc[idx]
                print ''
                yes = console.yes_no('Do you want to remove another person? Yes/No')

        print ''
        yes = console.yes_no('Do you want to add another cc(s)? Yes/No')
        if yes:
            print ''
            print 'Enter their e-mail addresses, one at a time.'
            print "To stop, enter something that does not contain '@'."
            ans = raw_input('Cc: ')
            while '@' in ans:
                cc.append(ans)
                ans = raw_input('Cc: ')
            print 'new cc list: '
            pprint.pprint(cc)

        self.data['assigned_to'] = assignee
        self.data['cc'] = cc

        return 'TEST_SUMMARY'


    def do_TEST_SUMMARY(self):
        print ''
        if self.data['summary'].strip() == '':
            return 'GET_SUMMARY'

        return 'CHECK_PKG_IN_SUMMARY'


    def do_GET_SUMMARY(self):
        print ''
        print "Summary can't be empty! Please enter a short description "\
                    "of the bug you are reporting"
        ans = raw_input('--> ')
        self.data['summary'] = ans

        return 'TEST_SUMMARY'


    def do_CHECK_PKG_IN_SUMMARY(self):
        if self.pkg not in self.data['summary']:
            self.data['summary'] = '[' + self.pkg + '] ' + self.data['summary']
            print 'Package name was not found in summary. It was added automatically.'
            print 'Summary is: ' + self.data['summary']

        return 'GET_SEVERITY'


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
        console.print_list(DESCRIPTIONS, msg='Available severities:')

        idx = console.get_index(len(SEVERITIES), 'Which one?')

        sev = SEVERITIES[idx]
        if sev == 'Enhancement':
            print 'Enhancement is tracked in features.opensuse.org!'
            return 'GET_SEVERITY'

        self.data['severity'] = sev
        return 'GET_DESCRIPTION'


    def do_GET_DESCRIPTION(self):
        print ''
        self.data['description'] = self.getHeader() + '\n\n' + console.edit_message(self.getHeader())
        yes = console.yes_no('Do you want to add an automatically gathered'\
                ' system description? Yes/No')
        if yes:
            self.data['description'] += '\n\n' + self.getSysData() + '\n'
        return 'ASK_SUBMIT'


    def do_ASK_SUBMIT(self):
        print '--------------------------------------------------------------'
        print ''
        print self.data['description']
        print '--------------------------------------------------------------'
        print ''

        yes = console.yes_no('Do you want to submit this report? Yes/No')
        if yes:
            print ''
            print 'Please wait, checking validity of product and component.'
            return 'CHECK'

        yes = console.yes_no('Bug will not be reported. Do you want to save the report? Yes/No')
        if yes:
            try:
                file_name = self.save()
                print 'Report was saved into %s.' % file_name
            except OSError, oe:
                print oe.args[0]

        return 'EXIT'


    def do_CHECK(self):
        '''Check validity of product and component for less interactive mode'''
        
        # checking product
        if self.products is None:
            tmp = self.bz.getproducts()
            self.products = [p['name'] for p in tmp]
            self.products.sort()
        
        OK = False
        for prod in self.products:
            if self.data['product'] == prod:
                OK = True
                break
            elif self.data['product'].lower() == prod.lower():
                self.data['product'] = prod
                print 'Product automatically corrected to %s.' % prod
                OK = True
                break
        if not OK:
            print ''
            print 'You have selected an invalid product.'
            self.check_prod = True
            return 'SELECT_PRODUCT_PLATFORM'
        
        # checking component
        if self.components is None:
            self.components = self.bz.getcomponents(self.data['product'])
        
        OK = False
        for comp in self.components:
            if self.data['component'] == comp:
                OK = True
                break
            elif self.data['component'].lower() == comp.lower():
                self.data['component'] = comp
                print 'Component automatically corrected to %s.' % comp
                OK = True
                break
        if not OK:
            print 'You have selected an invalid component.'
            self.check_comp = True
            return 'GET_COMPONENT'
        
        return 'SUBMIT'


    def do_SUBMIT(self):
        print ''
        print 'Submitting the bug report...'
        #bug = self.bz.createbug(**self.data) doesn't seem to work properly
        try:
            bug = self.bz._createbug(**self.data)
        except:
            print 'The data you have entered is invalid to create a bug report.'
            print 'Please use the interactive mode of this tool. (run it with no arguments)'
        else:
            print 'You have submitted bug report number #%d' % bug

        #print 'You have submitted bug report number %d at %s.' % (bug.id, bug.url)
        return 'EXIT'
