#!/usr/bin/env python

# provides login into Novell Bugzilla
# stores credentials in a file

class Credentials:
    ''' container for the user's credentials '''
    def __init__(self, username, password, cookie):
        self.username = username
        self.password = password
        self.cookie = cookie

import httplib
import sys
import os
import base64
import cPickle

from getpass import getpass


# command-line arguments
if len(sys.argv) > 1:

    if sys.argv[1] == '--clear':
        # delete the credentials file
        try:
            os.remove('.sbr')
        except OSError:
            pass
        sys.exit(0)

    elif sys.argv[1] == '--help':
        # show help / usage message
        print 'Usage:'
        print '--clear  cleares stored credentials (if any)'
        print '--help   shows this message'
        sys.exit(0)


auth_url = '/ICSLogin/auth-up'

# check to see if the credentials are already stored
try:
    # load the file, decode the string and load the serialized object
    creds_file = open('.sbr', 'r')
    data = creds_file.read()
    data = base64.b64decode(data)
    creds = cPickle.loads(data)
    print 'The user has stored credentials.'

except IOError:
    # no file found, get username & password
    print 'No credentials stored, please log in.'
    print 'No account? -> https://secure-www.novell.com/selfreg/jsp/createAccount.jsp'
    username = raw_input('Enter username: ')
    password = getpass('Enter password: ')

    # try to login
    connection = httplib.HTTPSConnection('bugzilla.novell.com')
    login_string = "username=%s&password=%s" % (username, password)

    connection.request("POST", auth_url, login_string)
    response = connection.getresponse()

    if response.status == 200:
        print 'Wrong login credentials!'
        print 'If you haven\'t got an account, please register here:'
        print 'https://secure-www.novell.com/selfreg/jsp/createAccount.jsp'

        fail = 1

    else:
        headers = response.getheaders()
        cookie = (headers[1])[1]
        creds = Credentials(username, password, cookie)

        data = cPickle.dumps(creds)
        data = base64.b64encode(data)

        creds_file = open('.sbr', 'w')
        creds_file.write(data)
        creds_file.close()


# testing purposes
if not fail:
    print creds.username
    print creds.cookie
