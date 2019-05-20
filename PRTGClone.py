import sys
import csv
import os
import urllib2
import re
import time
import xml.etree.ElementTree as ET

os.getcwd()
os.chdir('/tmp')

sensorId = 0
deviceRoot = ''
grpIdList = []
devIdList = []
sensIdList = []

def getAllDevs():
    buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=devices&output=xml&columns=objid,name&action=1&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    groupRoot = ET.fromstring(response)
    global allDevDict
    allDevDict = {item.find('name').text:item.find('objid').text for item in groupRoot.iter('item')}

def findDev(devName):
    for k,v in allDevDict.items():
        if k == devName:
            print v

def getGroupIds(groupId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=devices&output=xml&columns=objid,name&id=', groupId, '&action=1&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    groupRoot = ET.fromstring(response)
    global grpIdList
    for item in groupRoot.iter('item'):
        print item.find('objid').text
        grpIdList.append(item.find('objid').text)

def getDevIds(groupId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=devices&output=xml&columns=objid,name&id=', groupId, '&action=1&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    groupRoot = ET.fromstring(response)
    global devIdList
    for item in groupRoot.iter('item'):
        print item.find('objid').text
        devIdList.append(item.find('objid').text)


def getDevSensors(devId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=sensors&output=xml&columns=objid,name&id=', devId, '&action=1&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    deviceRoot = ET.fromstring(response)
    global sensIdList
    for item in deviceRoot('item'):
        print item.find('objid').text
        sensIdList.append(item.find('objid').text)


def cloneUrl(cloneId, sensorNameNew, targetId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/duplicateobject.htm?id=', cloneId, '&name=', sensorNameNew, '&targetid=', targetId, '&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).geturl()
    newSensorId = re.search('id%3D(\d+)', response)
    global sensorId
    sensorId = newSensorId.group(1)
    print 'duplicating sensor'

def startUrl(sensorId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/pause.htm?id=', sensorId, '&action=1&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    print 'starting sensor'

def scanUrl(sensorId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/scannow.htm?id=', sensorId, '&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    print 'initiating scan'

def tagUrl(sensorId, newTag):
    receive = ('https://prtg.oc.unlv.edu/api/getobjectproperty.htm?id=', sensorId, '&name=tags', '&username=api_update&passhash=4150398368')
    buildReceiveUrl = ''.join(receive)
    receiveRequest = urllib2.Request(buildReceiveUrl)
    receiveResponse = urllib2.urlopen(receiveRequest).read()
    tags = re.search('\<result\>([ -,a-zA-Z0-9]+)', receiveResponse)
    tagsList = str.split(tags.group(1))
    print tagsList
    tagsStr = ','.join(tagsList)
    newTagsStr = (newTag, ',', tagsStr)
    buildNewTagsStr = ''.join(newTagsStr)
    print buildNewTagsStr
    send = ('https://prtg.oc.unlv.edu/api/setobjectproperty.htm?id=', sensorId, '&name=tags&value=', buildNewTagsStr, '&username=api_update&passhash=4150398368')
    buildSendUrl = ''.join(send)
    print buildSendUrl
    sendRequest = urllib2.Request(buildSendUrl)
    sendResponse = urllib2.urlopen(sendRequest).read()
    print 'tagging', sendResponse

# def commentUrl(sensorId, comment):
#     buildUrl = ('https://prtg.oc.unlv.edu/api/setobjectproperty.htm?id=', sensorId, '&name=comments&value=', comment, '&username=api_update&passhash=4150398368')
#     buildUrlStr = ''.join(buildUrl)
#     request = urllib2.Request(buildUrlStr)
#     response = urllib2.urlopen(request).read()
#     print buildUrlStr
#     print 'added comment'

sensorIdList = ['11641', '11642', '11643', '11644', '11645', '11646', '11647', '11648', '11649', '11650']
dnsServerNameList = ['ns2', 'ns3', 'ns4']
newTag = 'pri-oc-info_only'
getDevSensors('9607')
comment = "Steps:\n1.  Check if website is available (up/down).  If down start \"unconfirmed\" incident.\n2.  Escalate to Cyndi Backstrom 581-1684"


with open('prtgapitest.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        devName = row[0]
        targetId = row[1]
        for item in root.iter('item'):
            for child in item:
                for i in sensorIdList:
                    if i == child.text:
                        cloneId = i
                        sensorName = item.find('name').text
                        repl = ('(', devName,)
                        buildRepl = ''.join(repl)
                        sensorNameNew = re.sub('\(ns1', buildRepl, sensorName)
                        cloneUrl(cloneId, sensorNameNew, targetId)
                        startUrl(sensorId)
                        scanUrl(sensorId)
                        tagUrl(sensorId, newTag)
                        # commentUrl(sensorId, comment)
                        print sensorId, sensorNameNew



buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=devices&output=xml&columns=objid,name&id=', groupId, '&action=1&username=api_update&passhash=4150398368')
buildUrlStr = ''.join(buildUrl)
request = urllib2.Request(buildUrlStr)
response = urllib2.urlopen(request).read()
groupRoot = ET.fromstring(response)

for item in groupRoot.iter('item'):
    print item.find('objid').text
    devIdList.append(item.find('objid').text)

buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=sensors&output=xml&columns=objid,name&id=', '11581', '&action=1&username=api_update&passhash=4150398368')
buildUrlStr = ''.join(buildUrl)
request = urllib2.Request(buildUrlStr)
response = urllib2.urlopen(request).read()
deviceRoot = ET.fromstring(response)
global sensIdList
for item in deviceRoot('item'):
    print item.find('objid').text


