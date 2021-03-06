import time
import urllib2 as url
import urllib
import ClientCookie
import re
import sys
import socket
import string
import os
from logininfo import *  # import various libraries and the login info
from includes import *
# def getCountThingy():
# currentTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", (time.gmtime(time.time()-300))) #Format time according to MediaWiki API Specifications
# x = "http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rcstart="+currentTime+"&rcend="+time.strftime("&Y-&m-&dT%H:%M:%SZ", time.gmtime())+"&rclimit=500&rcdir=newer&rcprop=comment|ids&format=xml" #Define RecentChanges Query
# data = url.urlopen(x).read() #Make the request
# data = data.lower() #Make everything lowercase for ease of parsing
# count = int(round(((data.count("revert")+data.count("rvv")+data.count("rv vand")+data.count("rv ")-data.count("rv good faith")-data.count("reverted good faith")-data.count("reverting good faith")-data.count("help:reverting"))/5.0)+1)) #Find the amount of hits of the word "revert" then subtract good faith and duplicate occurances, divide by 5 to average, and add 1 so it rounds up.
# totalEdits = int(round(data.count('<rc type')/5.0)) #Calculate total edits in same manner (temp fix)
# return (totalEdits, count) #Return a tuple of the results
usernameKey = 'lgname'
passwordKey = 'lgpassword'  # Define POST variable names
loginUrl = "http://en.wikipedia.org/w/api.php?format=xml&action=login"  # Define request URL
loginInformation = {usernameKey: uname, passwordKey: password}  # Creates a request dictionary
loginInformatione = urllib.urlencode(loginInformation)  # Encode the login information.
loginRequest = url.Request(loginUrl, loginInformatione)  # Creates a Request that is used to login
loginResponse = ClientCookie.urlopen(loginRequest)  # Sends the login to Wikipedia and stores the PHP session ID.
loginResponse = loginResponse.read()  # Get the HTML/XML from Wikipedia.
loginToken = loginResponse.split('token="')[1].split('" cookie')[0]  # Get 1st login token
loginInformation["lgtoken"] = loginToken  # Add token to dictionary
loginInformatione = urllib.urlencode(loginInformation)  # Re-encode with new login token
loginRequest = url.Request(loginUrl, loginInformatione)  # Login again (required by API), passing the login token this time
loginResponse = ClientCookie.urlopen(loginRequest)  # Get the cookie from the login request
loginResponse = loginResponse.read()  # Set the response to the .read of the response (parsable)
print loginResponse  # Print login response for debugging
x = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=tokens&format=xml").read().split('edittoken="')[1].split('" />')[0]  # Get edit token - required to edit the template
print x  # Print the token for debugging
theTuple = getCounts()  # Define tuple as array
open("/data/project/public_html/vacation9/VoxelBot/report.txt", "a").writelines([i.encode("utf-8") for i in getSummaries(True)])
print "Edit Per Minute: ", theTuple[0]  # Output Edits per Minute to Output Screen for Debugging
print "RV Per Minute: ", theTuple[1]  # Same, but for reverts
a = open("/home/vacation9/VoxelBot/bot.txt")  # open connection to the previous value file, bot.txt
b = a.read()  # set value of a to b
templatecontent = "http://en.wikipedia.org/w/api.php?action=query&titles=Template:Vandalism_information&format=xml&prop=revisions&rvprop=content"  # Get Template contents to do manual override check
templatecontent = ClientCookie.urlopen(templatecontent).read()  # Make the request
print templatecontent
if str(theTuple[1]) not in b and "&lt;!--NOOVERRIDE--&gt;" in templatecontent:
# if False:
        a.close()  # close to make way for write connection
        a = open("/home/vacation9/VoxelBot/bot.txt", "w")  # Open in write connection
        a.write(str(theTuple[1]))  # Add current values to previous value file
        a.close()  # A is no longer needed
        print "Template:"
        edit = """<!--This page is edited by VoxelBot. To manually stop VoxelBot from editing this page, change "NOOVERRIDE" below to "OVERRIDE" and please notify Vacation9 and Fox Wilson.-->
<!--NOOVERRIDE-->
{{{{#if:{{{style|}}}|wdefcon/styles/{{{style}}}|{{{prefix|User:Zsinj/}}}Wdefcon}}
|level  = {{WikiDefcon/levels|""" + str(theTuple[1]) + """}}
|sign   = ~~~~~
|info   = """ + str(theTuple[0]) + "/" + str(theTuple[1]) + """ according to ~~~
|align  = {{{align|}}}
|noinfo = {{{noinfo|}}}
|type   = {{{type|}}}
}}<noinclude>
{{documentation}}
</noinclude>"""  # Define template, adding in values
        level = 1 if theTuple[1] >= 20 else 2 if theTuple[1] >= 15 else 3 if theTuple[1] >= 10 else 4 if theTuple[1] >= 5 else 5
        summary = """Update template: level """ + str(level) + """ - """ + str(theTuple[0]) + """/""" + str(theTuple[1]) + """ (per minute)"""
        print edit  # Print for Debugging
        editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": summary, "text": edit, "bot": "true", "title": "Template:Vandalism information"}))  # Define the edit query and execute it
        response = ClientCookie.urlopen(editInfo).read()  # Get the response
        print response  # Print for debugging
else:
        print "No edit needed!"  # If the edit is identical to the previous version it isn't needed!
