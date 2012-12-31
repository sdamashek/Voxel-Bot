import ClientCookie as CC
import time
import urllib2 as url
import urllib
from xml.dom import minidom
def classifyEdit(summary):
	summary = summary.lower()
	vandalism = ["revert", "rv "]
	notVandalism = ["good faith", "agf", "unsourced", "unreferenced", "self", "speculat", "original research", "rv tag", "typo", "incorrect"]
	for i in notVandalism:
		if i in summary:
			return False
	for i in vandalism:
		if i in summary:
			if summary.count("*/")==0:
				return True
			elif i not in summary.split("*/")[1]:
				return False
			return True
	return False
def getSummaryList():
	currentTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", (time.gmtime(time.time()-300))) #Format time according to MediaWiki API Specifications
	x = "http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rcstart="+currentTime+"&rcend="+time.strftime("&Y-&m-&dT%H:%M:%SZ", time.gmtime())+"&rclimit=1000&rcdir=newer&rcprop=comment|ids&format=xml" #Define RecentChanges Query
	data = CC.urlopen(x).read() #Make the request
	data = data.lower() #Make everything lowercase for ease of parsing
	dom = minidom.parseString(data)
	changes = dom.getElementsByTagName("rc")
	return [(i.attributes['comment'].value+" Rev Link: http://en.wikipedia.org/w/index.php?diff="+i.attributes['revid'].value) for i in changes]
def getCounts():
	sums = getSummaryList()
	revert = int(round((len(([i for i in sums if classifyEdit(i)]))+1)/5.0))
	total = int(round((len(sums)+1)/5.0))
	return (total, revert)
def getSummaries(thatAreVandalism):
	e = []
	summaries = getSummaryList()
	for i in summaries:
		if classifyEdit(i) == thatAreVandalism:
			e.append(i+"\n\n")
	return e
