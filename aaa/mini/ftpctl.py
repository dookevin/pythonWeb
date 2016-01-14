#utf-8
import os

def loadtemplate():
    input = open("/etc/mininas/templates/proftpd/default")
    lines = input.read()
    input.close()
    return lines

def loadshareset():
    input = open("/etc/mininas/templates/proftpd/expanded")
    lines = input.read()
    input.close()
    return lines

def loadjson():
    input =open("/etc/mininas/data/configs/proftpd.json")
    lines = input.read()
    input.close()
    return eval(lines)

def dosplit(a):
    aa=a.split("\r")
    aaa=aa[0].split("\n")
    return aaa[0]


def editconf(timeout,port,maxc,maxh,maxl,rpath,usertype):
    d1=loadjson()
    sflist=[]
    data={}
    data['FTP_TIMEOUT_IDLE'] = dosplit(timeout)
    data['FTP_PORT'] = dosplit(port)
    data['FTP_MAX_CLIENTS'] = dosplit(maxc)
    data['FTP_MAX_HOST'] = dosplit(maxh)
    data['FTP_MAX_LOGIN'] = dosplit(maxl)
    data['FTP_DEFAULT_ROOT'] = rpath
    if usertype=='1':
        data['FTP_ANONYMOUS_PATH'] = rpath+"admin/Public/"
    input = open("/etc/mininas/data/configs/proftpd.json","w")
    input.write(str(data))
    input.close()
    print data
    makeconf()

def makeconf():
    m1=loadtemplate()
    m2=loadshareset()
    d1=loadjson()
    l1=m1.replace("%%FTP_TIMEOUT_IDLE%%",d1.get('FTP_TIMEOUT_IDLE')).replace("%%FTP_PORT%%",d1.get('FTP_PORT')).replace("%%FTP_MAX_CLIENTS%%",d1.get('FTP_MAX_CLIENTS')).replace("%%FTP_MAX_HOST%%",d1.get('FTP_MAX_HOST')).replace("%%FTP_MAX_LOGIN%%",d1.get('FTP_MAX_LOGIN')).replace("%%FTP_DEFAULT_ROOT%%",d1.get('FTP_DEFAULT_ROOT'))
    l2=""
    if d1.get('FTP_ANONYMOUS_PATH'):
        l2=m2.replace("%%FTP_ANONYMOUS_PATH%%",d1.get('FTP_ANONYMOUS_PATH'))
    l3=l1+l2
    input=open("/etc/proftpd/proftpd.conf","w")
    input.write(l3)
    input.close()
