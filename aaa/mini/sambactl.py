#utf-8
import os

def loadtemplate():
    input = open("/etc/mininas/templates/samba/global")
    lines = input.read()
    input.close()
    return lines

#allow_all
def loadshareset0():
    input = open("/etc/mininas/templates/samba/share_world_rw_without_guest")
    lines = input.read()
    input.close()
    return lines

#1group
def loadshareset1():
    input = open("/etc/mininas/templates/samba/share_group_rw_other_ro_without_guest")
    lines = input.read()
    input.close()
    return lines

#2groups
def loadshareset2():
    input = open("/etc/mininas/templates/samba/share_group_rw_group_ro")
    lines = input.read()
    input.close()
    return lines

def loadjson():
    input =open("/etc/mininas/data/configs/samba.json")
    lines = input.read()
    input.close()
    return eval(lines)

def addsf(sid,allowguest,option,name,des,available,group,rogroup):
    d1=loadjson()
    de=dosplit(des)
    if sid<10:
        id = "00"+str(sid)
    else:
        id = "0"+str(sid)
    se="/mnt/1/nobody/smbshare%s/"%id
    sflist=[]
    data={}
    data['SMB_WORKGROUP']=d1.get('SMB_WORKGROUP')
    data['SMB_NETBIOS_NAME']=d1.get('SMB_NETBIOS_NAME')
    data['SMB_MAP_TO_GUEST']=d1.get('SMB_MAP_TO_GUEST')
    if d1.get('share'):
        for e in d1.get('share'):
            data2={}
            data2['SMB_OPTION'] = e.get('SMB_OPTION')
            data2['SMB_FOLDER_NAME']=e.get('SMB_FOLDER_NAME')
            data2['SMB_COMMENT']=e.get('SMB_COMMENT')
            data2['SMB_FOLDER_PATH']=e.get('SMB_FOLDER_PATH')
            data2['SMB_SID']=e.get('SMB_SID')
            data2['SMB_AVAILABLE']=e.get('SMB_AVAILABLE')
            sflist.append(data2)
    data2={}
    data2['SMB_OPTION'] = option
    data2['SMB_FOLDER_NAME']=name
    data2['SMB_COMMENT']=de
    data2['SMB_FOLDER_PATH']=se
    data2['SMB_SID'] = str(sid)
    data2['SMB_AVAILABLE']=available
    sflist.append(data2)
    data['share']=sflist
    setgroup(sid,group)
    setrogroup(sid,rogroup)
    input = open("/etc/mininas/data/configs/samba.json","w")
    input.write(str(data))
    input.close()
    makeconf()

def setgroup(sid,ul):
    os.system("mininas_share_members -n %d -s '%s'"%(int(sid),str(ul)))

def setrogroup(sid,ul):
    os.system("mininas_share_members -n %d -r -s '%s'"%(int(sid),str(ul)))

def dosplit(a):
    aa=a.split("\r")
    aaa=aa[0].split("\n")
    return aaa[0]

def editsf(sid,name,des,available,option,allowguest,group,rogroup):
    d1=loadjson()
    sflist=[]
    data={}
    data['SMB_WORKGROUP']=d1.get('SMB_WORKGROUP')
    data['SMB_NETBIOS_NAME']=d1.get('SMB_NETBIOS_NAME')
    data['SMB_MAP_TO_GUEST']=d1.get('SMB_MAP_TO_GUEST')
    de=dosplit(des)
    if d1.get('share'):
        for e in d1.get('share'):
            if e.get('SMB_SID')==sid:
                data2={}
                data2['SMB_FOLDER_NAME']=name
                data2['SMB_COMMENT']=des
                data2['SMB_FOLDER_PATH']=e.get('SMB_FOLDER_PATH')
                data2['SMB_AVAILABLE']=available
                data2['SMB_SID']=e.get('SMB_SID')
                data2['SMB_OPTION']=option
                sflist.append(data2)
            else:
                data2={}
                data2['SMB_FOLDER_NAME']=e.get('SMB_FOLDER_NAME')
                data2['SMB_COMMENT']=e.get('SMB_COMMENT')
                data2['SMB_FOLDER_PATH']=e.get('SMB_FOLDER_PATH')
                data2['SMB_AVAILABLE']=e.get('SMB_AVAILABLE')
                data2['SMB_SID']=e.get('SMB_SID')
                data2['SMB_OPTION']=e.get('SMB_OPTION')
                sflist.append(data2)
    setgroup(sid,group)
    setrogroup(sid,rogroup)
    input = open("/etc/mininas/data/configs/samba.json","w")
    input.write(str(data))
    input.close()
    makeconf()

