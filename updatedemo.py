#coding:utf-8
import socket,httplib,json,urllib,os
import MySQLdb
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from threading import Timer
from multiprocessing import Process 
import hashlib
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
expires = datetime.timedelta(days=1)

tcp1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
tcp1.bind(('',51234))
tcp1.listen(5)
x="""HTTP/1.1 200 OK

"""

def checkupdate(chosen=1):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='wenshang',db='mininas',port=3306)
    cur=conn.cursor()
    cur.execute('select * from mini_syssetting where id=1')
    s=cur.fetchone()
    cur.close()
    conn.close()
    if s[5]==1:
        input =open("/etc/mininas/version")
        lines=input.read()
        input.close()
        ss= lines.split("\n")
        t=ss[0].split(" ")
        sv=t[1]+"."+t[2]+"."+t[3]
        input =open("/etc/mininas/hardversion")
        lines=input.read()
        input.close()
        ss= lines.split("\n")
        hv=ss[0]
        input =open("/etc/mininas/updatedversion")
        lines=input.read()
        input.close()
        ss= lines.split("\n")
        uv=ss[0]
        input =open("/etc/mininas/luv")
        lines=input.read()
        input.close()
        ss= lines.split("\n")
        shuv=ss[0].split("--/--")
        result=os.popen("ls /etc/mininas/ | grep updatelist").read()
        if shuv[0]==sv and shuv[1]==hv and shuv[2]==uv and result != "":
            if chosen==2:
                return getjson(sv)
            elif chosen==1:
                print "----------"
                downfile()
        else :
            params=urllib.urlencode({'sv':sv,'hv':hv,'uv':uv})
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            httpClient = httplib.HTTPConnection('www.winsuntech.cn',80,timeout=30)
            httpClient.request('POST','/NasUpdate/index.aspx',params,headers)
            response = httpClient.getresponse()
            re=response.read().split("\r")
            re1=re[0].split("\n")
            httpClient.close()
            p="wget %s -P /etc/mininas/"%(re1[0])
            os.system(p)
            input =open("/etc/mininas/luv","w")
            ws="%s--/--%s--/--%s"%(sv,hv,uv)
            input.write(ws)
            input.close()
            if chosen==2:
                return getjson(sv)
            elif chosen==1:
                print "----------"
                downfile()

def doupgrade(ver):
    input =open("/etc/mininas/updatelist.txt")
    lines=input.readlines()
    input.close()
    print ver
    for l in lines:
        if "lastest" in l:
            continue
        if "lastest" not in l and ver in l:
            dl=l.split("\n")
            dl1=dl[0].split("\r")
            dls=dl1[0].split(" ")
            conn=MySQLdb.connect(host='localhost',user='root',passwd='wenshang',db='mininas',port=3306)
            cur=conn.cursor()
            cur.execute('select * from mini_syssetting where id=1')
            rpath=cur.fetchone()
            cur.close()
            conn.close()
            path=str(rpath[1])+"update/"
            o="ls %s | grep %s"%(path,dls[4])
            print o
            result=os.popen(o).readlines()
            if result:
                m=hashlib.md5()
                i="%supdate/%s"%(rpath[1],dls[4])
                print i
                input =open(i,'rb')
                while 1:
                    blk = input.read(4096)
                    if not blk:
                        break
                    m.update(blk)
                n=m.hexdigest().upper()
                input.close()
                if n==dls[6]:
                    ip=updatego(path,dls[4])
            else :
                p="wget %s -P %s"%(dls[1],path)
                os.system(p)
                ip=updatego(path,dls[4])
    return ip

def updatego(path,name):
    #o="tar zcvf %s%s -P /dev/mmcblk0p2/"%(path,name)
    #os.system(o)
    ls=os.popen("ifconfig").readlines()
    i=0
    data={}
    data['returncode']="100100000"
    for l in ls:
        if i == 1:
            data2={}
            s=l.split(":")
            t=s[1].split(" ")
            data2['ip']=t[0]
            i=0
            data['data']=data2
            break
        if "eth0" in l:
            i =1
    tt=Timer(10,sup)
    tt.start()
    print data
    return json.dumps(data)

def sup():
    print 111
    
