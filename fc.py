#Featured article candidates and featured list candidates archiver and promoter
#By Vacation9 (Samuel Damashek)
import datetime
import urllib2 as url
import urllib
import ClientCookie
import re
import sys
import socket
import string
import os
import io
from xml.sax import saxutils as su
from logininfo import * #import various libraries and the login info
from includes import *
usernameKey = 'lgname'
passwordKey = 'lgpassword' #Define POST variable names
loginUrl = "http://en.wikipedia.org/w/api.php?format=xml&action=login" #Define request URL
loginInformation = {usernameKey: uname, passwordKey: password} # Creates a request dictionary
loginInformatione = urllib.urlencode(loginInformation) # Encode the login information.
loginRequest = url.Request(loginUrl, loginInformatione) # Creates a Request that is used to login
loginResponse = ClientCookie.urlopen(loginRequest) # Sends the login to Wikipedia and stores the PHP session ID.
loginResponse = loginResponse.read() # Get the HTML/XML from Wikipedia.
loginToken = loginResponse.split('token="')[1].split('" cookie')[0] #Get 1st login token
loginInformation["lgtoken"] = loginToken #Add token to dictionary
loginInformatione = urllib.urlencode(loginInformation) #Re-encode with new login token
loginRequest = url.Request(loginUrl, loginInformatione) #Login again (required by API), passing the login token this time
loginResponse = ClientCookie.urlopen(loginRequest) #Get the cookie from the login request
loginResponse = loginResponse.read() #Set the response to the .read of the response (parsable)
print loginResponse #Print login response for debugging
x = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=tokens&format=xml").read().split('edittoken="')[1].split('" />')[0] #Get edit token - required to edit the template
print x #Print the token for debugging
#~~~GLOBAL FUNCTIONS~~~#
montharray=["January","February","March","April","May","June","July","August","September","October","November","December"]
month = montharray[datetime.date.today().month-1]
year = datetime.date.today().year
print year
def getContent(page):
	url = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvlimit=1&format=xml&titles="+page.replace(" ","_")
	print url
	pagecontent = ClientCookie.urlopen(url).read()
	flcre = re.compile(r'(?<=preserve">).*?(?=</rev>)',re.DOTALL)
        flccontent = re.findall(flcre,pagecontent)[0]
	return flccontent
def rmGA(page):
	facats = ["Agriculture, food and drink","Art and architecture","Engineering and technology","Geography and places","History","Language and literature","Mathematics","Music","Natural sciences","Philosophy and religion","Social sciences and society","Sports and recreation","Theatre, film and drama","Video games","Warfare"]
	for facat in facats:
		catcontent = getContent("Wikipedia:Good articles/"+facat)
		newcontent = catcontent.replace(page+"\n","")
		if newcontent != catcontent:
			editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Removing FA promoted page from Good articles category", "text":newcontent.unescape(updatedTalk).replace("&quot;","\""), "bot": "true", "title": "Wikipedia:Good articles/"+facat})) #Define the edit query and execute it
			response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
			print response


