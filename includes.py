import ClientCookie as CC
import time
import urllib2 as url
import urllib
from xml.dom import minidom
def classifyEdit(summary):
	summary = summary.lower()
	vandalism = ["revert", "rv "]
	notVandalism = ["good faith", "agf", "unsourced", "unreferenced", "self", "speculat", "original research", "rv tag", "typo", "incorrect", "format"]
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
def recentChangesGet(timeFrom): #Because everybody likes recursiveness
	print timeFrom
	data = CC.urlopen("http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rcstart="+timeFrom+"&rcend="+time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())+"&rclimit=500&rcdir=newer&rcprop=comment|ids&format=xml").read() #Make the request
	data = data.lower() #Make everything lowercase for ease of parsing
	dom = minidom.parseString(data)
	recentChanges = dom.getElementsByTagName("recentchanges")
	changes = dom.getElementsByTagName("rc")
	try:
		return [(recentChangesGet(recentChanges[0].attributes['rcstart'].value))+((i.attributes['comment'].value+" Rev Link: http://en.wikipedia.org/w/index.php?diff="+i.attributes['revid'].value) for i in changes)]
	except KeyError:
		return [(i.attributes['comment'].value+" Rev Link: http://en.wikipedia.org/w/index.php?diff="+i.attributes['revid'].value) for i in changes]
def getSummaryList():
	currentTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", (time.gmtime(time.time()-1800))) #Format time according to MediaWiki API Specifications
	rc=recentChangesGet(currentTime)
	print rc
	return rc
def getCounts():
	sums = getSummaryList()
	rv = len(([i for i in sums if classifyEdit(i)]))
	revert = 0 if rv is 0 else int(round((rv+1)/30.0))
	total = int(round((len(sums)+1)/30.0))
	return (total, revert)
def getSummaries(thatAreVandalism):
	e = []
	summaries = getSummaryList()
	for i in summaries:
		if classifyEdit(i) == thatAreVandalism:
			e.append(i+"\n\n")
	return e