def setnosf():
    m1=loadtemplate()
    d1=loadjson()
    l1=m1.replace("%%SMB_WORKGROUP%%",d1.get('SMB_WORKGROUP')).replace("%%SMB_NETBIOS_NAME%%",d1.get('SMB_NETBIOS_NAME')).replace("%%SMB_MAP_TO_GUEST%%",d1.get('SMB_MAP_TO_GUEST'))
    input=open("/etc/samba/smb.conf","w")
    input.write(l1)
    input.close()
    data={}
    data['SMB_WORKGROUP']=d1.get('SMB_WORKGROUP')
    data['SMB_NETBIOS_NAME']=d1.get('SMB_NETBIOS_NAME')
    data['SMB_MAP_TO_GUEST']=d1.get('SMB_MAP_TO_GUEST')
    input = open("/etc/mininas/data/configs/samba.json","w")
    input.write(str(data))
    input.close()

def delsf(sid):
    d1=loadjson()
    sflist=[]
    data={}
    data['SMB_WORKGROUP']=d1.get('SMB_WORKGROUP')
    data['SMB_NETBIOS_NAME']=d1.get('SMB_NETBIOS_NAME')
    data['SMB_MAP_TO_GUEST']=d1.get('SMB_MAP_TO_GUEST')
    if d1.get('share'):
        for e in d1.get('share'):
            if e.get('SMB_SID')==str(sid):
                continue
            else:
                data2={}
                data2['SMB_FOLDER_NAME']=e.get('SMB_FOLDER_NAME')
                data2['SMB_COMMENT']=e.get('SMB_COMMENT')
                data2['SMB_FOLDER_PATH']=e.get('SMB_FOLDER_PATH')
                data2['SMB_AVAILABLE']=e.get('SMB_AVAILABLE')
                data2['SMB_SID']=e.get('SMB_SID')
                data2['SMB_OPTION']=e.get('SMB_OPTION')
                sflist.append(data2)
        data['share']=sflist
    input = open("/etc/mininas/data/configs/samba.json","w")
    input.write(str(data))
    input.close()
    makeconf()

def editconf(wg,nn,check):
    if check == '1':
        guest = 'bad user'
    else:
        guest = 'never'
    d1=loadjson()
    sflist=[]
    data={}
    data['SMB_WORKGROUP']=wg
    data['SMB_NETBIOS_NAME']=nn
    data['SMB_MAP_TO_GUEST']=guest
    if d1.get('share'):
        for e in d1.get('share'):
            data2={}
            data2['SMB_FOLDER_NAME']=e.get('SMB_FOLDER_NAME')
            data2['SMB_COMMENT']=e.get('SMB_COMMENT')
            data2['SMB_FOLDER_PATH']=e.get('SMB_FOLDER_PATH')
            data2['SMB_AVAILABLE']=e.get('SMB_AVAILABLE')
            data2['SMB_SID']=e.get('SMB_SID')
            data2['SMB_OPTION']=e.get('SMB_OPTION')
            sflist.append(data2)
        data['share']=sflist
    input = open("/etc/mininas/data/configs/samba.json","w")
    input.write(str(data))
    input.close()
    makeconf()