#~~~FLC~~~#
flcapproved = ["The Rambling Man","Dabomb87","Giants2008","NapHit","Hahc21"] #Users who are allowed to approve/disapprove FLC candidates
#~~~FLC PROMOTIONS~~~#
#~~~FLC FUNCTIONS~~~#
def flcProcess(link,user,diff,oldlink,result):
	flccontent = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles="+link.replace(" ","_")).read()
	if r"&lt;!--FLtop--&gt;" not in flccontent:
	#if True:
		print link
		print user
		print diff
		print oldlink
		flcre = re.compile(r"""(?<=preserve">).*?(?=</rev>)""",re.DOTALL)
		flccontent = re.findall(flcre,flccontent)[0]
		flccontent = "{{subst:User:Hahc21/FLTop|result="+result+"|closer="+user+"|time=~~~~~|link=diff="+diff+"&oldid="+oldlink+"}}\n" + flccontent
		flccontent = flccontent + "{{subst:User:Hahc21/FLBottom}}"
		editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Archiving FLC Nomination", "text":su.unescape(flccontent).replace("&quot;","\""), "bot": "true", "title": link.replace("&","%26")})) #Define the edit query and execute it
		response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
		print response
		flcpage = re.findall(r"(?<=Featured list candidates/).*?(?=/archive)",link.replace("_"," "))[0]
                print flcpage
		if result=="promoted":
			pagecontent = getContent(flcpage)
			pagecontent = "{{featured list}}\n" + pagecontent
			if "#REDIRECT" in pagecontent:
                	       	print "redirecting"
                       		flcpage = re.findall(r"(?<=#REDIRECT \[\[).*?(?=\]\])",pagecontent)[0] 
			editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Adding Featured List Star", "text":su.unescape(pagecontent).replace("&quot;","\""), "title": flcpage})) #Define the edit query and execute it
                	response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
       	       		print response
		talkUrl = "Talk:"+flcpage
		talkPage = getContent(talkUrl)
		if result=="promoted":
			talkPage = talkPage.replace("|class=list","|class=FL")
		talkPage = re.sub(r"{{featured list candidates.+?}}","",talkPage)
		if len(re.findall(r"{{[Aa]rticle ?[Hh]istory",talkPage))>0:
			print talkPage
			latestgan = re.compile("action[0-9]+ *?=.+?date *?=.+?[0-9][0-9][0-9][0-9]",re.DOTALL).findall(talkPage)[-1]
			print latestgan
			latestgannumber = str(int(re.findall(r"(?<=action)[0-9]+?(?=date)",latestgan)[0])+1)
			articleHistoryStart = re.findall(re.compile(r"{{[Aa]rticle ?[Hh]istory.*?(?=\| ?currentstatus)",re.DOTALL),talkPage)[0]
			actionTime = time.strftime("%H:%M, %d %B %Y", (time.gmtime(time.time())))
			updatedTalk = talkPage.replace(articleHistoryStart,articleHistoryStart+"\n|action"+latestgannumber+"=FLC"+"\n|action"+latestgannumber+"date="+actionTime+"\n|action"+latestgannumber+"link="+link+"\n|action"+latestgannumber+"result="+result+"\n|action"+latestgannumber+"oldid=\n")
			newstatus=""
			if result == "promoted":
				newstatus = r"currentstatus=FL" 
			else:
				newstatus = r"currentstatus=FFLC"
			updatedTalk = re.sub(r"currentstatus ?= ?.*?(?=(\||}|\n| ))",newstatus,updatedTalk)
			editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Updating Article history", "text":su.unescape(updatedTalk).replace("&quot;","\""), "bot": "true", "title": talkUrl.replace("&","%26")})) #Define the edit query and execute it
                	response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
                	print response
		else:
			newstatus=""
                        if result == "promoted":
                                newstatus = r"currentstatus=FL"
                        else:
                                newstatus = r"currentstatus=FFLC"
			actionTime = time.strftime("%H:%M, %d %B %Y", (time.gmtime(time.time())))
			updatedTalk = "{{Article history\n|action1=FLC"+"\n|action1date="+actionTime+"\n|action1link="+link+"\n|action1result="+result+"\n|action1oldid="+"\n|"+newstatus+"}}" + talkPage
			editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Adding Article history", "text":su.unescape(updatedTalk).replace("&quot;","\""), "bot": "true", "title": talkUrl.replace("&","%26")})) #Define the edit query and execute it
			response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
			print response 


#~~~FLC MAIN FUNCTION~~~#
#~~~ACCEPTED FLC~~~#
flcpromoted = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content|user|ids&rvlimit=5000&format=xml&titles=Wikipedia:Featured_list_candidates/Featured_log/"+month+"_"+str(year)).read()
print flcpromoted
dom = minidom.parseString(flcpromoted)
flccontent = ""
approvededit = False
revisionnumber = 0
while approvededit == False:
	print revisionnumber
	flccontent = dom.getElementsByTagName("rev")[revisionnumber]
	if flccontent.attributes['user'].value in flcapproved:
		flccontentnew = flccontent.childNodes[0].data.encode("utf8")
		approvinguser = flccontent.attributes['user'].value.encode("utf8")
		revid = flccontent.attributes['revid'].value.encode("utf8")
		oldid = flccontent.attributes['parentid'].value.encode("utf8")
		approvededit = True
	revisionnumber = revisionnumber + 1
print flccontentnew
for acceptedflc in re.findall(r"(?<=\{\{)Wikipedia:.*?(?=\}\})",flccontentnew):
	print acceptedflc
	flcProcess(acceptedflc,approvinguser,revid,oldid,"promoted")
