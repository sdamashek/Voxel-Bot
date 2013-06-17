import ClientCookie as CC
import time
import urllib2 as url
import urllib
from xml.dom import minidom


def classifyEdit(summary):
    summary = summary.lower()
    vandalism = ["revert", "rv ", "long-term abuse", "long term abuse", "lta", "abuse"]  # long term abuse (in blocks) added per legoktm
    notVandalism = ["uaa", "good faith", "agf", "unsourced", "unreferenced", "self", "speculat", "original research", "rv tag", "typo", "incorrect", "format"]
    for i in notVandalism:
        if i in summary:
            return False
    for i in vandalism:
        if i in summary:
            if summary.count("*/") == 0:
                return True
            elif i not in summary.split("*/")[1]:
                return False
            return True
    return False


def recentChangesGet(timeFrom, currentData=None):  # Because everybody likes recursiveness
    print timeFrom
    link = "http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rcstart=" + timeFrom + "&rcend=" + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + "&rclimit=5000&rcdir=newer&rcprop=comment|ids&format=xml"
    print link
    data = CC.urlopen(link).read()  # Make the request
    dom = minidom.parseString(data)
    recentChanges = dom.getElementsByTagName("recentchanges")
    data = data.lower()  # Make everything lowercase for ease of parsing
    dom = minidom.parseString(data)
    changes = dom.getElementsByTagName("rc")
    try:
        rcg = recentChangesGet(recentChanges[1].attributes['rcstart'].value)
        # print rcg
        changes = [(i.attributes['comment'].value + " Diff: http://en.wikipedia.org/w/index.php?diff=" + i.attributes['revid'].value) for i in changes]
        print "recursing"
        return rcg + changes
    except IndexError:
        print "ending recursion"
        return [(i.attributes['comment'].value + " Diff: http://en.wikipedia.org/w/index.php?diff=" + i.attributes['revid'].value) for i in changes]


def getSummaryList():
    currentTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", (time.gmtime(time.time() - 1800)))  # Format time according to MediaWiki API Specifications
    rc = recentChangesGet(currentTime)
    # print rc
    return rc


def getCounts():
    sums = getSummaryList()
    rv = len(([i for i in sums if classifyEdit(i)]))
    revert = 0 if rv is 0 else int(round((rv + 1) / 30.0))
    total = int(round((len(sums) + 1) / 30.0))
    return (total, revert)


def getSummaries(thatAreVandalism):
    e = []
    summaries = getSummaryList()
    for i in summaries:
        if classifyEdit(i) == thatAreVandalism:
            e.append(i + "\n\n")
    return e
