#!/usr/bin/env python
import os
import sys
import time
import urllib
import urllib2
import xml.dom.minidom as XML

def demonize():
    s = os.fork()
    if(s!=0):
        sys.exit()
    pid = os.getpid()
    pidfile = open('cyberoam.pid', 'w')
    pidfile.write(str(pid))
    pidfile.close()

def sendLoginRequest(username, password):
    url = 'http://172.16.68.6:8090/login.xml'
    post_data = 'mode=191' + '&username=' + username + '&password=' + password
    try:
        req = urllib2.Request(url, post_data)
        response = urllib2.urlopen(req)
        xml_dom = XML.parseString(response.read())
        document = xml_dom.documentElement
        response = document.getElementsByTagName('message')[0].childNodes[0].nodeValue
        if 'successfully' in response:
            return True
    except:
        return False

def sendLogoutRequest(username):
    url = 'http://172.16.68.6:8090/logout.xml'
    post_data = 'mode=193' + '&username=' + username
    req = urllib2.Request(url, post_data)
    response = urllib2.urlopen(req)
    print 'Logged out.'

def checkLiveStatus(username):
    url = 'http://172.16.68.6:8090/live?mode=192'
    url = url + '&username=' + username
    response = urllib2.urlopen(url).read()
    xml_dom = XML.parseString(response)
    document = xml_dom.documentElement
    status = document.getElementsByTagName('ack')[0].childNodes[0].nodeValue
    if status == 'ack':
        return True
    else:
        return False

def init(username, password):
    demonize()
    while True:
        if not checkLiveStatus(username):
            sendLoginRequest(username, password)
        time.sleep(5)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'login':
        un = sys.argv[2]
        passwd = sys.argv[3]
        init(un, passwd)
    elif cmd == 'logout':
        un = sys.argv[2]
        sendLogoutRequest(un)
    elif cmd == 'status':
        un = sys.argv[2]
        print checkLiveStatus(un)