#~~~DECLINED FLC~~~#
flcnotpromoted = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content|user|ids&rvlimit=5000&format=xml&titles=Wikipedia:Featured_list_candidates/Failed_log/"+month+"_"+str(year)).read()
print flcnotpromoted
dom = minidom.parseString(flcnotpromoted)
flccontent = ""
approvededit = False
revisionnumber = 0
while approvededit == False:
        print revisionnumber
        flccontent = dom.getElementsByTagName("rev")[revisionnumber]
        if flccontent.attributes['user'].value in flcapproved:
                flccontentnew = flccontent.childNodes[0].data.encode("utf8")
                approvinguser = flccontent.attributes['user'].value.encode("utf8")
                revid = flccontent.attributes['revid'].value.encode("utf8")
                oldid = flccontent.attributes['parentid'].value.encode("utf8")
                approvededit = True
        revisionnumber = revisionnumber + 1
print flccontentnew
for declinedflc in re.findall(r"(?<=\{\{)Wikipedia:.*?(?=\}\})",flccontentnew):
        print declinedflc
        flcProcess(declinedflc,approvinguser,revid,oldid,"not promoted")
#~~~FAC~~~#
facapproved = ["Uchucha", "GrahamColm", "Ian Rose", "Raul654"] #Users who are allowed to approve/disapprove FLC candidates
#~~~FAC PROMOTIONS~~~#
#~~~FAC FUNCTIONS~~~#
def facProcess(link,user,diff,oldlink,result):
	faccontent = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles="+link.replace(" ","_")).read()
	if "&lt;!--FAtop--&gt;" not in faccontent and "&lt;!--FLtop--&gt;" not in faccontent:
	#if True:
		print link
		print user
		print diff
		print oldlink
		facre = re.compile(r"""(?<=preserve">).*?(?=</rev>)""",re.DOTALL)
		faccontent = re.sub(r"&gt;noinclude&lt;{{la.+?}}&gt;/noinclude&lt;","", re.findall(facre,faccontent)[0])
		faccontent = "{{subst:User:Hahc21/FLTop|result="+result+"|closer="+user+"|time=~~~~~|type=FA|link=diff="+diff+"&oldid="+oldlink+"}}\n" + faccontent
		faccontent = faccontent + "{{subst:User:Hahc21/FLBottom}}"
		editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Archiving FAC Nomination", "text":su.unescape(faccontent).replace("&quot;","\""), "bot": "true", "title": link.replace("&","%26")})) #Define the edit query and execute it
		response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
		print response
		facpage = re.findall(r"(?<=Featured article candidates/).*?(?=/archive)",link.replace("_"," "))[0]
                print facpage
		if result == "promoted":
			pagecontent = getContent(facpage).replace("{{good article}}","").replace("{{goodarticle}}","").replace("{{Good article}}","").replace("{{Goodarticle}}","")
			pagecontent = "{{featured article}}\n" + pagecontent
			if "#REDIRECT" in pagecontent:
                        	print "redirecting"
                        	facpage = re.findall(r"(?<=#REDIRECT \[\[).*?(?=\]\])",pagecontent)[0] 
			editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Adding Featured Article Star", "text":su.unescape(pagecontent).replace("&quot;","\""), "title": facpage})) #Define the edit query and execute it
	                response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
        	        print response
			rmGA(facpage)
		talkUrl = "Talk:"+facpage
		talkPage = getContent(talkUrl)
		if result=="promoted":
			talkPage = re.sub(r"\|class=.*?(?=(\||\n|}))","|class=FA",talkPage)
		talkPage = re.sub(r"{{featured article candidates.+?}}","",talkPage)
		if len(re.findall(r"{{[Aa]rticle ?[Hh]istory",talkPage))>0:
			print talkPage
			latestgan = re.compile("action[0-9]+ *?=.+?date *?=.+?[0-9][0-9][0-9][0-9]",re.DOTALL).findall(talkPage)[-1]
			print latestgan
			latestgannumber = str(int(re.findall(r"(?<=action)[0-9]+?(?=date)",latestgan)[0])+1)
			articleHistoryStart = re.findall(re.compile(r"{{[Aa]rticle ?[Hh]istory.*?(?=\| ?currentstatus)",re.DOTALL),talkPage)[0]
			actionTime = time.strftime("%H:%M, %d %B %Y", (time.gmtime(time.time())))
			updatedTalk = talkPage.replace(articleHistoryStart,articleHistoryStart+"\n|action"+latestgannumber+"=FAC"+"\n|action"+latestgannumber+"date="+actionTime+"\n|action"+latestgannumber+"link="+link+"\n|action"+latestgannumber+"result="+result+"\n|action"+latestgannumber+"oldid=\n")
			newstatus=""
			if len(re.findall("currentstatus ?= ?GA",talkPage))>=1:
				newstatus = r"currentstatus=GA"
			elif result == "promoted":
				newstatus = r"currentstatus=FA" 
			else:
				newstatus = r"currentstatus=FFAC"
			updatedTalk = re.sub(r"currentstatus ?= ?.*?(?=(\||}|\n| ))",newstatus,updatedTalk)
			editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Updating Article history", "text":su.unescape(updatedTalk).replace("&quot;","\""), "bot": "true", "title": talkUrl.replace("&","%26")})) #Define the edit query and execute it
                	response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
                	print response
		else:
			newstatus=""
                        if result == "promoted":
                                newstatus = r"currentstatus=FA"
                        else:
                                newstatus = r"currentstatus=FFAC"
			actionTime = time.strftime("%H:%M, %d %B %Y", (time.gmtime(time.time())))
			updatedTalk = "{{Article history\n|action1=FAC"+"\n|action1date="+actionTime+"\n|action1link="+link+"\n|action1result="+result+"\n|action1oldid="+"\n|currentstatus="+newstatus+"}}" + talkPage
			editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Adding Article history", "text":su.unescape(updatedTalk).replace("&quot;","\""), "bot": "true", "title": talkUrl.replace("&","%26")})) #Define the edit query and execute it
                        response = ClientCookie.urlopen(editInfo).read() #Get the response for debugging
                        print response 

