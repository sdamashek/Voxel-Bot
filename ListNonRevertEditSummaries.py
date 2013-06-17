from xml.dom import minidom
import urllib


def isRevert(text):
    text = text.lower()
        if "revert" in text and "good faith" not in text:
            return True
        return False
import time
currentTime = time.strftime(
    "%Y-%m-%dT%H:%M:%SZ", (time.gmtime(time.time() - 300)))
                            # Format time according to MediaWiki API
                            # Specifications
x = "http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rcstart=" + \
    currentTime + \
    "&rclimit=500&rcdir=older&rcprop=comment&format=xml"  # Define RecentChanges Query
x = urllib.urlopen(x).read()
dom = minidom.parseString(x)
changes = dom.getElementsByTagName("rc")
for i in changes:
    attr = i.attributes['comment'].value
    if not isRevert(attr) and attr is not "" and attr is not " ":
        print attr
        print "------------"
