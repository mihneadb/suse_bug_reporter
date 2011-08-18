def test_find_app():
    from bugreporter.aid_user.find_app import find_app

    resp = "WM_CLASS(STRING) = \"konsole\", \"Konsole\""
    
    ans = find_app(resp)
    assert ans == "The app's name is konsole."


def test_which():
    from bugreporter.aid_user.find_package import which

    try:
        ans = which('/some/path/exec')
    except AssertionError:
        pass

    ans = which('ls')
    assert ans == '/bin/ls'

    ans = which('asdfgh')
    assert ans == None


def test_get_package():
    from bugreporter.aid_user.find_package import get_package

    try:
        ans = get_package('relative/path')
    except AssertionError:
        pass

    ans = get_package('/bin/ls')
    assert ans == 'coreutils'

    ans = get_package('/some/exec')
    assert ans == None


def test_find_package():
    from bugreporter.aid_user.find_package import find_package
    
    ans = find_package('ls')
    assert ans == 'The package for /bin/ls is coreutils.'

    ans = find_package('/bin/ls')
    assert ans == 'The package for /bin/ls is coreutils.'

    ans = find_package('asdfg')
    assert ans == None

    ans = find_package('/asd/fgh')
    assert ans == None