#~~~FAC MAIN FUNCTION~~~#
#~~~ACCEPTED FAC~~~#
facpromoted = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content|user|ids&rvlimit=5000&format=xml&titles=Wikipedia:Featured_article_candidates/Featured_log/"+month+"_"+str(year)).read()
print facpromoted
dom = minidom.parseString(facpromoted)
faccontent = ""
approvededit = False
revisionnumber = 0
while approvededit == False:
	print revisionnumber
	faccontent = dom.getElementsByTagName("rev")[revisionnumber]
	if faccontent.attributes['user'].value in facapproved:
		faccontentnew = faccontent.childNodes[0].data.encode("utf8")
		approvinguser = faccontent.attributes['user'].value.encode("utf8")
		revid = faccontent.attributes['revid'].value.encode("utf8")
		oldid = faccontent.attributes['parentid'].value.encode("utf8")
		approvededit = True
	revisionnumber = revisionnumber + 1
print faccontentnew
for acceptedfac in re.findall(r"(?<=\{\{)Wikipedia:.*?(?=\}\})",faccontentnew):
	print acceptedfac
	facProcess(acceptedfac,approvinguser,revid,oldid,"promoted")
#~~~DECLINED FAC~~~#
facnotpromoted = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content|user|ids&rvlimit=5000&format=xml&titles=Wikipedia:Featured_article_candidates/Archived_nominations/"+month+"_"+str(year)).read()
print facnotpromoted
dom = minidom.parseString(facnotpromoted)
faccontent = ""
approvededit = False
revisionnumber = 0
while approvededit == False:
        print revisionnumber
        faccontent = dom.getElementsByTagName("rev")[revisionnumber]
        if faccontent.attributes['user'].value in facapproved:
                faccontentnew = faccontent.childNodes[0].data.encode("utf8")
                approvinguser = faccontent.attributes['user'].value.encode("utf8")
                revid = faccontent.attributes['revid'].value.encode("utf8")
                oldid = faccontent.attributes['parentid'].value.encode("utf8")
                approvededit = True
        revisionnumber = revisionnumber + 1
print faccontentnew
for declinedfac in re.findall(r"(?<=\{\{)Wikipedia:.*?(?=\}\})",faccontentnew):
        print declinedfac
        facProcess(declinedfac,approvinguser,revid,oldid,"not promoted")

