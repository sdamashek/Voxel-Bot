#!/usr/bin/env python
"""Client-side HTTP cookie handling.

ClientCookie is a Python module for handling HTTP cookies on the
client side, useful for accessing web sites that require cookies to be
set and then returned later.  It also provides some other (optional)
useful stuff: HTTP-EQUIV and Refresh handling, automatic adding of the
Referer [sic] header, robots.txt observance and lazily-seek()able
responses.  These extras are implemented using an extension that makes
it easier to add new functionality to urllib2 (now part of urllib2, as
of Python 2.4).  It has developed from a port of Gisle Aas' Perl
module HTTP::Cookies, from the libwww-perl library.
"""

try: True
except NameError:
    False, True = 0, 1

import re
#VERSION_MATCH = re.search(r'VERSION = "(.*)"', open("ClientCookie/_ClientCookie.py").read())
#VERSION = VERSION_MATCH.group(1)
VERSION = '1.3.0'
INSTALL_REQUIRES = []
NAME = "ClientCookie"
PACKAGE = True
LICENSE = "BSD"  # or ZPL 2.1
PLATFORMS = ["any"]
ZIP_SAFE = True
CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
License :: OSI Approved :: Zope Public License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: System :: Networking :: Monitoring
Topic :: System :: Systems Administration
"""

#-------------------------------------------------------
# the rest is constant for most of my released packages:

import sys

if PACKAGE:
    packages, py_modules = [NAME], None
else:
    packages, py_modules = None, [NAME]

doclines = __doc__.split("\n")

if not hasattr(sys, "version_info") or sys.version_info < (2, 3):
    from distutils.core import setup
    _setup = setup
    def setup(**kwargs):
        ignore_keys = [
            # distutils >= Python 2.3 args
            # XXX probably download_url came in earlier than 2.3
            "classifiers", "download_url",
            # setuptools args
            "install_requires", "zip_safe", "test_suite",
            ]
        if sys.version_info < (2, 1):
            ignore_keys.append("platforms")
        for key in ignore_keys:
            if kwargs.has_key(key):
                del kwargs[key]
        # Only want packages keyword if this is a package,
        # only want py_modules keyword if this is a single-file module,
        # so get rid of packages or py_modules keyword as appropriate.
        if kwargs["packages"] is None:
            del kwargs["packages"]
        else:
            del kwargs["py_modules"]
        apply(_setup, (), kwargs)
else:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

setup(
    name = NAME,
    version = VERSION,
    license = LICENSE,
    platforms = PLATFORMS,
    classifiers = [c for c in CLASSIFIERS.split("\n") if c],
    install_requires = INSTALL_REQUIRES,
    zip_safe = ZIP_SAFE,
    test_suite = "test",
    author = "John J. Lee",
    author_email = "jjl@pobox.com",
    description = doclines[0],
    long_description = "\n".join(doclines[2:]),
    url = "http://wwwsearch.sourceforge.net/%s/" % NAME,
    download_url = ("http://wwwsearch.sourceforge.net/%s/src/"
                    "%s-%s.tar.gz" % (NAME, NAME, VERSION)),
    py_modules = py_modules,
    packages = packages,
    )
