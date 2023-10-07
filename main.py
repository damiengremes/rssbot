import feedparser
import requests
import time
import calendar

# insert your desired RSS feeds in the following list - two example already given
feed = ['https://www.bleepingcomputer.com/feed/','https://krebsonsecurity.com/feed/']

# insert the link to your Discord webhook
webhookurl = ""

# this file needs to exist, even if empty - will be used to check new articles since last runtime
prevtxt = 'previous.txt'

def getPreviousRunTime():
	file = open(prevtxt,'r')
	prtime = file.readlines()
	file.close()
	for inttime in prtime:
		ftime = str(inttime)
	return float(inttime)

def setNewRunTime(newtime):
	file = open(prevtxt,'w')
	file.write(newtime)
	file.close()
	return

def timeEpochToStruct(timein):
	return time.gmtime(timein)

def timeStructToEpoch(timein):
	return calendar.timegm(timein)

def postToDiscord(title,author,date,link):
	message = {
		"content": ":newspaper: | **{}** by {} on {}:\n{}".format(title,author,date,link)
	}
	requests.post(webhookurl,data=message)

oldTime = getPreviousRunTime()
newTime = str(time.time())

for site in feed:
	rssfeed = feedparser.parse(site)
	for news in range(len(rssfeed)-1):
		try:
			title=rssfeed.entries[news].title
			link=rssfeed.entries[news].link
			author=rssfeed.entries[news].author
			date=rssfeed.entries[news].published
			timed=rssfeed.entries[news].published_parsed
			#print("**{}** by {} on {}:\n{}".format(title,author,date,link))
			if(timeStructToEpoch(timed)>oldTime):
				#print("**{}** by {} on {}:\n{}".format(title,author,date,link))
				postToDiscord(title,author,date,link)
				time.sleep(2)
		except:
			pass

	setNewRunTime(newTime)
