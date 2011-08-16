#!/usr/bin/env python

import bugzilla
from getpass import getpass

bugzillaURL = 'https://bugzilla.novell.com/xmlrpc.cgi'


user = raw_input('Insert user name: ')
password = getpass('Insert password: ')


cls = bugzilla.getBugzillaClassForURL(bugzillaURL)
bz = cls(url=bugzillaURL, user=user, password=password)

