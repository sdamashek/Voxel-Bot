   [1]SourceForge.net Logo

                                 ClientCookie

   Please read [2]this note explaining the relationship between
   ClientCookie, cookielib and urllib2, and which to use when.

   ClientCookie is a [3]Python module for handling HTTP cookies on the
   client side, useful for accessing web sites that require cookies to be
   set and then returned later. It also provides some other (optional)
   useful stuff: HTTP-EQUIV and Refresh handling, automatic adding of the
   Referer [[4]sic] header, automatic observance of robots.txt and
   lazily-seek()able responses. These extras are implemented using an
   extension that makes it easier to add new functionality to urllib2. It
   has developed from a port of Gisle Aas' Perl module HTTP::Cookies,
   from the [5]libwww-perl library.
 import ClientCookie
 response = ClientCookie.urlopen("http://foo.bar.com/")

   This function behaves identically to urllib2.urlopen, except that it
   deals with cookies automatically. That's probably all you need to
   know.

   Python 2.0 or above is required, and urllib2 is recommended. If you
   have 2.1 or above, you've already got a recent enough version of
   urllib2. For Python 2.0, you need the newer versions from Python 2.1
   (available from the source distribution or Python CVS: [6]urllib2.py).
   Note that you don't need to replace the original urllib2 / urllib -
   you can just make sure they're in sys.path ahead of the copies from
   2.0's standard library.

   For full documentation, see [7]here and the docstrings in the module
   source code.

   Other than Gisle, particular thanks to Johnny Lee (MSIE Perl code) and
   Ronald Tschalar (advice on Netscape cookies).

Notes about ClientCookie, urllib2 and cookielib

   Even if you're not using Python 2.4, please note the last of these
   points.
    1. The cookie handling parts of ClientCookie are in Python 2.4
       standard library as module cookielib and extensions to module
       urllib2.
    2. ClientCookie works with Python 2.4.
    3. For new code to run on Python 2.4, I recommend use of standard
       library modules urllib2 and cookielib instead of ClientCookie. I
       recommend [8]turning on RFC 2965 support to work around a bug in
       cookielib in Python 2.4.0.
    4. Handler classes thst are missing from 2.4's urllib2 (eg.
       HTTPRefreshProcessor) may be used with 2.4's urllib2 (however,
       note the paragraph below). With any version of Python, parts of
       urllib2 that are missing from ClientCookie (eg. ProxyHandler) may
       be used with ClientCookie, and urllib2.Request objects may be used
       with ClientCookie. IMPORTANT: For all other code, use ClientCookie
       exclusively: do NOT mix use of ClientCookie and urllib2!

   Finally, note that, if you want to use ClientCookie.RefreshProcessor
   with Python 2.4's urllib2, you must also use
   ClientCookie.HTTPRedirectHandler.

Download

   All documentation (including these web pages) is included in the
   distribution.

   To port your code from 0.4.x to 1.0.x, see [9]here.

   Stable release.
     * [10]ClientCookie-1.3.0.tar.gz
     * [11]ClientCookie-1.3.0.zip
     * [12]Change Log (included in distribution)
     * [13]Older versions.

   Old release.
     * [14]ClientCookie-0.4.19.tar.gz
     * [15]ClientCookie-0_4_19.zip
     * [16]Change Log (included in distribution)
     * [17]Older versions.

   For installation instructions, see the INSTALL file included in the
   distribution.

Subversion

   The [18]Subversion (SVN) trunk is
   [19]http://codespeak.net/svn/wwwsearch/ClientCookie/trunk, so to check
   out the source:
svn co http://codespeak.net/svn/wwwsearch/ClientCookie/trunk ClientCookie

