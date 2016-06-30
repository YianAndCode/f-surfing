#!/usr/bin/env python
import urllib2
import time
import json
import os
import platform

####### CONFIG AREA #######

# Username, your student ID
USERNAME = "StudentID"

# Password, your password for esurfing client, not for iNode client
PASSWORD = "Password"

# Net Auth Server IP, the IP 113.105.243.254 is for FOSU
NASIP = "113.105.243.254"

####### CONFIG AREA #######


# iswifi, the default value is 1050, I don't know what it mean
#         other values: 4060, 4070
ISWIFI = "1050"

BASEURL = "http://enet.10000.gd.cn:10001/client/"
LOGINURL = BASEURL + "login"
CHALLENGEURL = BASEURL + "challenge"
HEARTBEATURL = "http://enet.10000.gd.cn:8001/hbservice/client/active?"
CHECKINTERNETURL = "http://www.qq.com"

SECRET = "Eshore!@#"

UA = "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"

ISOTIMEFORMAT='%Y-%m-%d %X'

def get_ip_address():
    if platform.system() == "Windows":
        import socket
        ipList = socket.gethostbyname_ex(socket.gethostname())
        j = 0
        print "Index | IP"
        for i in ipList[2]:
            print j, "     ",i
            j = j + 1
        index = int(raw_input("Please input the index number of you IP address.(Usually, the IP looks like 10.xxx.xxx.xxx):\n"))
        if index >= 0 and index < len(ipList[2]):
            return ipList[2][index]
        else:
            print "Invalid Index number"
            exit()
    ip=os.popen(". /lib/functions/network.sh; network_get_ipaddr ip wan; echo $ip").read()
    ip2=str(ip).split("\n")[0]
    return ip2

IP = get_ip_address()

def get_mac_address():
    if platform.system() == "Windows":
        import uuid
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
        return "-".join([mac[e:e+2] for e in range(0,11,2)]).upper()
    ic=os.popen("ifconfig |grep -B1 \'"+ IP +"\' |awk \'/HWaddr/ { print $5 }\'").read()
    ic=str(ic).split("\n")[0]
    ic=ic.replace(":","-")
    return ic.upper()

MAC = get_mac_address()

print "Your IP is: ", str(IP)
print "Your MAC is: ", str(MAC)

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest().upper()
    
def timestamp():
    return int(time.time() * 1000) / 1
    
def formattime():
    return time.strftime(ISOTIMEFORMAT, time.localtime(time.time())) + " "


def get_token(response):
    if response != "failed":
        # DEBUG
        print response

        result = response.split("\",\"")[0]
        result = result.split("\":\"")[-1]
        print formattime(), "Token is: ", result
        return result
    return "failed"
    
def post_challenge():
    strtime = str(timestamp())
    authenticator = md5(str(IP + NASIP + MAC + strtime + SECRET))
    # DEBUG
    datas = {"username" : USERNAME, "clientip" : IP, "nasip" : NASIP, "mac" : MAC, "timestamp" : strtime, "authenticator" : authenticator}
    postdata = json.dumps(datas)
    # DEBUG
    req = urllib2.Request(CHALLENGEURL, postdata)
    req.add_header('User-agent', UA)
    try:
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.HTTPError, e:
        print formattime(), str(e.code)
        print formattime(), str(e.reason)
        return "failed"
    except urllib2.URLError, e:
        print formattime(), str(e.reason)
        return "failed"
    
def post_login(token):
    strtime = str(timestamp())
    authenticator = md5(str(IP + NASIP + MAC + strtime + token + SECRET))
    # DEBUG
    datas = {"username" : USERNAME, "password" : PASSWORD, "clientip" : IP, "nasip" : NASIP, "mac" : MAC, "timestamp" : strtime, "authenticator" : authenticator, "iswifi" : ISWIFI}
    postdata = json.dumps(datas)
    # DEBUG
    req = urllib2.Request(LOGINURL, postdata)
    req.add_header('User-agent', UA)
    try:
        print formattime(), "Send login info"
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.HTTPError, e:
        print formattime(), str(e.code)
        print formattime(), str(e.reason)
        return "failed"
    except urllib2.URLError, e:
        print formattime(), str(e.reason)
        return "failed"
    
def heartbeat():
    strtime = str(timestamp())
    authenticator = md5(str(IP + NASIP + MAC + strtime + SECRET))
    url = HEARTBEATURL + "username=" + USERNAME + "&clientip=" + IP + "&nasip=" + NASIP + "&mac=" + MAC + "&timestamp=" + strtime + "&authenticator=" + authenticator
    req = urllib2.Request(url)
    # DEBUG
    print url
    req.add_header('User-agent', UA)
    try:
        print formattime(), "Send heartbeat"
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.HTTPError, e:
        print formattime(), str(e.code)
        print formattime(), str(e.reason)
        return "failed"
    except urllib2.URLError, e:
        print formattime(), str(e.reason)
        return "failed"
    
def keep_heartbeat():
    while True:
        result = heartbeat()
        if result != "failed":
            print formattime(), result
            code = result.split('\"')[3]
            print formattime(), "The code is:", code
            if code == "0":
                time.sleep(60)
                continue
            elif code == "1":
                login()
                continue
            elif code == "2":
                break
            else:
                continue
    
def login():
    code = ""
    for i in range(0, 5):
        result = post_login(get_token(post_challenge()))
        print formattime(), result
        if result != "failed":
            code = result.split('\"')[3]
            if code == "0":
                break
            elif code == "11064000":
                print formattime(), "User had been blocked"
                exit();
        time.sleep(5)
    return result
    
def main():
    while True:
        try:
            for i  in range(0, 5):
                tester = urllib2.urlopen(CHECKINTERNETURL)
                if(tester.geturl() == CHECKINTERNETURL):
                    result = heartbeat()
                    print formattime(), result
                    if result != "failed":
                        code = result.split('\"')[3]
                        print formattime(), "The code is:", code
                        if code == "0":
                            break
                        elif code == "2":
                            print "Failed"
                            exit()
                print formattime(), "Loging..."
                login()
                sleep(5)
            
            time.sleep(60)
            keep_heartbeat()

        except urllib2.HTTPError, e:
            print formattime(), str(e.code)
            print formattime(), str(e.reason)
        except urllib2.URLError, e:
            print formattime(), str(e.reason)

if __name__ == '__main__':
    main()