def getjson(sv):
    input =open("/etc/mininas/updatelist.txt")
    lines=input.readlines()
    input.close()
    data={}
    data['returncode']="100100000"
    data2={}
    uplist=[]
    for l in lines:
        if "lastest" in l:
            ls=l.split("\n")
            ls1=ls[0].split("\r")
            lss=ls1[0].split(" ")
            continue
        if lss[1] in l:
            dl=l.split("\n")
            dls=dl[0].split(" ")
            data3={}
            data3['version']=dls[0]
            data3['des']=dls[3].decode("GBK")
            data3['date']=dls[2]
            data3['status']=dls[5]
            data2['lastest']=data3
        else:
            dl=l.split("\n")
            dls=dl[0].split(" ")
            data4={}
            data4['version']=dls[0]
            data4['des']=dls[3].decode("GBK")
            data4['date']=dls[2]
            data4['status']=dls[5]
            uplist.append(data4)
    data2['list']=uplist
    data2['nowversion']=sv
    data['data']=data2
    print data
    ejson = json.dumps(data)
    return ejson

def downfile():
    input =open("/etc/mininas/updatelist.txt")
    lines=input.readlines()
    input.close()
    conn=MySQLdb.connect(host='localhost',user='root',passwd='wenshang',db='mininas',port=3306)
    cur=conn.cursor()
    cur.execute('select * from mini_syssetting where id=1')
    rpath=cur.fetchone()
    cur.close()
    conn.close()
    for l in lines:
        if "lastest" in l:
            continue
        ll=l.split("\n")
        ll1=ll[0].split("\r")
        sp=ll1[0].split(" ")
        o="ls %supdate/ | grep %s"%(rpath[1],sp[4])
        result=os.popen(o).read()
        if result:
            m=hashlib.md5()
            i="%supdate/%s"%(rpath[1],sp[4])
            input =open(i,'rb')
            while 1:
                blk = input.read(4096)
                if not blk:
                    break
                m.update(blk)
            n=m.hexdigest().upper()
            input.close()
            if n==sp[6]:
                continue
            else:
                q="rm %s"%i
                os.system(q)
                p="wget %s -P %supdate/"%(sp[1],rpath[1])
                os.system(p)
        else :
            p="wget %s -P %supdate/"%(sp[1],rpath[1])
            os.system(p)

def autocheckupgrade():
    version="3.0.1"
    params=urllib.urlencode({'version':version})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    httpClient = httplib.HTTPConnection('www.winsuntech.cn',80,timeout=30)
    httpClient.request('POST','/NasUpdate/sversion.aspx',params,headers)
    response = httpClient.getresponse()
    re=response.read().split("\r")
    re1=re[0].split("\n")
    httpClient.close()
    re2=re1[0].split("-")
    re3=re2[1].split(".")
    re4=version.split(".")
    if int(re3[2])>int(re4[2]):
        print 1111
    p="wget %s -P /tmp/"%(re1[0])
    os.system(p)

def doupdate(version):
    t="/etc/mininas/update/mininasupguide.sh /tmp/mininas-%s.tar.gz"%(version)
    os.system(t)
    i="rm /tmp/mininas-%s.tar.gz"%(version)
    os.system(i)

def cronjob():
    scheduler = BlockingScheduler()
    print "*******"
    scheduler.add_job(checkupdate,'cron', second='0', hour='2',minute='0')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

child_proc = Process(target=cronjob)
child_proc.start()

while 1:
    y="""HTTP/1.1 200 OK

"""
    
    clientsock1,clientaddr1 = tcp1.accept()
    print ("Got 1", clientsock1.getpeername())
    data = clientsock1.recv(4096)
    now = datetime.datetime.utcnow()
    if len(data)>5:
        dl=data.split(":")
        if dl[0] == "10102":
            ejson=doupgrade(dl[1])
            clientsock1.send(ejson)
            clientsock1.close()
        else :
            input =open("/mnt/updatestatus.txt")
            lines=input.read()
            input.close()
            ss= lines.split("\n")
            y=y+"<script>window.name = "+ss[0]+"; </script>"
            n=clientsock1.send(y)
            clientsock1.close()
    else:
        if data == "10100":
            ejson=checkupdate(2)
            clientsock1.send(ejson)
            clientsock1.close()
        else :
            input =open("/mnt/updatestatus.txt")
            lines=input.read()
            input.close()
            ss= lines.split("\n")
            rd={}
            rd['data']=ss[0]
            rd1=json.dumps(rd)
            y=y+rd1
            #y=y+"<html><head></head><body><span>$"+ss[0]+"$</span></body><html>"
            n=clientsock1.send(y)
            clientsock1.close()