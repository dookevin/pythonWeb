#coding=utf-8
import os,json,re

#def getdiskinfo(dname):
#    ys="udevadm info --query=all --name=/dev/%s"%dname
#    yl=os.popen(ys).readlines()
#    data={}
#    for y in yl:
#        if 'ID_SERIAL=' in y:
#            yyt=y.split('=')
#            x=yyt[1].split('\n')
#            data['sn']=x[0]
#        if 'ID_ATA_ROTATION_RATE_RPM=' in y:
#            c=y.split('=')
#            x=c[1].split('\n')
#            data['rotationrate']=x[0]
#        if 'ID_VENDOR=' in y:
#            c=y.split('=')
#            x=c[1].split('\n')
#            data['vendor']=x[0]
#        if 'ID_TYPE=' in y:
#            c=y.split('=')
#            x=c[1].split('\n')
#            data['type']=x[0]
#        if 'DEVNAME=' in y:
#            c=y.split('=')
#            x=c[1].split('\n')
#            data['devname']=x[0]
#        if 'ID_MODEL=' in y:
#            c=y.split('=')
#            x=c[1].split('\n')
#            data['model']=x[0]
#        if 'ID_SERIAL_SHORT=' in y:
#            c=y.split('=')
#            x=c[1].split('\n')
#            data['snshort']=x[0]
#        if 'ID_BUS=' in y:
#            c=y.split('=')
#            x=c[1].split('\n')
#            data['bus']=x[0]
#    ss="lsblk -lnb | grep %s | grep disk| awk '{print $4}'"%dname
#    s = os.popen(ss).read()
#    if data.get('bus') == "ata":
#        data['capacity'] = str(int(s)/(1024*1024*1024))+" GB"
#    else:
#        return 0
#    return data
#
#def getalldisks():
#    sflist=[]
#    si=os.popen("blkid | grep /dev/sd").readlines()
#    for s in si:
#        pts=s.split(":")
#        dn=re.sub('[^A-Za-z]','',pts[0])
#        rd=dn.split("dev")
#        if rd[1] not in sflist:
#            sflist.append(rd[1])
#    return sflist
#
#def getdiskname(sn):
#    si=os.popen("blkid | grep /dev/sd").readlines()
#    for s in si:
#        pts=s.split(":")
#        dn=re.sub('[^A-Za-z]','',pts[0])
#        rd=dn.split("dev")
#        ls=os.popen("udevadm info --query=all --name=/dev/%s | grep ID_SERIAL="%rd[1]).readlines()
#        for l in ls:
#            if sn in l:
#                return rd[1]
#    return 0
#
#def recorddiskinfo(type,label,version,uuid,disk):
#    data={}
#    sflist = []
#    for e in disk:
#        data2={}
#        data2['disk']=getdiskinfo(e)
#        data2['subuuid']=getsubuuid(e)
#        sflist.append(data2)
#    data['subset']=sflist
#    data['version']=version
#    data['label']=label
#    data['uuid']=uuid
#    data['mode']=type
#    input =open("/etc/mininas/data/configs/volume.json",'w')
#    input.write(str(data))
#    input.close()
#
#def checkrdinfo():
#    input=open("/etc/mininas/data/configs/volume.json")
#    d=input.read()
#    input.close()
#    if d:
#        data=eval(d)
#        uid=data.get('uuid')
#        dcheck= os.popen("btrfs filesystem show").readlines()
#        cp0=0
#        for ds in dcheck:
#            if uid in ds:
#                cp0=1
#        if cp0 == 1:
#            cp1=0
#            for f in data.get('subset'):
#                suid=f.get('subuuid')
#                edcheck= os.popen("blkid | grep /dev/sd").readlines()
#                for esd in edcheck:
#                    if suid in esd:
#                        cp1=cp1+1
#            if cp1 == len(data.get('subset')):
#                #correct
#                return 100
#            elif cp1==0:
#                #missing both disks
#                return 102
#            elif cp1 < len(data.get('subset')):
#                #missing 1 disk
#                return 101
#        else :
#            #missing both disks
#            return 102
#    else:
#        return 103
#
#def searchdisk(sn):
#    si=os.popen("blkid | grep /dev/sd").readlines()
#    for s in si:
#        pts=s.split(":")
#        dn=re.sub('[^A-Za-z]','',pts[0])
#        rd=dn.split("dev")
#        ls=os.popen("udevadm info --query=all --name=/dev/%s | grep ID_SERIAL="%rd[1]).readlines()
#        for l in ls:
#            if sn in l:
#                return 1
#    return 0
#
#def clearjson():
#    input=open("/etc/mininas/data/configs/volume.json","w")
#    input.close()
#
#def getlastrdinfo():
#    input=open("/etc/mininas/data/configs/volume.json")
#    d=input.read()
#    input.close()
#    if d:
#        return eval(d)
#    else:
#        return null
#
#def getdisklist(uuid):
#    sflist=[]
#    si=os.popen("blkid | grep /dev/sd").readlines()
#    for s in si:
#        if uuid in s:
#            pts=s.split(":")
#            dn=re.sub('[^A-Za-z]','',pts[0])
#            rd=dn.split("dev")
#            if dn not in sflist:
#                sflist.append(rd[1])
#    return sflist
#
#def createsingle(dname,da):
#    o="mkfs.btrfs -f -L %s -d single /dev/%s"%(dname,da)
#    os.system(o)
#    #o="/mnt/%s"%dname
#    #os.makedirs(o)
#    o="mount /dev/%s /mnt/%s"%(da,dname)
#    os.system(o)
#    label=dname
#    type="single"
#    version="1.0.0"
#    recorddiskinfo(type,label,version,getuuid(),getdisklist(getuuid()))
#
#def createsingle2(dname,da,db):
#    o="mkfs.btrfs -f -L %s -d single /dev/%s /dev/%s"%(dname,da,db)
#    os.system(o)
#    o="mount /dev/%s /mnt/%s"%(da,dname)
#    os.system(o)
#    label=dname
#    type="single"
#    version="1.0.0"
#    recorddiskinfo(type,label,version,getuuid(),getdisklist(getuuid()))
#
#def addsingle(db):
#    data=getlastrdinfo()
#    o="btrfs device add -f /dev/%s /mnt/%s"%(db,data.get('label'))
#    os.system(o)
#    label=data.get('label')
#    type="single"
#    version="1.0.0"
#    recorddiskinfo(type,label,version,getuuid(),getdisklist(getuuid()))
#
#def createraid1(dname,da,db):
#    o="mkfs.btrfs -f -L %s -m raid1 -d raid1 /dev/%s /dev/%s"%(dname,da,db)
#    os.system(o)
#    o="mount /dev/%s /mnt/%s"%(da,dname)
#    os.system(o)
#    label=dname
#    type="raid1"
#    version="1.0.0"
#    recorddiskinfo(type,label,version,getuuid(),getdisklist(getuuid()))
#
#def delraid(dname):
#    o="umount /mnt/%s"%(dname)
#    os.system(o)
#
#def getuuid():
#    rc=os.popen("btrfs filesystem show").readlines()
#    for e in rc:
#        if "uuid" in e:
#            s=e.split("uuid: ")
#            ss=s[1].split("\n")
#            return ss[0]
#    return 0
#
#def getsubuuid(dname):
#    rc=os.popen("blkid /dev/%s"%dname).read()
#    rb=rc.split('UUID_SUB="')
#    rd=rb[1].split('"')
#    return rd[0]
#
#def prereplace(sda,rname):
#    o="mount -o degraded /dev/%s /mnt/%s"%(sda,rname)
#    os.system(o)
#
#def replacedisk(sdx,sdb,rname):
#    o="btrfs replace start %s /dev/%s /mnt/%s -f"%(sdx,sdb,rname)
#    os.system(o)
#
#def doreplace():
#    rd1=getlastrdinfo()
#    rname = rd1.get('label')
#    rlist=getalldisks()
#    for p in rlist:
#        c=0
#        r = getdiskinfo(p)
#        if r==0:
#            continue
#        else:
#            for e in rd1.get('subset'):
#                if r.get('sn') == e.get('disk').get('sn'):
#                    c=1
#            if c == 1:
#                sdy = p
#            else:
#                sdn = p
#    lines=os.popen("btrfs filesystem show %s"%rd1.get('uuid')).readlines()
#    for l in lines:
#        if "warning" in l and "missing" in l:
#            st=re.sub('[^0-9]','',l)
#    ss1="lsblk -lnb | grep %s | grep disk| awk '{print $4}'"%sdy
#    ss2="lsblk -lnb | grep %s | grep disk| awk '{print $4}'"%sdn
#    dd1 = os.popen(ss1).read()
#    dd2 = os.popen(ss2).read()
#    if dd2> dd1 :
#        prereplace(sdy,rname)
#        replacedisk(st,sdn,rname)
#        label=rd1.get('label')
#        type="raid1"
#        version="1.0.0"
#        recorddiskinfo(type,label,version,getuuid(),getdisklist(getuuid()))
#        return 1
#    return 0

