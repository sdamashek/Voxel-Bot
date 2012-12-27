#!/usr/bin/env python

# These tests access the network.

import unittest, string, os
from unittest import TestCase
import urllib2

import ClientCookie
from ClientCookie import build_opener, install_opener, urlopen, urlretrieve
from ClientCookie import CookieJar, HTTPCookieProcessor, \
     HTTPHandler, HTTPRefreshProcessor, \
     HTTPEquivProcessor, HTTPRedirectHandler, \
     HTTPRedirectDebugProcessor, HTTPResponseDebugProcessor

#from cookielib import CookieJar
#from urllib2 import build_opener, install_opener, urlopen
#from urllib2 import HTTPCookieProcessor, HTTPHandler

#from ClientCookie import CreateBSDDBCookieJar

try: True
except NameError:
    True = 1
    False = 0


## logger = ClientCookie.getLogger("ClientCookie")
## logger.addHandler(ClientCookie.StreamHandler())
## logger.setLevel(ClientCookie.DEBUG)

class FunctionalTests(TestCase):
    def test_clientcookie(self):
        # XXX set up test page on SF or python.org
        # this test page depends on cookies, and an http-equiv refresh
        #cj = CreateBSDDBCookieJar("/home/john/db.db")
        cj = CookieJar()
        handlers = [
            HTTPCookieProcessor(cj),
            HTTPRefreshProcessor(max_time=None, honor_time=False),
            HTTPEquivProcessor(),

            HTTPRedirectHandler(),  # needed for Refresh handling in 2.4.0
#            HTTPHandler(True),
#            HTTPRedirectDebugProcessor(),
#            HTTPResponseDebugProcessor(),
            ]

        o = apply(build_opener, handlers)
        try:
            install_opener(o)
            try:
                r = urlopen("http://wwwsearch.sf.net/cgi-bin/cookietest.cgi")
            except urllib2.URLError, e:
                #print e.read()
                raise
            data = r.read()
            #print data
            self.assert_(
                string.find(data, "Your browser supports cookies!") >= 0)
            self.assert_(len(cj) == 1)

            # test response.seek() (added by HTTPEquivProcessor)
            r.seek(0)
            samedata = r.read()
            r.close()
            self.assert_(samedata == data)
        finally:
            o.close()
            # uninstall opener (don't try this at home)
            ClientCookie._urllib2_support._opener = None

    def test_urlretrieve(self):
        url = "http://www.python.org/"
        verif = CallbackVerifier(self)
        fn, hdrs = urlretrieve(url, "python.html", verif.callback)
        try:
            f = open(fn)
            data = f.read()
            f.close()
        finally:
            os.remove(fn)
        r = urlopen(url)
        self.assert_(data == r.read())
        r.close()

##     def test_cacheftp(self):
##         from urllib2 import CacheFTPHandler, build_opener
##         o = build_opener(CacheFTPHandler())
##         r = o.open("ftp://ftp.python.org/pub/www.python.org/robots.txt")
##         data1 = r.read()
##         r.close()
##         r = o.open("ftp://ftp.python.org/pub/www.python.org/2.3.2/announce.txt")
##         data2 = r.read()
##         r.close()
##         self.assert_(data1 != data2)

class CallbackVerifier:
    # for .test_urlretrieve()
    def __init__(self, testcase):
        self._count = 0
        self._testcase = testcase
    def callback(self, block_nr, block_size, total_size):
        if block_nr != self._count:
            self._testcase.fail()
        self._count = self._count + 1


class ResponseTests(TestCase):
    def test_response_close_and_read(self):
        opener = ClientCookie.build_opener(ClientCookie.SeekableProcessor)
        r = opener.open("http://wwwsearch.sf.net/bits/cctest2.txt")
        # closing response shouldn't stop methods working if we're using
        # SeekableProcessor (ie. _Util.response_seek_wrapper)
        r.read()
        r.close()
        r.seek(0)
        self.assertEqual(r.read(), "Hello ClientCookie functional test suite.\n")


if __name__ == "__main__":
    unittest.main()
