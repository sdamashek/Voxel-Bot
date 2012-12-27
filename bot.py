import time
import urllib2 as url
import urllib
import ClientCookie
import re
from logininfo import *
def getCountThingy():
    currentTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", (time.gmtime(time.time()-300))) #EXAMPLE: from=20121226170007 time.time()-300
    x = "http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rcstart="+currentTime+"&rclimit=5000&rcdir=older&rcprop=comment&format=xml"
    data = url.urlopen(x).read()
    data = data.lower()
    count = int(round(((data.count("revert")-data.count("reverted good faith")-data.count("reverting good faith"))/5.0)+1)) #Round up
    totalEdits = int(round(data.count('<rc type')/5.0))
    return (totalEdits, count)
theTuple = getCountThingy()
print "Edit Per Minute: ", theTuple[0]
print "RV Per Minute: ", theTuple[1]
a = open("bot.txt")
b = a.read()
if str(theTuple[0]) + " " + str(theTuple[1]) not in b:
	a.close()
	a = open("bot.txt", "w")
	a.write(str(theTuple[0]) + " " + str(theTuple[1]))
	a.close()
	print "Template:"
	edit = """{{{{#if:{{{style|}}}|wdefcon/styles/{{{style}}}|{{{prefix|User:Zsinj/}}}Wdefcon}}
|level  = {{WikiDefcon/levels|"""+str(theTuple[1])+"""}}
|sign   = ~~~~
|info   = """ + str(theTuple[0]) + "/" + str(theTuple[1])+ """ according to VoxelBot.
|align  = {{{align|}}} 
|noinfo = {{{noinfo|}}}
|type   = {{{type|}}}
}}<noinclude>
{{documentation}}
</noinclude>"""
	print edit
	usernameKey = 'lgname'
	passwordKey = 'lgpassword'
	loginUrl = "http://en.wikipedia.org/w/api.php?format=xml&action=login"
	loginInformation = {usernameKey: uname, passwordKey: password} # Creates a request dictionary
	loginInformatione = urllib.urlencode(loginInformation) # Encode the login information.
	loginRequest = url.Request(loginUrl, loginInformatione) # Creates a Request that is used to login
	loginResponse = ClientCookie.urlopen(loginRequest) # Sends the login to Wikipedia and stores the PHP session ID.
	loginResponse = loginResponse.read() # Get the HTML/XML from Wikipedia.
	loginToken = loginResponse.split('token="')[1].split('" cookie')[0]
	loginInformation["lgtoken"] = loginToken
	loginInformatione = urllib.urlencode(loginInformation)
	loginRequest = url.Request(loginUrl, loginInformatione) 
	loginResponse = ClientCookie.urlopen(loginRequest)
	loginResponse = loginResponse.read()
	print loginResponse
	x = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=tokens&format=xml").read().split('edittoken="')[1].split('" />')[0]
	print x
	editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Updating Vandalism Information Template (Unapproved bot editing [[Wikipedia:Bot_policy#Requests_for_approval|in own userspace)]]", "text": edit, "title": "User:VoxelBot/Vandalism information"}))
	response = ClientCookie.urlopen(editInfo).read()
	print response
else:
	print "No edit needed!"
