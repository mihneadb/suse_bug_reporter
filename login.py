#!/usr/bin/env python

import curl
import pycurl
import sys

import urllib
import urllib2

test = curl.Curl()

tup = (('login', sys.argv[1]), ('password', sys.argv[2]))

# try to login
#test.post("https://bugzilla.novell.com/ICSLogin/auth-up", tup)
# try to login 2
values = {'user': sys.argv[1],
        'password': sys.argv[2]}
data = urllib.urlencode(values)
url = "https://bugzilla.novell.com/ICSLogin/auth-up"
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

the_page = response.read()

print the_page

