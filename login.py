#!/usr/bin/env python

import httplib
import sys

url = '/ICSLogin/auth-up'

conn = httplib.HTTPSConnection('bugzilla.novell.com')
string = "username=%s&password=%s" % (sys.argv[1], sys.argv[2])

conn.request("POST", url, string)
response = conn.getresponse()

if response.status == 200:
    print 'Wrong login credentials!'
else:
    h = response.getheaders()
    print 'Login successful! - cookie is %s' % (str((h[1])[1]))
