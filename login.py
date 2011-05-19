#!/usr/bin/env python

# provides login into Novell Bugzilla
# stores credentials in a file

class credentials:
    ''' container for the user's credentials '''
    def __init__(self, username, password, cookie):
        self.username = username
        self.password = password
        self.cookie = cookie

import httplib
import sys
import base64
import cPickle

from getpass import getpass

auth_url = '/ICSLogin/auth-up'

# check to see if the credentials are already stored
try:
    creds_file = open('.sbr', 'r')
    data = creds_file.read()
    data = base64.b64decode(data)
    creds = cPickle.loads(data)
    print 'The user has stored credentials.'

except IOError:
    # no file found
    print 'No credentials stored, please log in.'
    username = raw_input('Enter username: ')
    password = getpass('Enter password: ')

    connection = httplib.HTTPSConnection('bugzilla.novell.com')
    login_string = "username=%s&password=%s" % (username, password)

    connection.request("POST", auth_url, login_string)
    response = connection.getresponse()

    if response.status == 200:
        print 'Wrong login credentials!'

    else:
        headers = response.getheaders()
        cookie = (headers[1])[1]
        creds = credentials(username, password, cookie)

        data = cPickle.dumps(creds)
        data = base64.b64encode(data)

        creds_file = open('.sbr', 'w')
        creds_file.write(data)
        creds_file.close()


# testing purposes
print creds.username
print creds.cookie
