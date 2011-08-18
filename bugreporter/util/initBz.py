import bugzilla
from bugreporter.util import login

def initBugzilla():
    #check login
    (username, password) = login.getCreds()
    
    print "Connecting to Novell's Bugzilla..."

    #instantiate the bz object
    bugzillaURL = 'https://bugzilla.novell.com/xmlrpc.cgi'
    cls = bugzilla.getBugzillaClassForURL(bugzillaURL)
    bz = cls(url=bugzillaURL, user=username, password=password)

    return bz
