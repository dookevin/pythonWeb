#utf-8
import urllib,httplib,sys,json

def createsingle1():
    params=urllib.urlencode({'rtype':'0','disks':'1'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/createraid',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def createsingle2():
    params=urllib.urlencode({'rtype':'0','disks':'1,2'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/createraid',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def createraid1():
    params=urllib.urlencode({'rtype':'1','disks':'1,2'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/createraid',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def delraid():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/delraid',"",headers)
    response = httpClient.getresponse()
    print json.load(response)

def addraid():
    params=urllib.urlencode({'disk':'2'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/addraid',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def getrdinfo():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/getrdinfo',"",headers)
    response = httpClient.getresponse()
    print json.load(response)

def ifraid():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/ifraid',"",headers)
    response = httpClient.getresponse()
    print json.load(response)

def winviewedit(st):
    params=urllib.urlencode({'usertype':'2','bios':'412322','workgroup':st})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/winviewedit',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def getwinview():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/getwinview',"",headers)
    response = httpClient.getresponse()
    print json.load(response)

def addsharefolder():
    params=urllib.urlencode({'name':'2!@#!%$#^$*()','description':'vasdf2','available':'1','option':'0','allowguest':'1','group':'aaaaaa bbbbbb','rogroup':'cccccc dddddd'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/setsharefolder',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def editsharefolder(a,b):
    params=urllib.urlencode({'name':'$%^!@$&124','description':'bn8ayg','available':a,'option':b,'allowguest':'1','group':'aaaaaa bbbbbb cccccc','rogroup':'dddddd'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/editsharefolder',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def delsharefolder(st):
    params=urllib.urlencode({'sid':st})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/delsharefolder',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def getsflist():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/getsflist',"",headers)
    response = httpClient.getresponse()
    print json.load(response)

def tmset():
    params=urllib.urlencode({'name':'vasdfsdf','size':'10'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/tmadd',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def tmget():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/tmget',"",headers)
    response = httpClient.getresponse()
    print json.load(response)

def tmdel(sv):
    params=urllib.urlencode({'uuid':sv})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/tmdel',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def tmedit(sv):
    params=urllib.urlencode({'name':'t2789f1','size':'20','uuid':sv})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/tmedit',params,headers)
    response = httpClient.getresponse()
    print json.load(response)

def checkupdate():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/checkversion',"",headers)
    response = httpClient.getresponse()
    print json.load(response)

def doupgrade():
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('127.0.0.1',80,timeout=30)
    httpClient.request('POST','/default/system/doupgrade',"",headers)
    response = httpClient.getresponse()
    print json.load(response)


if sys.argv[1]=="1":
    createsingle1()
elif sys.argv[1]=="2":
    createsingle2()
elif sys.argv[1]=="3":
    createraid1()
elif sys.argv[1]=="4":
    delraid()
elif sys.argv[1]=="5":
    addraid()
elif sys.argv[1]=="6":
    getrdinfo()
elif sys.argv[1]=="7":
    ifraid()
elif sys.argv[1]=="8":
    winviewedit(sys.argv[2])
elif sys.argv[1]=="9":
    getwinview()
elif sys.argv[1]=="10":
    addsharefolder()
elif sys.argv[1]=="11":
    editsharefolder(sys.argv[2],sys.argv[3])
elif sys.argv[1]=="12":
    delsharefolder(sys.argv[2])
elif sys.argv[1]=="13":
    getsflist()
elif sys.argv[1]=="14":
    tmset()
elif sys.argv[1]=="15":
    tmget()
elif sys.argv[1]=="16":
    tmdel(sys.argv[2])
elif sys.argv[1]=="17":
    tmedit(sys.argv[2])
elif sys.argv[1]=="18":
    checkupdate()
elif sys.argv[1]=="19":
    doupgrade()


