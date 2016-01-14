import os,uuid

def loadtemplate():
    input = open("/etc/mininas/templates/netatalk/global")
    lines = input.read()
    input.close()
    return lines

def loadshareset():
    input = open("/etc/mininas/templates/netatalk/share")
    lines = input.read()
    input.close()
    return lines

def loadjson():
    input =open("/etc/mininas/data/configs/afp.json")
    lines = input.read()
    input.close()
    if lines:
        return eval(lines)
    return 0

def addtmf(uname,name,size):
    d1=loadjson()
    data={}
    sflist=[]
    if d1 !=0:
        for e in d1.get('share'):
            data2={}
            data2['TM_FOLDER_NAME'] = e.get('TM_FOLDER_NAME')
            data2['TM_FOLDER_PATH'] = e.get('TM_FOLDER_PATH')
            data2['TM_FOLDER_SIZE'] = e.get('TM_FOLDER_SIZE')
            data2['TM_FOLDER_UUID'] = e.get('TM_FOLDER_UUID')
            data2['TM_FOLDER_USER'] = e.get('TM_FOLDER_USER')
            sflist.append(data2)
    data2={}
    fid=str(uuid.uuid1())
    o="/mnt/1/timemachine/%s"%fid
    os.makedirs(o)
    os.system("chmod 0700 %s"%o)
    os.system("chown %s:%s %s"%(uname,uname,o))
    data2['TM_FOLDER_NAME'] = name
    data2['TM_FOLDER_PATH'] = o
    data2['TM_FOLDER_SIZE'] = str(int(size)*1000)
    data2['TM_FOLDER_UUID'] = fid
    data2['TM_FOLDER_USER'] = uname
    sflist.append(data2)
    data['share']=sflist
    input = open("/etc/mininas/data/configs/afp.json","w")
    input.write(str(data))
    input.close()
    makeconf()

def edittmf(name,fid,size):
    d1=loadjson()
    data={}
    sflist=[]
    if d1 !=0:
        for e in d1.get('share'):
            if e.get('TM_FOLDER_UUID')== fid:
                data2={}
                data2['TM_FOLDER_NAME'] = name
                data2['TM_FOLDER_PATH'] = e.get('TM_FOLDER_PATH')
                data2['TM_FOLDER_SIZE'] = str(int(size)*1000)
                data2['TM_FOLDER_UUID'] = e.get('TM_FOLDER_UUID')
                data2['TM_FOLDER_USER'] = e.get('TM_FOLDER_USER')
            else:
                data2={}
                data2['TM_FOLDER_NAME'] = e.get('TM_FOLDER_NAME')
                data2['TM_FOLDER_PATH'] = e.get('TM_FOLDER_PATH')
                data2['TM_FOLDER_SIZE'] = e.get('TM_FOLDER_SIZE')
                data2['TM_FOLDER_UUID'] = e.get('TM_FOLDER_UUID')
                data2['TM_FOLDER_USER'] = e.get('TM_FOLDER_USER')
            sflist.append(data2)
    data['share']=sflist
    input = open("/etc/mininas/data/configs/afp.json","w")
    input.write(str(data))
    input.close()
    makeconf()

def deltmf(fid):
    d1=loadjson()
    data={}
    sflist=[]
    if d1 !=0:
        for e in d1.get('share'):
            if e.get('TM_FOLDER_UUID')== fid:
                continue
            else:
                data2={}
                data2['TM_FOLDER_NAME'] = e.get('TM_FOLDER_NAME')
                data2['TM_FOLDER_PATH'] = e.get('TM_FOLDER_PATH')
                data2['TM_FOLDER_SIZE'] = e.get('TM_FOLDER_SIZE')
                data2['TM_FOLDER_UUID'] = e.get('TM_FOLDER_UUID')
                data2['TM_FOLDER_USER'] = e.get('TM_FOLDER_USER')
                sflist.append(data2)
    data['share']=sflist
    input = open("/etc/mininas/data/configs/afp.json","w")
    input.write(str(data))
    input.close()
    makeconf()

def makeconf():
    m1=loadtemplate()
    m2=loadshareset()
    d1=loadjson()
    l2=""
    if d1 != 0 :
        for e in d1.get('share'):
            l2=l2+m2.replace("%%TM_FOLDER_NAME%%",e.get('TM_FOLDER_NAME')).replace("%%TM_FOLDER_PATH%%",e.get('TM_FOLDER_PATH')).replace("%%TM_FOLDER_SIZE%%",e.get('TM_FOLDER_SIZE'))
    l3=m1+l2
    input=open("/usr/local/etc/afp.conf","w")
    input.write(l3)
    input.close()