FAQs - pre-install

     * Doesn't the standard Python library module, Cookie, do this?
       No: Cookie.py does the server end of the job. It doesn't know when
       to accept cookies from a server or when to pass them back.
     * Which version of Python do I need?
       2.0 or above.
     * Is urllib2.py required?
       No. You probably want it, though.
     * Which urllib2.py do I need?
       You don't, but if you want to use the extended urllib2 callables
       from ClientCookie, and you have Python 2.0, you need to upgrade to
       the version from Python 2.1. Otherwise, you're OK.
     * Which license?
       ClientCookie is dual-licensed: you may pick either the [20]BSD
       license, or the [21]ZPL 2.1 (both are included in the
       distribution).
     * Where can I find out more about the HTTP cookie protocol?
       There is more than one protocol, in fact (see the [22]docs for a
       brief explanation of the history):
          + The original [23]Netscape cookie protocol - the standard
            still in use today, in theory (in reality, the protocol
            implemented by all the major browsers only bears a passing
            resemblance to the protocol sketched out in this document).
          + [24]RFC 2109 - obsoleted by RFC 2965.
          + [25]RFC 2965 - the Netscape protocol with the bugs fixed (not
            widely used - the Netscape protocol still dominates, and
            seems likely to remain dominant indefinitely, at least on the
            Internet). [26]RFC 2964 discusses use of the protocol.
            [27]Errata to RFC 2965 are currently being discussed on the
            [28]http-state mailing list (update: list traffic died months
            ago and hasn't revived).
          + A [29]paper by David Kristol setting out the history of the
            cookie standards in exhausting detail.
          + HTTP cookies [30]FAQ.
     * Which protocols does ClientCookie support?
       Netscape and RFC 2965. RFC 2965 handling is switched off by
       default.
     * What about RFC 2109?
       RFC 2109 cookies are currently parsed as Netscape cookies, and
       treated by default as RFC 2965 cookies thereafter if RFC 2965
       handling is enabled, or as Netscape cookies otherwise. RFC 2109 is
       officially obsoleted by RFC 2965. Browsers do use a few RFC 2109
       features in their Netscape cookie implementations (port and
       max-age), and ClientCookie knows about that, too.

   I prefer questions and comments to be sent to the [31]mailing list
   rather than direct to me.

   [32]John J. Lee, April 2006.
     _________________________________________________________________

   [33]Home
   [34]General FAQs
   [35]mechanize
   [36]pullparser
   ClientCookie
   [37]ClientCookie docs
   [38]ClientForm
   [39]DOMForm
   [40]python-spidermonkey
   [41]ClientTable
   [42]1.5.2 urllib2.py
   [43]1.5.2 urllib.py
   [44]Download
   [45]FAQs - pre-install

References

   1. http://sourceforge.net/
   2. http://wwwsearch.sourceforge.net/ClientCookie/#compatnotes
   3. http://www.python.org/
   4. http://www.ietf.org/rfc/rfc2616.txt
   5. http://www.linpro.no/lwp/
   6. http://cvs.sourceforge.net/viewcvs.py/*checkout*/python/python/dist/src/Lib/urllib2.py?rev=1.13.2.2
   7. http://wwwsearch.sourceforge.net/ClientCookie/doc.html
   8. http://docs.python.org/lib/cookielib-examples.html
   9. http://wwwsearch.sourceforge.net/ClientCookie/porting-0.4-1.0.txt
  10. http://wwwsearch.sourceforge.net/ClientCookie/src/ClientCookie-1.3.0.tar.gz
  11. http://wwwsearch.sourceforge.net/ClientCookie/src/ClientCookie-1.3.0.zip
  12. http://wwwsearch.sourceforge.net/ClientCookie/src/ChangeLog.txt
  13. http://wwwsearch.sourceforge.net/ClientCookie/src/
  14. http://wwwsearch.sourceforge.net/ClientCookie/src/ClientCookie-0.4.19.tar.gz
  15. http://wwwsearch.sourceforge.net/ClientCookie/src/ClientCookie-0_4_19.zip
  16. http://wwwsearch.sourceforge.net/ClientCookie/src/ChangeLog.txt
  17. http://wwwsearch.sourceforge.net/ClientCookie/src/
  18. http://subversion.tigris.org/
  19. http://codespeak.net/svn/wwwsearch/ClientCookie/trunk#egg=ClientCookie-dev
  20. http://www.opensource.org/licenses/bsd-license.php
  21. http://www.zope.org/Resources/ZPL
  22. http://wwwsearch.sourceforge.net/ClientCookie/doc.html
  23. http://www.netscape.com/newsref/std/cookie_spec.html
  24. http://www.ietf.org/rfcs/rfc2109.txt
  25. http://www.ietf.org/rfcs/rfc2965.txt
  26. http://www.ietf.org/rfcs/rfc2964.txt
  27. http://kristol.org/cookie/errata.html
  28. http://lists.bell-labs.com/mailman/listinfo/http-state
  29. http://doi.acm.org/10.1145/502152.502153
  30. http://www.cookiecentral.com/
  31. http://lists.sourceforge.net/lists/listinfo/wwwsearch-general
  32. mailto:jjl@pobox.com
  33. http://wwwsearch.sourceforge.net/
  34. http://wwwsearch.sourceforge.net/bits/GeneralFAQ.html
  35. http://wwwsearch.sourceforge.net/mechanize/
  36. http://wwwsearch.sourceforge.net/pullparser/
  37. http://wwwsearch.sourceforge.net/ClientCookie/doc.html
  38. http://wwwsearch.sourceforge.net/ClientForm/
  39. http://wwwsearch.sourceforge.net/DOMForm/
  40. http://wwwsearch.sourceforge.net/python-spidermonkey/
  41. http://wwwsearch.sourceforge.net/ClientTable/
  42. http://wwwsearch.sourceforge.net/bits/urllib2_152.py
  43. http://wwwsearch.sourceforge.net/bits/urllib_152.py
  44. http://wwwsearch.sourceforge.net/ClientCookie/#download
  45. http://wwwsearch.sourceforge.net/ClientCookie/#faq_pre
