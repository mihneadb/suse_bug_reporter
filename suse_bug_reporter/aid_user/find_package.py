import os.path
import rpm


def which(executable):
    ''' returns absolute path to program's executable, or None if it's not found '''

    assert '/' not in executable

    PATH = ('/bin', '/sbin', '/usr/bin', '/usr/sbin')

    for d in PATH:
        abs_path = os.path.join(d, executable)
        if os.path.exists(abs_path):
            return abs_path
    return None


def get_package(abs_path):
    ''' returns the package (if it exists) for the executable found at the
        abs path given. '''
    assert os.path.isabs(abs_path)

    ts = rpm.TransactionSet()
    match = ts.dbMatch('basenames', abs_path)

    pkg = None
    for header in match:
        pkg = header['name']

    return pkg


def find_package(resp=None):
    '''Returns a tuple of two items - the first is the printable output for the user;
    The second is the actual path to the package'''

    print "Which binary's package do you want to find?"
    print 'You can enter either its name or its absolute path.'

    if resp != None:
        name = resp
    else:
        name = raw_input('--> ')
        name = name.strip()
    
    # check if this is absolute path
    if not os.path.isabs(name):
        name = which(name)
        if name == None:
            return None

    pkg = get_package(name)
    
    if pkg == None:
        return None

    return ('The package for %s is %s.' % (name, pkg), pkg)
