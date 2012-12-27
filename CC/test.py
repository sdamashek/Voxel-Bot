#!/usr/bin/env python

"""Test runner.

To run tests against installed code rather than files extracted from package,
use the -i command line option.

For further help, enter this at a command prompt:

python test.py --help

"""

import sys, string

from ClientCookie._Util import startswith

# Modules containing tests to run -- a test is anything named *Tests, which
# should be classes deriving from unittest.TestCase.
MODULE_NAMES = ["test_misc", "test_date", "test_headers", "test_cookies",
                "test_urllib2"]

## import sys
## sys.setrecursionlimit(50)

import os, traceback
from unittest import TestCase

try: True
except NameError:
    True = 1
    False = 0

import ClientCookie
level = ClientCookie.DEBUG
#level = ClientCookie.INFO
#level = ClientCookie.NOTSET
#ClientCookie.getLogger("ClientCookie").setLevel(level)

RUN_AGAINST_INSTALLED = False

def import_tests(module_names):
    """Import everything named *Tests from named modules.

    This is so unittest.main() will run test cases in other modules.

    """
    try:
        from ClientCookie._Util import endswith
    except ImportError:
        traceback.print_exc()
        if RUN_AGAINST_INSTALLED:
            sys.exit("Perhaps ClientCookie isn't installed properly?")
        else:
            sys.exit("Perhaps the locally extracted source files aren't in "
                     "this directory?")

    g = globals()
    for module_name in module_names:
        try:
            __import__(module_name)
        except ImportError:
            traceback.print_exc()
            sys.exit("Import of test module failed -- Couldn't find tests?")
        module = sys.modules[module_name]
        candidates = dir(module)
        for name in candidates:
            if endswith(name, "Tests"):
                test_class = getattr(module, name)
                g[name] = test_class


if __name__ == "__main__":
    import unittest
    test_path = os.path.join(os.path.dirname(sys.argv[0]), "test")
    try:
        i = sys.argv.index("-i")
    except ValueError:
        RUN_AGAINST_INSTALLED = False
        sys.path.insert(0, test_path)
    else:
        del sys.argv[i]
        RUN_AGAINST_INSTALLED = True
        sys.path[0] = test_path
    import_tests(MODULE_NAMES)
    unittest.main()
