from ClientCookie import *
import time
import urllib2 as url
import urllib
from xml.dom import minidom
def classifyEdit(summary):
	summary = summary.lower()
	vandalism = ["revert", "rv "]
	notVandalism = ["good faith", "agf", "unsourced", "unreferenced"]
	for i in notVandalism:
		if i in summary:
			return False
	for i in vandalism:
		if i in summary:
			return True
	return False
def getSummaryList():
	currentTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", (time.gmtime(time.time()-300))) #Format time according to MediaWiki API Specifications
	x = "http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rcstart="+currentTime+"&rcend="+time.strftime("&Y-&m-&dT%H:%M:%SZ", time.gmtime())+"&rclimit=500&rcdir=newer&rcprop=comment&format=xml" #Define RecentChanges Query
	data = url.urlopen(x).read() #Make the request
	data = data.lower() #Make everything lowercase for ease of parsing
	dom = minidom.parseString(data)
	changes = dom.getElementsByTagName("rc")
	return [i.attributes['comment'].value for i in changes]
def getCounts():
	sums = getSummaryList()
	revert = int(round((len(([i for i in sums if classifyEdit(i)]))+1)/5.0))
	total = int(round((len(sums)+1)/5.0))
	return (total, revert)
def getSummaries(thatAreVandalism):
	summaries = getSummaryList()
	for i in summaries:
		if classifyEdit(i) == thatAreVandalism:
			print i
			print "----------------"