pathchassis="/run/mininas/dvm/chassis/"
pathpools="/run/mininas/dvm/pools/"
pathvolumes="/run/mininas/dvm/volumes/"

def getrotationrate(slot):
    data = os.popen("cat %s%s/disk/id_ata_rotation_rate_rpm"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getmodel(slot):
    data = os.popen("cat %s%s/disk/id_model"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getserialshort(slot):
    data = os.popen("cat %s%s/disk/id_serial_short"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getsize(slot):
    data = os.popen("cat %s%s/disk/attr_size"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getuuid(slot):
    data = os.popen("cat %s%s/fs/id_fs_uuid"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getsubuuid(slot):
    data = os.popen("cat %s%s/fs/id_fs_uuid_sub"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getrotationratehistory(slot):
    data = os.popen("cat %s1/snapshot/ready/%s/disk/id_ata_rotation_rate_rpm"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getmodelhistory(slot):
    data = os.popen("cat %s1/snapshot/ready/%s/disk/id_model"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getserialshorthistory(slot):
    data = os.popen("cat %s1/snapshot/ready/%s/disk/id_serial_short"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getsizehistory(slot):
    data = os.popen("cat %s1/snapshot/ready/%s/disk/attr_size"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getuuidhistory(slot):
    data = os.popen("cat %s1/snapshot/ready/%s/fs/id_fs_uuid"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getsubuuidhistory(slot):
    data = os.popen("cat %s1/snapshot/ready/%s/fs/id_fs_uuid_sub"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def ifpoolsmounted(slot):
    data = os.popen("cat %s%s/mounted"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def haspools(slot):
    data = os.popen("cat %s%s/mounted"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def ifdiskmounted(slot):
    data = os.popen("cat %s%s/mounted"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def ifdiskpath(slot):
    data = os.popen("cat %s%s/path"%(pathchassis,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getvtype(slot):
    data = os.popen("cat %s%s/volume/usage/data"%(pathpools,slot)).read()
    if data:
        data1 = data.split('\n')
        data2 = data1[0].split('\r')
        return data2[0]
    else:
        return data

def ifslotempty(slot):
    data = os.listdir("%s%s"%(pathchassis,slot))
    if data:
        return 1
    return 0

def ifvolumeempty(slot):
    data = os.listdir("%s%s/volume"%(pathpools,slot))
    if data:
        return 1
    return 0

def getreadydisks(slot):
    list = []
    data = os.popen("ls -1 %s%s/volume/ready"%(pathpools,slot)).readlines()
    for l in data:
        l1=l.split("\n")
        l2=l1[0].split("\r")
        list.append(l2[0])
    return list

def getdisklist():
    list = []
    data = os.popen("ls -1 %s"%(pathchassis)).readlines()
    for l in data:
        l1=l.split("\n")
        l2=l1[0].split("\r")
        list.append(l2[0])
    return list

def gethistory(slot):
    list = []
    data = os.popen("ls -1 %s%s/snapshot/ready"%(pathpools,slot)).readlines()
    for l in data:
        l1=l.split("\n")
        l2=l1[0].split("\r")
        list.append(l2[0])
    return list

def getvolumetype(slot):
    data = os.popen("cat %s%s/volume/usage/data"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getvolumeuuid(slot):
    data = os.popen("cat %s%s/volume/uuid"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getvolumetotal(slot):
    data = os.popen("cat %s%s/volume/total"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]

def getvolumestatus(slot):
    data = os.popen("cat %s%s/enabled"%(pathpools,slot)).read()
    data1 = data.split('\n')
    data2 = data1[0].split('\r')
    return data2[0]
