#!/usr/bin/env python

import sys
import rpm
import urllib2
import osc.conf
import osc.core

try:
    from xml.etree import cElementTree as ET
except ImportError:
    import cElementTree as ET



def getVersion(header):
    ''' returns a string that represents the package's version '''
    version = ''

    for key in ('epoch', 'version', 'release'):
        if header[key] == None:
            continue
        if version != '':
            version += '-'
        version += header[key]

    return version


def getApiURL(disturl):
    ''' returns a string that represents the package's apiurl '''
    disturl = disturl.split('/')
    disturl = disturl[2].split('.')
    apiurl = '.'.join(disturl[1:])
    apiurl = 'https://api.' + apiurl

    return apiurl


def getProject(disturl):
    ''' returns a string that represents the package's project name '''
    disturl = disturl.split('/')

    return disturl[3]


def getInfo(package):
    ''' returns a dictionary with a tuple associated to each package
    the tuple is like this: (version, apiurl, project, package) 
    !! supports globbing. if called with 'python*', it will search all the
    packages that match python*. if called with 'python', it will do exact
    matching '''

    #check to see if the user wants globbing
    glob = 0
    if package[-1] == '*':
        glob = 1;
        package = package[:-1]


    ts = rpm.TransactionSet()
    
    ret = {}

    for symbol in ('name', 'provides'):

        #to match all packages, with globbing!
        if not glob:
            match = ts.dbMatch(symbol, package)
        else:
            match = ts.dbMatch()
            match.pattern(symbol, rpm.RPMMIRE_GLOB, package + '*')

        for header in match:
            disturl = header['disturl']
            version = getVersion(header)
            if '.pm.' in version:
                apiurl = None
                project = 'Packman'
            else:
                apiurl = getApiURL(disturl)
                project = getProject(disturl)

            ret[header['name']] = (version, apiurl, project, header['name'])

    ts.clean()
    ts.closeDB()

    if ret == {}:
        return None

    return ret


def getProjectData(apiurl, project):
    ''' returns the xml-formatted data that represents the project, if it
    exists. Otherwise, it returns None '''

    try:
        data = osc.core.meta_exists(metatype='prj',
                path_args=(osc.core.quote_plus(project)),
                apiurl=apiurl,
                create_new=False) #not sure what create_new=False does!
    except urllib2.HTTPError:
        return None

    return data


def getPackageData(apiurl, project, package):
    ''' returns the xml-formatted data that represents the package, if it
    exists. Otherwise, it returns None '''

    try:
        data = osc.core.meta_exists('pkg',
                path_args=(osc.core.quote_plus(project),
                    osc.core.quote_plus(package)),
                apiurl=apiurl,
                create_new=False) #not sure what create_new=False does!
    except urllib2.HTTPError:
        return None

    return data


def getDevelPnP(tree):
    ''' returns the name of the devel package and the corresponding project,
    if available; else, returns the default package & project name '''

    package = tree.get('name')
    project = tree.get('project')

    devel = tree.find('devel')

    if devel != None:
        if 'package' in devel.keys():
            package = devel.get('package')
        project = devel.get('project')

    return (project, package)


def getMail(apiurl, userid):
    ''' returns a string with the user's (userid) email '''
    return osc.core.get_user_data(apiurl, userid, 'email')[0]


def getPersons(apiurl, tree):
    ''' returns a list of tuples like (email, role) '''
    ret = []
    
    for person in tree.iter('person'):
        mail = getMail(apiurl, person.get('userid'))
        role = person.get('role')

        ret.append((mail, role))

    if not ret:
        return None
    return ret


def getBugownersMail(persons):
    ''' returns a list of emails as strings '''
    return [p[0] for p in persons if p[1] == 'bugowner']


def getMaintainersMail(persons):
    ''' returns a list of emails as strings '''
    return [p[0] for p in persons if p[1] == 'maintainer']


def getMailsTuple(persons):
    ''' returns a tuple like (assignee, cc) - cc is a list '''

    #default
    assignee = 'bnc-team-screening@forge.provo.novell.com'
    cc = []

    bugowners = getBugownersMail(persons)
    maintainers = getMaintainersMail(persons)

    if len(bugowners) > 0:
        # assign the report to the first one, all the rest will be cc'd
        assignee = bugowners[0]

    elif len(maintainers) > 0:
        # the same as above
        assignee = maintainers[0]

    cc = [mail for mail in (bugowners + maintainers) if mail != assignee]

    return (assignee, cc)


def getAssignedPersons(input_package):

    #init
    osc.conf.get_config()

    pkg_info = getInfo(input_package)
    if pkg_info == None:
        # no package found
        print "No package found, maybe try adding the '*' character?"
        sys.exit(1)

    keys = pkg_info.keys()
    
    if len(keys) == 1:
        (version, apiurl, project, package) = pkg_info[keys[0]]
    
    else:
        # there are more than one packages that match, the user must pick one
        print "There are more than one packages that match your search, please pick one"
        for p in range(len(keys)):
            print '%4d %40s\t' % (p, keys[p]),
            if p%2 == 1:
                print ''

        idx = int(raw_input("\nWhich one? "))
        (version, apiurl, project, package) = pkg_info[keys[idx]]

    prj_data = getProjectData(apiurl, project)
    if prj_data == None:
        print "Project %s doesn't exist!" % (project)
        return None

    pkg_data = getPackageData(apiurl, project, package)
    if pkg_data == None:
        print "Package %s doesn't exist in project %s!" % (package, project)
        return None

    tree = ET.fromstring(''.join(pkg_data))
    devel_prj, devel_pkg = getDevelPnP(tree)

    if (devel_prj, devel_pkg) != (project, package):
        # need to load data for the devel project in order to get the real
        # maintainer

        prj_data = getProjectData(apiurl, devel_prj)
        if prj_data == None:
            # no meta for the devel project
            pass

        else:
            pkg_data = getPackageData(apiurl, devel_prj, devel_pkg)
            if pkg_data == None:
                # no meta for the devel package
                pass

            else:
                tree = ET.fromstring(''.join(pkg_data))
                project, package = devel_prj, devel_pkg

    persons = getPersons(apiurl, tree)
    if persons == None:
        tree = ET.fromstring(''.join(prj_data))
        persons = getPersons(apiurl, tree)

    return getMailsTuple(persons)




# testing purposes

if __name__ == '__main__':
    print getAssignedPersons(sys.argv[1])
