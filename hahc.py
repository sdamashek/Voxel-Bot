# By Samuel Damashek
# For Hahc21 and GA Wikiproject
import time
import urllib2 as url
import urllib
import ClientCookie
import sys
import socket
import string
import os
import re
from xml.dom import minidom
from logininfo import *  # import various libraries and the login info
from includes import *
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
giantlistofpages = []


def iloverecursion(passedUrl):
    global giantlistofpages
    listurlcontent = ClientCookie.urlopen(passedUrl).read()  # Make the request
    dom = minidom.parseString(listurlcontent)
    eilist = dom.getElementsByTagName("ei")
    for element in eilist:
        try:
            element = element.attributes['title'].value
            talkpage = ClientCookie.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles=" + element.replace(" ", "_").encode("utf-8")).read()
            talkdom = minidom.parseString(talkpage)
            talkcontent = talkdom.getElementsByTagName("rev")[0].childNodes[0].data
            # print talkcontent[0:200]
            articlere = re.compile("{{ArticleHistory.+?}}", re.DOTALL)
            articlehistory = articlere.search(talkcontent).group(0)
            # print articlehistory
            if "currentstatus=GA" in articlehistory.replace(" ", ""):
                galist = re.compile("action[0-9]+ *?=.+?date *?=.+?[0-9][0-9][0-9][0-9]", re.DOTALL).findall(articlehistory)
                ganlist = []
                for item in galist:
                    print item + "\n"
                    if "=GAN" in item.replace(" ", ""):
                        ganlist = ganlist + [item]
                latestgan = ganlist[len(ganlist) - 1]
                month = re.search("[0-9][0-9]? [a-zA-Z]+? [0-9]+?", latestgan).group(0).split(" ")[1]
                year = re.search("20[0-9]+", latestgan).group(0)
                print month
                print year
                thetuple = month, year, element
                giantlistofpages += [thetuple]
        except IndexError:
            print "Index Error. Most likely the entry wasn't formatted correctly."
        except AttributeError:
            print "Attribute Error"
        # except:
        # print "Unexpected error, could not parse current element/page. Error
        # was ", sys.exc_info()[0]
    if len(dom.getElementsByTagName("embeddedin")) == 2:
        iloverecursion("http://en.wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=Template:ArticleHistory&eilimit=5000&format=xml&eicontinue=" + dom.getElementsByTagName("embeddedin")[1].attributes['eicontinue'].value)
iloverecursion("http://en.wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=Template:ArticleHistory&eilimit=5000&format=xml")
year = datetime.date.today().year
edit = "==" + year + "==\n"
montharray = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
if datetime.date.today().month == 1:
    month = "December"
else:
    month = montharray[datetime.date.today().month - 2]
edit = edit + "===" + month + "===\n{{div col||25em}}"
for page in giantlistofpages:
    print month + " " + year
    if page[0] == month and page[1] == year:
        edit = edit + "[[" + page[2] + "|" + re.split(":", page[2])[1] + "]]\n\n"
edit = edit + "{{div col end}}\n"
editInfo = url.Request("http://en.wikipedia.org/w/api.php", urllib.urlencode({"format": "xml", "action": "edit", "token": x, "summary": "Updating statistics in own userspace. ([[User:VoxelBot/task2|more information]])", "text": edit.encode("utf-8"), "bot": "true", "title": "User:Hahc21/Sweeps_List"}))  # Define the edit query and execute it
response = ClientCookie.urlopen(editInfo).read()  # Get the response
print response  # Print for debugging