def getsflist():
    d1=loadjson()
    sflist = []
    if d1.get('share'):
        for e in d1.get('share'):
            data2={}
            data2['SMB_FOLDER_NAME']=e.get('SMB_FOLDER_NAME')
            data2['SMB_COMMENT']=e.get('SMB_COMMENT')
            data2['SMB_AVAILABLE']=e.get('SMB_AVAILABLE')
            data2['SMB_SID']=e.get('SMB_SID')
            data2['SMB_OPTION']=e.get('SMB_OPTION')
            data2['group']=os.popen("mininas_share_members -n %s"%e.get('SMB_SID')).read()
            data2['rogroup']=os.popen("mininas_share_members -n %s -r"%e.get('SMB_SID')).read()
            sflist.append(data2)
    return sflist

def makeconf():
    print 0
    m1=loadtemplate()
    print 00
    d1=loadjson()
    l2=""
    print 1
    if d1.get('share'):
        print 2
        for e in d1.get('share'):
            if int(e.get('SMB_SID'))<10:
                id = "00"+str(e.get('SMB_SID'))
            else:
                id = "0"+str(e.get('SMB_SID'))
            print 3
            if e.get('SMB_OPTION') == "0":
                print 4
                m2=loadshareset0()
                print 5
                try:
                    #l2=l2+m2.replace("%%SMB_FOLDER_NAME%%",e.get('SMB_FOLDER_NAME')).replace("%%SMB_COMMENT%%",e.get('SMB_COMMENT')).replace("%%SMB_FOLDER_PATH%%",e.get('SMB_FOLDER_PATH')).replace("%%SMB_FOLDER_AVAIL%%",e.get('SMB_AVAILABLE')).replace("%%SID%%",id)
                    l2 = l2+m2.replace("%%SMB_FOLDER_NAME%%",e.get('SMB_FOLDER_NAME')).replace("%%SMB_COMMENT%%",e.get('SMB_COMMENT')).replace("%%SMB_FOLDER_PATH%%",e.get('SMB_FOLDER_PATH')).replace("%%SMB_FOLDER_AVAIL%%",e.get('SMB_AVAILABLE')).replace("%%SID%%",id)
                except ttt:
                    print ttt
            elif e.get('SMB_OPTION') == "1":
                print 41
                m2=loadshareset1()
                print 51
                l2=l2+m2.replace("%%SMB_FOLDER_NAME%%",e.get('SMB_FOLDER_NAME')).replace("%%SMB_COMMENT%%",e.get('SMB_COMMENT')).replace("%%SMB_FOLDER_PATH%%",e.get('SMB_FOLDER_PATH')).replace("%%SMB_FOLDER_AVAIL%%",e.get('SMB_AVAILABLE')).replace("%%SID%%",id)
            else:
                print 42
                m2=loadshareset2()
                print 52
                l2=l2+m2.replace("%%SMB_FOLDER_NAME%%",e.get('SMB_FOLDER_NAME')).replace("%%SMB_COMMENT%%",e.get('SMB_COMMENT')).replace("%%SMB_FOLDER_PATH%%",e.get('SMB_FOLDER_PATH')).replace("%%SMB_FOLDER_AVAIL%%",e.get('SMB_AVAILABLE')).replace("%%SID%%",id)
    print 6
    l1=m1.replace("%%SMB_WORKGROUP%%",d1.get('SMB_WORKGROUP')).replace(" %%SMB_NETBIOS_NAME%%",d1.get('SMB_NETBIOS_NAME')).replace("%%SMB_MAP_TO_GUEST%%",d1.get('SMB_MAP_TO_GUEST'))
    print 7
    l3=l1+l2
    input=open("/etc/samba/smb.conf","w")
    input.write(l3)
    input.close()
    #os.system("mininas_samba_quickfix")

#data={}
#data['SMB_WORKGROUP']="vadfasdf"
#data['SMB_NETBIOS_NAME']="va3eadf"
#data['SMB_MAP_TO_GUEST']="never"
#input = open("/etc/mininas/data/configs/samba.json","w")
#input.write(str(data))
#input.close()
