#!/usr/bin/env python

import rpm


def getVersion(header):

    version = ''

    for key in ('epoch', 'version', 'release'):
        if header[key] == None:
            continue
        if version != '':
            version += '-'
        version += header[key]

    return version

def getApiURL(disturl):

    disturl = disturl.split('/')
    disturl = disturl[2].split('.')
    apiurl = '.'.join(disturl[1:])
    apiurl = 'https://api.' + apiurl

    return apiurl

def getProject(disturl):

    disturl = disturl.split('/')

    return disturl[3]

def getInfo(package):
    ''' returns a dictionary with a tuple associated to each package
    the tuple is like this: (version, apiurl, project, package) '''
    
    ts = rpm.TransactionSet()
    
    ret = {}

    for symbol in ('name', 'provides'):

        match = ts.dbMatch(symbol, package)
        for header in match:
            disturl = header['disturl']
            version = getVersion(header)
            if '.pm.' in version:
                apiurl = None
                project = 'Packman'
            else:
                apiurl = getApiURL(disturl)
                project = getProject(disturl)

            ret[header['name']] = (version, apiurl, project, package)

    ts.clean()
    ts.closeDB()

    return ret

print getInfo('gstreamer')
