'''
Copyright (C) 2011  Mihnea Dobrescu-Balaur

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import sys
import re
import rpm
import urllib2
import osc.conf
import osc.core

from subprocess import Popen, PIPE

from bugreporter.util.console import yes_no, print_list, get_index
from bugreporter.aid_user.find_package import which

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


def getInfo(package):
    ''' returns a tuple associated to the package selected by the user
    the tuple is like this: (version, apiurl, project, package) 
    !! supports globbing. if called with 'python*', it will search all the
    packages that match python*. if called with 'python', it will do exact
    matching 
    !! if there is more than one package matched, the user must choose one '''

    #check to see if the user wants globbing
    glob = 0
    if package[-1] == '*':
        glob = 1;


    ts = rpm.TransactionSet()
    
    ret = {}

    #regex stuff for parsing the disturl
    bs_re = re.compile(r"^(?P<bs>.*)://(?P<apiurl>.*?)/(?P<project>.*?)/"\
            "(?P<repository>.*?)/(?P<md5>[a-f0-9]*)-(?P<source>.*)$")
    srcrep_re = re.compile(r"^srcrep:(?P<md5>[a-f0-9]*)-(?P<source>.*)$")


    for symbol in ('name', 'provides', 'basenames'):

        if symbol == 'basenames':
            if len(ret.keys()) > 0:
                # a package was already found, no need to look for owner of executable
                break

            if '/' not in package:
                abs = which(package)
                if abs is None:
                    break
                
                package = abs

        #to match all packages, with globbing!
        if not glob:
            match = ts.dbMatch(symbol, package)
        else:
            match = ts.dbMatch()
            match.pattern(symbol, rpm.RPMMIRE_GLOB, package)

        for header in match:
            disturl = header['disturl']
            version = getVersion(header)

            if '.pm.' in version:
                apiurl = None
                project = 'Packman'
                ret[header['name']] = (version, apiurl, project, header['name'])
                continue

            if disturl:
                m = srcrep_re.match(disturl)
                if m:
                    ret[header['name']] = (version,
                            apiurl,
                            header['distribution'].split('/')[0].strip(),
                            m.group('source'))

                m = bs_re.match(disturl)
                if m:
                    apiurl = m.group('apiurl')
                    if apiurl.split('.')[0] != 'api':
                        apiurl = apiurl.split('.')
                        apiurl = 'https://api.' + '.'.join(apiurl[1:])
                    ret[header['name']] = (version,
                            apiurl,
                            m.group('project'),
                            m.group('source'))
            else:
                ret[header['name']] = (version,
                        None,
                        header['distribution'].split('/').strip(),
                        header['name'])

    ts.clean()
    ts.closeDB()

    keys = ret.keys()
    length = len(keys)
    if length == 0:
        return None
        
    elif length == 1:
        ret = ret[keys[0]]

    elif length > 1:
        # there are more than one packages that match, the user must pick one
        msg = 'There are more than one packages that match your search'\
                ', please pick one'
        print_list(keys, msg=msg, columns=2)
        print ''
        idx = get_index(length, 'Which one?')
        ret = ret[keys[idx]]

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
    
    for person in tree.findall('person'):
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


def getAssignedPersons(pkg_info):
    ''' takes as argument a tuple returned by the getInfo() function;
    returns a tuple with the list of emails for the persons associated
    with the input_package '''

    #init
    try:
        osc.conf.get_config()
    except osc.oscerr.NoConfigfile:
        print 'You have to have a valid .oscrc file. Please do so by running osc.'
        sys.exit(1)

    (version, apiurl, project, package) = pkg_info  

    if project == 'Packman':
        print 'Packman is not supported.'
        sys.exit(1)

    prj_data = getProjectData(apiurl, project)
    if prj_data == None:
        print "Project %s doesn't exist!" % (project)
        sys.exit(1)

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

