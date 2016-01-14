#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.template import loader,Context
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect,requires_csrf_token,csrf_exempt
from django import forms
from models import BtFileinfo_down,User,Fileinfo_up,Fileinfo_down,Ntpinfo,Group,Usergroup,Syssetting,Zfsinfo,Diskinfo,Zpoolinfo,Sharefuser,Addressbook,Tokenbackup,Tmpfileinfo
import os,json,re,sys,shutil,datetime,atexit,time,pexpect,urllib2
from threading import Timer
import psutil,struct,ntplib,re,platform,random,gc
from aaa import settings
from django.utils import timezone
import main_down,socket,diskctl
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.db import connection
from PIL import Image
import eyed3,chardet
from aaa.settings import FILE_SAVE_PATH
import hashlib,string,sambactl,ftpctl,tmctl

from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from constant import getMessage as get_message ,IMAGE,MUSIC,VIDEO,getQuestions
global FILE_SAVE_PATH

root_path = "/mnt/"
if 'Windows' in platform.system():
    FILE_SAVE_PATH= "d:/upload/"
    root_path = FILE_SAVE_PATH
else:
    urp=Syssetting.objects.get(id=1)
    FILE_SAVE_PATH=str(urp.uploadrootpath)
    root_path = "/mnt/"




### shihl  ###
upload_dir = {
    1:"photo",
    2:"video",
    3:"music",
    4:"download",
    5:"sync",
    6:"addbook",
    "1":"photo",
    "2":"video",
    "3":"music",
    "4":"download",
    "5":"sync",
    "6":"addbook",

}

down_type = {
    0:u"其它",
    1:u"下载完成",
    2:u"下载中",
    3:u"暂停",
    None:"",
    "":"",
    "null":"",
}

system_path = ("photo","music","video","sync","download","btdownload","btdownload/bt",u"photo/来自iOS",u"photo/来自Android",u"photo/qq",u"video/来自iOS",u"video/来自Android",u"video/qq",u"music/来自iOS",u"music/来自Android",u"music/qq")

system_user =["daemon","bin","sys","sync","games","man","lp","mail","news","uucp","proxy","www-data","backup","list","irc","gnats","nobody","systemd-timesync","systemd-network","systemd-resolve","systemd-bus-proxy","Debian-exim","messagebus","statd","sshd","mysql","proftpd","ftp","dnsmasq","admin","thunder","root"]

tmp_system = False

class UserForm(forms.Form):
	UserName = forms.CharField(label='UserName',max_length=100,widget=forms.TextInput(attrs={'class':"inp"}))
	Password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':"inp"}))

# devicetype (1:ios-pad,2:ios,3:Android-pad,4:Android,5:web端)
# deviceid 设备序列号
# Create your views here.
#@csrf_protect
#def index(request):
#	return render_to_response('Default/Account/Login.html',context_instance=RequestContext(request))
@csrf_exempt
def index(req):
    postType = req.POST.get("devicetype","5")
#	print postType=="5"
    if postType=="5":
        if req.method == 'POST':
            uf = UserForm(req.POST)
            if uf.is_valid():
                UserName = uf.cleaned_data['UserName']
                Password = uf.cleaned_data['Password']
                #print "UserName :",UserName
                #print "Password :",Password
                user = User.objects.filter(UserName=UserName,Password=Password)
                if user:
                    user = user[0]
                    user.login = 1
                    user.save()
                    rs = '100100000'
                    if not isSetQuestion() and user.UserName == u"admin":
                        rs = '100102248'
                    data = {'returncode':rs,'message':get_message(rs)}
                    response = HttpResponse(json.dumps(data),content_type="application/json")
                    response.set_cookie('UserName',UserName,3600*24)#5)#
                    response.set_cookie('realname',user.realname,3600*24)#5)#
                    return response
            data = {'returncode':'100100100','message':get_message('100100100')}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            uf = UserForm()
        return render_to_response('Default/Account/Login.html',{'uf':uf},context_instance=RequestContext(req))
    elif postType=="4":
        uname = req.POST.get("username",req.GET.get("username",0))
        upwd = req.POST.get("password",req.GET.get("password",0))
        id = req.POST.get("deviceid",req.GET.get("deviceid",0))
        u=User.objects.filter(deviceid=id)
        if u:
            u=u[0]
            if not isSetQuestion() and u.UserName == u"admin":
                rs = '100102248'
                data = {'returncode':rs,'message':get_message(rs)}
                return HttpResponse(json.dumps(data),content_type="application/json")
            p=os.popen("cat /run/mininas/system/product_serial_no").read()
            data = {'returncode':'100100000','data':{'username':u.UserName,'sn':p}}
            return HttpResponse(json.dumps(data),content_type="application/json")
        user = User.objects.filter(UserName=uname,Password=upwd)
        if user:
            try:
                user = user[0]
                user.deviceid=id
                user.save()
                if not isSetQuestion() and user.UserName == u"admin":
                    rs = '100102248'
                    data = {'returncode':rs,'message':get_message(rs)}
                    return HttpResponse(json.dumps(data),content_type="application/json")
                p=os.popen("cat /run/mininas/system/product_serial_no").read()
                data = {'returncode':'100100000','data':{'username':u.UserName,'sn':p}}
                return HttpResponse(json.dumps(data),content_type="application/json")
            except Exception,e:
                print 'EEEEE :',e
                pass
        data = {'returncode':'100100100','data':{'username':uname}}
        return HttpResponse(json.dumps(data),content_type="application/json")
    elif postType=="2":
        uname = req.POST.get("username",req.GET.get("username",0))
        upwd = req.POST.get("password",req.GET.get("password",0))
        id = req.POST.get("deviceid",req.GET.get("deviceid",0))
        if id !='':
            u=User.objects.filter(deviceid=id)
            if u:
                u=u[0]
                if not isSetQuestion() and u.UserName == u"admin":
                    rs = '100102248'
                    data = {'returncode':rs,'message':get_message(rs)}
                    return HttpResponse(json.dumps(data),content_type="application/json")
                p=os.popen("cat /run/mininas/system/product_serial_no").read()
                data = {'returncode':'100100000','data':{'username':u.UserName,'sn':p}}
                return HttpResponse(json.dumps(data),content_type="application/json")
        user = User.objects.filter(UserName=uname,Password=upwd)
        if user:
            try:
#                o=random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',15)
#                w=""
#                for i in o:
#                    w=w+i
                user = user[0]
                user.deviceid=tmp_random()
                user.save()
#                print user.deviceid
                if not isSetQuestion() and user.UserName == u"admin":
                    rs = '100102248'
                    data = {'returncode':rs,'message':get_message(rs)}
                    return HttpResponse(json.dumps(data),content_type="application/json")
                p=os.popen("cat /run/mininas/system/product_serial_no").read()
                data = {'returncode':'100100000','data':{'username':user.UserName,'deviceid':user.deviceid,'sn':p}}
                return HttpResponse(json.dumps(data),content_type="application/json")
            except Exception,e:
                print 'EEEEE :',e
                pass
        data = {'returncode':'100100100','data':{'username':uname}}
        return HttpResponse(json.dumps(data),content_type="application/json")

def tmp_random():
    deviceids =[u.deviceid for u in User.objects.filter()]
    o = tmp_get(deviceids)
    return o
    
def tmp_get(deviceids):
    o=random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',15)
    o = ''.join(o)
    if o in deviceids:
        o = tmp_get(deviceids)
    tokens =[u.token for u in Tokenbackup.objects.filter()]
    if o in tokens:
        o = tmp_get(deviceids)
    return o

@csrf_exempt
def home(req):
    return check_user(req,"Default/Home/Index.html",arg={1:1})
    #name,realname = getusername(req),getrealname(req)
    #return render_to_response("Default/Home/Index.html",{'realname':realname,'UserName':name},context_instance=RequestContext(req))

#response = HttpResponse(json.dumps(data),content_type="application/json")
#response.set_cookie('UserName',UserName,3600*24)#5)#


# 退出登录  
@csrf_exempt
def logout(request):
    rs = "100100000"
    try:
        deviceid = request.POST.get("deviceid","")
        username = request.POST.get("username",getusername(request))
        postType = request.POST.get("devicetype","5")
        #print "username :",username
        user = User.objects.filter()
        try:
            
            if postType!="5":
                user = user.filter(deviceid = deviceid)
                if user:
                    user = user[0]
                    user.deviceid = ""
                    user.save()
            elif postType=="5":
                user = user.filter(UserName = username)
                if user:
                    print 'log out ...'
                    user = user[0]
                    user.login = 0
                    user.save()
        except Exception,e:
            print 'out login...',e
            rs = "100102235"
        data = {'returncode':rs,'message':get_message(rs)}
        response = HttpResponse(json.dumps(data),content_type="application/json")
        response.set_cookie('UserName',"",1)
        response.set_cookie('logout',1,24*3600)
        return response#HttpResponse(json.dumps(data),content_type="application/json")
    except Exception,e:
        print e
    data = {'returncode':rs,'data':{},'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getselfacls(req):
    name = req.POST.get("username")
    u=User.objects.filter(UserName=name)
    data={}
    if u:
        data['data'] = u[0].acls
    data['returncode']=100100100
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def foldersearch(req):
    keyword = req.POST.get("keyword")
    sort = req.POST.get("sortBy")
    type = req.POST.get("devicetype")
    id = req.POST.get("deviceid")
    path = req.POST.get("filePath")
    flist=[]
    if type=="4":
        dlist=getfolderlist(path)
        for d in dlist:
            s=d.find(keyword)
            if s != -1:
                flist.append(d)
    data['data']=flist
    data['returncode']='100100100'
    return HttpResponse(json.dumps(data),content_type="application/json")

# 密保相关

# 设置密保问题
@csrf_exempt
def setQuestion(request):
    rs = "100102250"
    user = getusername(request)
    #print '=====>',user
    if user != "admin":
        rs = "100102250"
        data = {'returncode':rs,'message':get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    u = User.objects.get(UserName = user)
    q1 = request.POST.get('q1',None)
    q2 = request.POST.get('q2',None)
    q3 = request.POST.get('q3',None)
    #print q1,q2,q3
    if q1 and q2 and q3:
        u.q1 = q1
        u.q2 = q2
        u.q3 = q3
        u.t = int(time.time())
        s = random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',20)
        u.key_code = ''.join(s)
        try:
            u.save()
            #print 'sssssssssssssss'
        except Exception,e:
            #print "EEEEE :",e
            rs = "100102251"
            data = {'returncode':rs,'message':get_message(rs)}
            return HttpResponse(json.dumps(data),content_type="application/json")
        data = {}
        data2 = {}
        data2['q1'] = u.q1.split('_')[0]
        data2['q2'] = u.q2.split('_')[0]
        data2['q3'] = u.q3.split('_')[0]
        data['returncode'] = "100100000"
        data['code'] = u.key_code
        data['data'] = data2
        #print 'DDDDDDDDD:',data
    
    return HttpResponse(json.dumps(data),content_type="application/json")
   
# 获取密保问题 #getQuestions
@csrf_exempt
def getQuestion(request):
    u = User.objects.get(UserName = "admin")
    if not (u.q1 and u.q2 and u.q3):
        rs = "100102248"
        data = {'returncode':rs,'message':get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data,data2 = {},{}
    data2['q1'] = "%s_%s" %(u.q1.split('_')[0],u.q1.split('_')[2])
    data2['q2'] = "%s_%s" %(u.q2.split('_')[0],u.q2.split('_')[2])
    data2['q3'] = "%s_%s" %(u.q3.split('_')[0],u.q3.split('_')[2])
    data['returncode'] = "100100000"
    data['data'] = data2
    #print "DDDDDDDDDD :",data
    return HttpResponse(json.dumps(data),content_type="application/json")

# 验证密保答案
@csrf_exempt
def check_answer(request):
    rs = "100102249"
    data = {'returncode':rs,'message':get_message(rs)}
    
    u = User.objects.get(UserName = "admin")
    q1 = request.POST.get("q1",None)
    q2 = request.POST.get("q2",None)
    q3 = request.POST.get("q3",None)
    if u.q1.split('_')[1]==q1 and u.q2.split('_')[1]==q2 and u.q3.split('_')[1]==q3:
        rs = "100100000"
        try:
            
            t = int(time.time())
            s = random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',20)
            u.t = t
            u.key_code = ''.join(s)
            #print 'KKKKKKKKK :',u.key_code
            u.save()
        except:pass
        data = {'returncode':rs,'message':get_message(rs),'code':u.key_code}
    return HttpResponse(json.dumps(data),content_type="application/json")

#重置密码
@csrf_exempt
def reSetPwd(request):
    rs = "100102252"
    #now_uname  改的用户名
    #newpwd       新的密码
    kcode = request.POST.get("code",None)
    newpwd = request.POST.get("newpwd",None)
    #print 'kcode :',kcode
    u = User.objects.filter(UserName="admin",key_code=kcode)
    #print '=====>',u
    if u:
        u = u[0]
        tt = u.t
        now_t = time.time()
        if int(now_t-tt)>180:
            rs = "100102253"
            data = {'returncode':rs,'message':get_message(rs)}
            return HttpResponse(json.dumps(data),content_type="application/json")
        if u and newpwd:
            u.Password = newpwd
            #print 'PPPPPPPPPP :',u.Password,u.UserName
            try:
                u.save()
                rs = "100100000"
            except:pass
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

#重置普通用户密码
@csrf_exempt
def reSetPwdUser(request):
    rs = "100102250" #"100102252" #
    uname = request.POST.get("uname",None)
    newpwd = request.POST.get("newpwd",None)
    admin_pwd = request.POST.get("admin_pwd",None)
    if uname and newpwd and admin_pwd:
        
        admin = User.objects.filter(UserName="admin",Password=admin_pwd)
        if not admin:
            rs = "100102252"
        else:
            users = User.objects.filter(UserName=uname)
            if not users:
                rs = "100100102"
            else:
                try:
                    u = users[0]
                    u.Password = newpwd
                    u.save()
                    rs = "100100000"
                except:pass
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")    

#修改密码
@csrf_exempt
def changepwd(request):
    postType = request.POST.get("devicetype",request.GET.get("devicetype","5"))
    
    username = request.POST.get('uname',getusername(request))
    password = request.POST.get('oldpwd','')
    new_password = request.POST.get('newpwd','')
    data = {}
    rs = u"100102241"
    ch=2
    
    try:
        message = ""
        user = User.objects.filter(UserName = username,Password = password)
        os.system("service samba start")
        #up = pexpect.spawn('passwd %s' %(username.decode("utf8")))
        #up.expect('New')
        #up.sendline(new_password)
        #up.expect('Retype')
        #up.sendline(new_password)
        #ch=up.expect(["Bad","passwd"])
        #up.expect
        #up.interact()
        #sba = pexpect.spawn('smbpasswd -a %s' %(username.decode("utf8")))
        #sba.expect('New')
        #sba.sendline(new_password)
        #sba.expect('Retype')
        #sba.sendline(new_password)
        #sba.interact()
        o="/usr/local/sbin/operate_without_expect 3 %s %s 0"%(username.decode("utf8"),new_password)
        result=os.system(o)
        print result
        ww  = Syssetting.objects.get(id=1)
        if ww.samba == "0":
            os.system("service samba stop")
        if user:
            user = user[0]
            user.Password = new_password
            user.save()
            rs = "100100000"
        else:
            rs = "100102242"
    except Exception,e:
        print 'eeeeeeee :',e
        rs = "100102242"
    
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data))

#   编辑用户
@csrf_exempt
def edituser(request):
	username = request.POST.get("username","")
	realname = request.POST.get("realname","")
	email = request.POST.get("email","")
	u = User.objects.filter(UserName=username)
	rs = "100100104"
	if u:
		u = u[0]
		if realname:
			u.realname = realname
		if email:
			u.email = email
		try:
			u.save()
			rs = "100100000"
			os.system
		except Exception,e:
			print e
	data = {'returncode':rs}
	return HttpResponse(json.dumps(data))

@csrf_exempt
def syncaddbook(request):
    friends = request.POST.get("strJson","")
    name = request.POST.get("username","")
    dname = request.POST.get("devicename","")
    id = request.POST.get("deviceid","")
    o="%s%s/sync/addbook"%(FILE_SAVE_PATH,name)
    input =open(o)
    #print o
    hs = input.readlines()
    input.close()
    input =open(o,"w")
    data={}
    ws=""
    for e in hs:
        ws=ws+e
    ISOTIMEFORMAT='%Y-%m-%d %X'
    ws=ws+"%s&^&%s&^&%s&^&%s\n"%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())),dname,id,friends)
    input.write(ws)
    input.close
    #id = request.POST.get("deviceid","")
    #fs =friends.split("/")
    #s=Addressbook.objects.filter(deviceid=id)
    #if s:
        #for ss in s:
            #s.delete()
    #for f in fs:
        #sp=f.split(",")
        #pt=Addressbook()
        #pt.deviceid=id
        #pt.friendname=sp[0].decode("utf8")
        #pt.email=sp[1]
        #pt.phonenumber=sp[2]
        #pt.shihongliang=sp[3]
        #try:
            #pt.save()
        #except Exception,e:
            #print 'eeeeeeee :',e
    
    data = {'returncode':'100100000'}
    return HttpResponse(json.dumps(data))

@csrf_exempt
def getaddbook(request):
    sdata = request.POST.get("time","")
    name = request.POST.get("name","")
    #print 'name :',name
    o="%s%s/sync/addbook"%(FILE_SAVE_PATH,name)
    input =open(o)
    hs = input.readlines()
    input.close()
    data={}
    for e in hs:
        if sdata in e:
            s=e.split("&^&")
            t=s[3].split("\n")
            data['data']=t[0]
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data))

@csrf_exempt
def deladdbook(request):
    sdata = request.POST.get("time","")
    name = request.POST.get("name","")
    o="%s%s/sync/addbook"%(FILE_SAVE_PATH,name)
    input =open(o)
    hs = input.readlines()
    input.close()
    input =open(o,"w")
    data={}
    ws=""
    for e in hs:
        if sdata in e:
            continue
        ws=ws+e
    input.write(ws)
    input.close()
    data['returncode']='100100000'
    data['shaoqiwei']="fuck you"
    return HttpResponse(json.dumps(data))

@csrf_exempt
def getbackuplist(request):
    name = request.POST.get("name","")
    o="%s%s/sync/addbook"%(FILE_SAVE_PATH,name)
    input =open(o)
    hs = input.readlines()
    input.close()
    data={}
    tlist=[]
    for e in hs:
        data2={}
        s=e.split("&^&")
        data2['time']=s[0]
        data2['devicename']=s[1]
        tlist.append(data2)
    data['data']=tlist
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data))

#@csrf_exempt
#def syncdata(request):
#    rs = u"100102228"
#    user_name = getusername(request)
#    
##    print "user_name :",user_name
#    user = User.objects.filter(UserName = user_name)
#    if not user:
##        print 'uuuuuuuuuuuuuu'
#        return HttpResponse(rs)
#    else:
#        user = user[0]
#    
#    t = request.POST.get("type",'')
#    
#    if t:
#        try:
#            t = int(t)
#        except Exception,e:
#            print 'FFFFFFFFF :',e
#            pass
#    
#    act = request.POST.get("act",None)
#    obj = request.FILES.get("file",None)
##    if not obj:
##        data = {"returncode":rs,"message":get_message(rs)}
##        return HttpResponse(json.dumps(data),content_type="application/json")
#    
#    dir_type = upload_dir.get(t)  # 获取文件该放到那个种类中
#    
#    if dir_type:
#        p = '%s%s/%s/' % (FILE_SAVE_PATH,user_name,dir_type)
#    else:
#        p = '%s%s/' % (FILE_SAVE_PATH,user_name)
#        
#    if act and act !="/":
#        p = '%s%s' % (FILE_SAVE_PATH,act)
#    fileName = request.POST.get("name")
#    file_path = '%s%s' %(p,fileName)
##    print file_path
#    file_name,ftype=os.path.splitext(fileName)
#    fu = Fileinfo_up.objects.filter(path=act,name=file_name,ftype=ftype)
#    if fu:
#        data = {"returncode":rs,"message":get_message(rs)}
#        return HttpResponse(json.dumps(data),content_type="application/json")    
#    try:
#        #POST:<QueryDict: {u'chunks': [u'2'], u'chunk': [u'0'], u'type': [u'2'], u'name': [u'ssss.avi'], u'act':[u'admin/video/\u6211\u7684\u89c6\u9
#        chunk_count = request.POST.get("chunks",0)
#        chunknum = request.POST.get("chunk",0)
#        postType = request.POST.get("devicetype","5")
##        print "postType :",postType
#        if postType=="4":
#            if chunk_count:
#                chunk_count = int(chunk_count)
#            if chunknum:
#                chunknum = int(chunknum)
#        elif postType=="5":
#            if chunk_count:
#                chunk_count = int(chunk_count)
#            if chunknum:
#                chunknum = int(chunknum)
##        print 'chunk_count :',chunk_count,'-->',chunknum
#        path = "%s%s"%(p,fileName)
#        tfi=Tmpfileinfo.objects.filter(path=path)
#        if tfi:
#            if chunk_count> chunknum+1 and chunknum<=tfi[0].count:
#                data = {"returncode":rs,"message":get_message(rs)}
#                return HttpResponse(json.dumps(data),content_type="application/json")
#            elif chunk_count>chunknum+1 and chunknum > tfi[0].count:
#                tmpf = open(path,"ab")
#                for chunk in obj.chunks():
#                    tmpf.write(chunk)
#                tmpf.close()
#                tfi[0].count = chunknum
#                tfi[0].save()
#                data = {"returncode":rs,"message":get_message(rs)}
#                return HttpResponse(json.dumps(data),content_type="application/json")
#            elif chunk_count==chunknum+1:
#                tmpf = open(path,"ab")
#                for chunk in obj.chunks():
#                    tmpf.write(chunk)
#                tmpf.close()
#                tfi[0].delete()
#        elif not tfi and chunk_count>1:
#            tmpf = open(path,"ab")
#            for chunk in obj.chunks():
#                tmpf.write(chunk)
#            tmpf.close()
#            ntfi = Tmpfileinfo()
#            ntfi.path = path
#            ntfi.count = 0
#            ntfi.save()
#            data = {"returncode":rs,"message":get_message(rs)}
#            return HttpResponse(json.dumps(data),content_type="application/json")
#        else :
#            tmpf = open(path,"ab")
#            for chunk in obj.chunks():
#                tmpf.write(chunk)
#            tmpf.close()
#        file_name,ftype=os.path.splitext(fileName) # 获取文件名 和 后缀
#        fu = Fileinfo_up()
#        fu.userid = user
#        fu.name = file_name 
#        
#        if act:
#            fu.path = "%s" %(act)
#        else:
#            fu.path = "%s/%s/" %(user_name,dir_type)
##        print fu.path
##        print file_path
#        fu.size = os.path.getsize(file_path)#fSize(file_path)
#        fu.type = t
#        fu.ftype = ftype
#        fu.owner = user_name
#        fu.lastwritetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        fu.uploadstarttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        fu.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        fu.uploadtotaltime = 1
#        fu.status = 1
#        fu.filestatus = 0
#        
#        if t==3:
#            try:
#                import eyed3
#                f = eyed3.load(file_path)
#                fu.singer = f.tag.artist#.encode('utf8')
#                fu.ablum = f.tag.album
#                if f.tag:
#                    if f.tag.genre:
#                        fu.style = f.tag.genre.name
#                fu.age = f.tag.recording_date
#                fu.duration = fTime(f.info.time_secs)
#            except Exception,e:
#                print 'Music ：',e
#                pass
#        if t==1:
#            try:
#                from PIL import Image
#                img = Image.open(file_path)
#                path_im = "%sim/" %(p)
#                if not os.path.exists(path_im):
#                    if 'Windows' in platform.system():
#                        os.makedirs(path_im)
#                    else:
#                        #mf=path_im.split("/mnt/")
#                        #o="zfs create %s"%(mf[1])
#                        #i="zfs set mountpoint=%s %s"%(path_im,mf[1])
#                        #os.system(o)
#                        #os.system(i)
#                        os.makedirs(path_im)
#                fp = "%s%s1%s" %(path_im,fu.name,fu.ftype)
#                #print fp,type(fp)
#                img.thumbnail((200,200),Image.ANTIALIAS)
#                img.save(fp.decode("utf8"))#)
#                fp = "%s%s2%s" %(path_im,fu.name,fu.ftype)
#                #print fp,type(fp)
#                img.thumbnail((80,80),Image.ANTIALIAS)
#                img.save(fp.decode("utf8"))#)
#            except Exception,e:
#                print "UP Photo :",e
#        
#        try: 
#            fu.save()
#            rs = "100100000"
#        except Exception,e:# 处理保存失败
#            print "UP :",e
#        
#        data = {"returncode":rs,"message":get_message(rs)}
#        return HttpResponse(json.dumps(data),content_type="application/json")
#    except Exception,e:
#        print "EEEEEEEEE",e
##	return 'sss'
#    
#    data = {"returncode":rs,"message":get_message(rs)}
#    return HttpResponse(json.dumps(data),content_type="application/json")

#   删除用户
@csrf_exempt
def deluser(request):
    username = request.POST.get("username","")
    u = User.objects.filter(UserName = username)
    rs = "100100104"
    if u:
        if u[0].UserName == "admin":
            data = {'returncode':"200100002",'message':get_message("200100002")}
            return HttpResponse(json.dumps(data),content_type="application/json")
        try:
            u=u[0]
            ugs = Usergroup.objects.filter(username=u.UserName)
            for ug in ugs:
                if ug.UserName == "admin":
                    continue
                ug.delete()
            pp = FILE_SAVE_PATH+u.UserName
            os.chdir(FILE_SAVE_PATH)
            if os.path.exists(pp):
                shutil.rmtree(pp)
            u.delete()
            rs = "100100000"
        except Exception,e:
            os.chdir(root_path)
            print e
        os.system("service samba start")
        up = "mininas_user_delete %s"%(username.decode("utf8"))
        os.system(up)
        ww  = Syssetting.objects.get(id=1)
        if ww.samba == 0:
            os.system("service samba stop")
        p = FILE_SAVE_PATH+username
        o="rm -rf %s"%(p)
        os.system(o)
        us = Sharefuser.objects.filter(username=username)
        for u in us:
            u.delete()
    input =open("/etc/proftpd/proftpd.conf")
    lines= input.readlines()
    input.close()
    o="Directory %s"%p
    i=0
    ws=""
    for l in lines:
        if i>0 and i<=4:
            i=i+1
            continue
        if o in l:
            i=i+1
            continue
        ws=ws+l
    input =open("/etc/proftpd/proftpd.conf","w")
    input.write(ws)
    input.close()
    os.chdir(root_path)
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

##       Photo
@csrf_exempt
def photo(req):
    #name,realname = getusername(req),getrealname(req)
    #return render_to_response("Default/Photo/Index.html",{'realname':realname,'UserName':name},context_instance=RequestContext(req))
    return check_user(req,"Default/Photo/Index.html",arg={1:1})

@csrf_exempt
def pplayer(req):
    return check_user(req,"Default/Photo/Player.html",arg={1:1})

@csrf_exempt
def photou(req):
    return check_user(req,"Default/Photo/UploadFile.html",arg={1:1})
#    name=getusername(req)
#    return render_to_response("Default/Photo/UploadFile.html",context_instance=RequestContext(req))

# 新增文件夹
@csrf_exempt
def photoa(req):
    rs = '100100211'
    if req.method == 'POST':
        name=req.REQUEST.get('name',None)
        print name
        if name:
            n=name.split("/")
#            if n[0] == "admin":
#                data = {'returncode':rs,'message':get_message(rs)}
#                return HttpResponse(json.dumps(data),content_type="application/json")
            try: #100102230
                print FILE_SAVE_PATH
                p = (u"%s%s" %(FILE_SAVE_PATH,name)).decode("utf8")
                print p
                if os.path.exists(p):
                    rs = '100102230'
                else:
                    os.makedirs(p)
                    os.system("chown %s:%s %s"%(n[0],n[0],p))
                    os.system("chmod 755 %s"%p)
                    rs = '100100000'
            except Exception,e:
                print 'PPP :',e
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

# 删除文件夹
@csrf_exempt
def photod(req):
    if req.method == 'POST':
        name=req.REQUEST.get('name',None)
        deviceid=req.REQUEST.get('deviceid',None)
        print 'name ------->',name
        user=getusername(req)
        if user:
            print user
            n=name.split("/",1)
            if n[0]!=user:
                print 1
                data = {'returncode':'100100214','message':get_message('100100214')}
                return HttpResponse(json.dumps(data),content_type="application/json")
            print 2
            for e in system_path:
                print 3
                if e+"/" == n[1] or e == n[1]:
                    print 4
                    data = {'returncode':'100100214','message':get_message('100100214')}
                    return HttpResponse(json.dumps(data),content_type="application/json")
            print 5
            if name:
                try:
                    print 6
                    os.chdir(FILE_SAVE_PATH)
                    print '========>',FILE_SAVE_PATH+name
                    shutil.rmtree((FILE_SAVE_PATH+name))
                    data = {'returncode':'100100000','message':get_message()}
                    fus = Fileinfo_up.objects.filter(path__contains=name)
                    print 7
                    for fu in fus:
                        try:
                            print 8
                            fus.delete()
                        except Exception,e:
                            print e
                    print 9
                    return HttpResponse(json.dumps(data),content_type="application/json")
                except Exception,e:
                    print 10
                    os.chdir(root_path)
                    print 'DDDDD :',e
    print 11
    os.chdir(root_path)
    data = {'returncode':'100100214','message':get_message('100100214')}
    return HttpResponse(json.dumps(data),content_type="application/json")

# 文件夹重命名
@csrf_exempt
def photor(req):
    rs = "100100215"
    if req.method == 'POST':
        oname=u"%s" %(req.REQUEST.get('oldName',None))
        nname=u"%s" %(req.REQUEST.get('newName',None))
        #print oname,nname
        if oname and nname:
            try:
                os.chdir(FILE_SAVE_PATH)
                newfilename = "/".join(oname.split("/")[0:-2])+"/"+nname
                old_p = FILE_SAVE_PATH+oname
                #print 'ooo :',old_p,type(old_p)
                new_p = FILE_SAVE_PATH+newfilename   #100102236
                
                if os.path.exists(new_p):
                    rs = '100102230'
                    data = {'returncode':rs,'message':get_message(rs)}
                    return HttpResponse(json.dumps(data),content_type="application/json")
                else:
                    #print 'nnnnnnn :',new_p,type(new_p)
                    #print '------->',old_p
                    os.renames(old_p.decode('utf8'),new_p.decode('utf8'))
                
                #print 'ssssssssssssss'
                fs = Fileinfo_up.objects.filter(path__contains=oname)
                #print 'fs :',fs
                
                for f in fs:
                    #print 'newfilename :',newfilename,'--->',f.path,str(f.path)
                    f.path = str(f.path).replace(oname,newfilename+"/")
                    f.save()
                rs = "100100000"
            except Exception,e:
                os.chdir(root_path)
                print 'EEEEE :',e
                pass
    os.chdir(root_path)
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

# 迅雷文件夹重命名
@csrf_exempt
def thunderdrename(req):
    rs = "100100215"
    if req.method == 'POST':
        oname="%s%s"%(FILE_SAVE_PATH,req.REQUEST.get('oldName',None))
        nname="%s%s"%(FILE_SAVE_PATH,req.REQUEST.get('newName',None))
        os.chdir(FILE_SAVE_PATH)
        os.rename(oname.decode('utf8'),nname.decode('utf8'))
        rs = "100100000"
    
    os.chdir(root_path)
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

# 删除迅雷文件
@csrf_exempt
def thunderddel(request):
    #print 'going....'
    rs = "100102227"
    fs = request.POST.get("fpath","")
    for f in fs.split(','):
        fpath = "%s%s" %(FILE_SAVE_PATH,f)
        isfile = os.path.isfile(fpath)
        #print isfile,fpath
        if isfile:
            try:
                #shutil.rmtree(fpath.decode("utf8"))
                os.remove(fpath.decode("utf8"))
                rs = "100100000"
            except:
                pass
    
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

# 文件移动
@csrf_exempt
def photom(request):
    rs = "100102222"
    npath = request.POST.get("npath","")
    fids = request.POST.get("fids","")
    opath = request.POST.get("opath","")
    move = request.POST.get("option","")
    #print "npath :[",npath,"]"
    #print "fids :[",fids,"]"
    #print "opath :[",opath,"]"
    if fids and npath and move=="":
        fids = [int(i) for i in fids.split(",")]
        #print "fids :",fids
        for fid in fids:
            upfile = Fileinfo_up.objects.filter(id = fid)
            #print "upfile :",upfile
            if upfile:
                f = upfile[0]
                if f.path == npath: #跳过相同目录移动
                    continue
                old_path = "%s%s%s" %(f.path,f.name,f.ftype)
                old_path_im = "%sim/%s2%s" %(f.path,f.name,f.ftype)
                old_path_im1 = "%sim/%s1%s" %(f.path,f.name,f.ftype)
                #print "old_path :",old_path
                print 6
                if f.ftype.upper() in IMAGE:
                    picOption(f)
                print 6
                f.path = npath
                try:
                    os.chdir(FILE_SAVE_PATH)
                    new_path = FILE_SAVE_PATH+npath
                    disk_file_path = FILE_SAVE_PATH+old_path
                    #print 'new_path :',new_path
                    #hasfile = os.path.join(new_path,f.name+f.ftype)
                    print 66
                    if os.path.isfile(new_path+f.name+f.ftype):
                        #shutil.rmtree(disk_file_path)
                        os.remove(disk_file_path.decode("utf8"))
                    else:
                        #print 'nnnnnnnnnnnnnn',disk_file_path,'nnnnnnnnnnn',new_path
                        if not os.path.isfile(disk_file_path):
                            f.delete()
                        else:
                            shutil.move(disk_file_path,new_path)
                    print 77
                    try:
                        
                        if f.ftype.upper() in IMAGE:
                            path_im = "%s%s" %(FILE_SAVE_PATH,old_path_im)
                            path_im1 = "%s%s" %(FILE_SAVE_PATH,old_path_im1)
                            #if os.path.isfile(path_im):
                            #print 'AB'*10
                            path_im_new = new_path+"im/"
                            if not os.path.exists(path_im_new):
                                #print 'CD'*10
                                #mf=path_im_new.split("/mnt/")
                                #o="zfs create %s"%(mf[1].decode("utf8"))
                                #i="zfs set mountpoint=%s %s"%(path_im_new,mf[1].decode("utf8"))
                                #os.system(o)
                                #os.system(i)
                                os.makedirs(path_im_new)
                            if os.path.isfile(path_im):
                                shutil.move(path_im,path_im_new)
                            if os.path.isfile(path_im1):
                                shutil.move(path_im1,path_im_new)
                        elif f.ftype.upper() in MUSIC:
                            f = muicOption(f)
                        print 88
                    except Exception,e:
                        os.chdir(root_path)
                        print e
                    f.save()
                    ff = Fileinfo_up.objects.filter(name=f.name,path=npath)
                    if len(ff)>1:
                        ff[0].delete()
                    rs = "100100000"
                    print 99
                except Exception,e:
                    os.chdir(root_path)
                    print 'MMMMMM :',e
                    data = {'returncode':rs,'message':e}
                    return HttpResponse(json.dumps(data),content_type="application/json")
    elif move == "xl":
        # 判断迅雷
        if opath and npath:
            fu = Fileinfo_up()
            try:
                os.chdir(FILE_SAVE_PATH)
                tt = opath.split('/')
                p = '/'.join(tt[0:-1])
                fname,ftype = os.path.splitext(tt[-1])
                file_path = "%s%s" %("",opath)
                fu.name = fname
                fu.ftype = ftype
                fu.path = npath
                fu.uploadstarttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fu.size = os.path.getsize(file_path)
                new_path = "%s%s" %(FILE_SAVE_PATH,npath)
                #print 'new_path ------>',new_path
                newfile = (new_path+fu.name+fu.ftype).decode("utf8")
                oldfile = ("%s%s"%(FILE_SAVE_PATH,opath)).decode("utf8")
                #print "isfile ====>",os.path.isfile(newfile)
                if os.path.isfile(newfile):
                    #print 'a'*10
                    os.remove(oldfile.decode("utf8"))
                    #print 'b'*10
                else:
                    #print 'nnnnnnnnnnnnnn',oldfile,'nnnnnnnnnnn',new_path
                    shutil.move(oldfile,new_path)
                #shutil.move(disk_file_path,new_path)
                #print 'TTTTTTT :',ftype
                if ftype.upper() in IMAGE:
                    fu = picOption(fu)
                    fu.type = 1
                elif ftype.upper() in MUSIC:
                    fu = muicOption(fu)
                    fu.type = 3
                elif ftype.upper() in VIDEO:
                    fu.type = 2
                else:
                    fu.type = 0
                fu.status = 1
                fu.owner = "admin"
                fu.userid = User.objects.get(UserName="admin")
                #print 'do save..'
                fu.save()
                rs = "100100000"
                os.chdir(root_path)
            except Exception,e:
                print 'XXXXXXXXXXXXXXX :',e
    elif move == "bt":
        pass
    else:
        data = {'returncode':"100102222",'message':get_message("100102222")}
        return HttpResponse(json.dumps(data),content_type="application/json")
    os.chdir(root_path)
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")


# 文件夹移动
@csrf_exempt
def photofo(request):
    rs = "100102223"
    opath = request.POST.get("opath","")
    npath = request.POST.get("npath","")
    if opath and npath:
        opath = opath.strip()
        npath = npath.strip()
        #print "opath :",opath
        #print "npath :",npath
        ufs = Fileinfo_up.objects.filter(path__contains=opath)
        if ufs:
            for f in ufs:
                # 存在数据库中的路径
                db_path = "%s"%f.path
                #print 'db_path :',type(db_path),db_path
                try:
                    oname = opath.split("/")[-2]
                    # 子目录
                    #new_path = db_path.replace(opath,npath)
                    child_dir = db_path.split(opath)
#                    print 'ccccccccccc :',child_dir
                    if child_dir[-1]!=u"":
                        child_dir = child_dir[-1]
                    else:
                       child_dir = ""
                    #print "new_path :",npath#,'child :', child_dir
                    new_path = "%s%s/%s" %(npath,oname,child_dir)
#                    print "----->new_path :",new_path
                    f.path = new_path
                    f.save()
                except Exception,e:
                    print "replace folder :",e
        
        try:
            os.chdir(FILE_SAVE_PATH)
            o = FILE_SAVE_PATH+opath
            n = FILE_SAVE_PATH+npath#[:-1]
            
            #print 'old path :',o
            #print 'new path :',n
            
            shutil.move(o.decode('utf8'),n.decode('utf8')) 
            
            rs = "100100000"
            
        except Exception,e:
            os.chdir(root_path)
            print 'move flder :',e
        
    os.chdir(root_path)
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")    

# 文件重命名
@csrf_exempt
def filerename(request):
    rs = "100100210"
    fid = request.POST.get("fid",0)
#    print 'fid :',fid
    fname = request.POST.get("fname","")
    if fid and fname:
        try:
            uf = Fileinfo_up.objects.filter(id=fid)
            if uf:
                uf = uf[0]#FILE_SAVE_PATH+
                db_path = uf.path
#                print "db_path :",db_path,type(db_path)
                old_p = "%s%s%s%s" %(FILE_SAVE_PATH,db_path,uf.name,uf.ftype)
                new_p = "%s%s%s%s" %(FILE_SAVE_PATH,db_path,fname,uf.ftype)
#                print 'ppppppppp'
                old_p_im = "%s%sim/%s1%s" %(FILE_SAVE_PATH,db_path,uf.name,uf.ftype)
                old_p_im2 = "%s%sim/%s2%s" %(FILE_SAVE_PATH,db_path,uf.name,uf.ftype)
                uf.name = fname
#                print 'fname :',fname
                os.chdir(FILE_SAVE_PATH)
#                print 'do rename...'
#                print "old_p :",old_p
#                print "new_p :",new_p
                os.rename(old_p.decode('utf8'),new_p.decode('utf8'))
                # im
#                print "old_p_im :",old_p_im
                if os.path.isfile(old_p_im):
                    new_p_im = "%s%sim/%s1%s" %(FILE_SAVE_PATH,db_path,fname,uf.ftype)
                    os.rename(old_p_im.decode('utf8'),new_p_im.decode('utf8'))
                    
#                print "old_p_im2 :",old_p_im2
                if os.path.isfile(old_p_im2):
                    new_p_im2 = "%s%sim/%s2%s" %(FILE_SAVE_PATH,db_path,fname,uf.ftype)
                    os.rename(old_p_im2.decode('utf8'),new_p_im2.decode('utf8'))
                uf.save()
                rs = "100100000"
        except Exception,e:
            os.chdir(root_path)
            print " file rename :",e
    os.chdir(root_path)
    data = {'returncode':rs,'message':get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

# shihl
def getphoto(request):
    
    return 

@csrf_exempt
def check_user(request,uri,arg={1:1}):
    
    username = getusername(request)
    tmp_uri = "system"
    tmp_uri2 = "thunderdownload"
    if (tmp_uri.upper() in uri.upper() or tmp_uri2.upper() in uri.upper()) and "admin"!=username:
        return HttpResponseRedirect("/")
        
    user = User.objects.filter(UserName = username)
    #print '---->',user
    if not user:
        return HttpResponseRedirect("/")
    user = user[0]
    if user.login == 1:
        d = dict([["UserName",user.UserName]] + arg.items())
        return render_to_response(uri,d,context_instance=RequestContext(request))
    
    return HttpResponseRedirect("/")
    #return render_to_response('Default/Account/Login.html',{},context_instance=RequestContext(request))

@csrf_exempt
def login_info(request):
    name = getusername(request)
    return render_to_response('Default/Account/login-infor.html',{'UserName':name},context_instance=RequestContext(request))

@csrf_exempt
def login(request):
#	response = HttpResponseRedirect('Default/Home/Index.html')
#	response.set_cookie('UserName','',1)
	uf = UserForm()
	return render_to_response('Default/Account/Login.html',{'uf':uf},context_instance=RequestContext(request))



def playerview(request):
    return check_user(request,"Default/Music/Index.html",arg={1:1})
#    name,realname = getusername(request),getrealname(request)
#    return render_to_response("Default/Music/Index.html",{'UserName':name,'realname':realname},context_instance=RequestContext(request))

@csrf_exempt
def diskoperationboot(request):
    return check_user(request,"Default/Account/diskoperationboot.html",arg={1:1})

def player(request):
    return check_user(request,"Default/Music/Player.html",arg={1:1})
#    name,realname = getusername(request),getrealname(request)
#    return render_to_response("Default/Music/Player.html",{'UserName':name,'realname':realname},context_instance=RequestContext(request))

@csrf_exempt
def uploadview(request):
	name,realname = getusername(request),getrealname(request)
	return render_to_response("Default/Music/UploadFile.html",{'UserName':name,'realname':realname},context_instance=RequestContext(request))

#照片上传
@csrf_exempt
def upphotou(request):
	return uploadfile(request,1)

# 照片列表
@csrf_exempt
def photolist(request):
    return check_user(request,"Default/Photo/List.html",arg={1:1})

# 照片时间列表
@csrf_exempt
def phototimeline(request):
    return check_user(request,"Default/Photo/Timeline.html",arg={1:1})


# 音频上传
@csrf_exempt
def uploadmusic(request):
	return uploadfile(request,3)

# 文件 删除
@csrf_exempt
def deletefile(request):
    file_id = request.POST.get('fid',[])
    isdel = "0"#request.POST.get('isdel','0')  #isdel  0:直接删除，1：回收站
    rs = "100100209"
    #print 'file_id :',file_id
    if file_id:
        try:
            file_id = [int(i) for i in file_id.split(',')]
        except Exception,e:
            print e
            file_id = [file_id]
    #print 'file_id2 :',file_id
    fs = Fileinfo_up.objects.filter(id__in=file_id)
    if fs:
        for f in fs:
            f.filestatus = 1
            try:
                file_path = "%s%s%s%s" %(FILE_SAVE_PATH,f.path,f.name,f.ftype)
                #print "file_path :",file_path
                if isdel=="0":
                    os.remove(file_path)
                    file_path_im = "%s%sim/%s2%s" %(FILE_SAVE_PATH,f.path,f.name,f.ftype)
                    os.remove(file_path_im)
                    file_path_im = "%s%sim/%s1%s" %(FILE_SAVE_PATH,f.path,f.name,f.ftype)
                    os.remove(file_path_im)
                    f.delete()
                elif isdel=="1": #回收站文件夹
                    f.save()
                rs = "100100000"
            except Exception,e:
                if f:
                    #f.save()   
                    f.delete()
                    rs = "100100000"
                print e
    data = {'returncode':rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")


#  视频中心
@csrf_exempt
def video_view(request):
    return check_user(request,"Default/Video/Index.html")

@csrf_exempt
def video_player_view(request):
    return check_user(request,"Default/Video/Player.html")

@csrf_exempt  
def video_upload_view(request):
    return check_user(request,"Default/Video/UploadFile.html")

##############
##
##         下载中心
##
##############
@csrf_exempt
def download_view(request):
    return check_user(request,"Default/Download/Index.html")

@csrf_exempt
def getdownfilelist(request):
    user = getusername(request)
    if not user:
        rs = "100102246"
        data = {'returncode':rs,'message':get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    rs = ""
    status = request.POST.get("status","") # status
    dedelete = 0#request.POST.get("dedelete",0)  # 是否是回收站
    username = getusername(request)
    search = request.POST.get("keyword",None)
    dfs = Fileinfo_down.objects.filter(user=username)
    try:
        if status:
            dfs = dfs.filter(status=status)
        if search:
            dfs = dfs.filter(name__icontains=search)
        dfs,pageTotal = paginator(request,dfs)
        objs = format_obj(dfs,6)
    except Exception,e:
        print 'get down center file err :',e
        return formatResponse()
    return formatResponse(objs,pageTotal)

@csrf_exempt
def thunderdown(request):
    path = "%s"%(request.POST.get("file",""))
    def readfile(fn, buf_size=200000):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
    return HttpResponse(readfile(path))

@csrf_exempt
def playvideo(request):
    path = request.GET.get("path","")
    fn = FILE_SAVE_PATH + path
    def readfile(path, buf_size=200000):
        f = open(path, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
    return HttpResponse(readfile(fn))

# 新增下载文件
#@check_user
@csrf_exempt
def adddownload(request):
    rs = "100102224"
    username = getusername(request)
    user = User.objects.filter(UserName = username)
    if user:
        user = user[0]
    else:
        data = {'returncode':rs,"message":get_message(rs)}
        return HttpResponse(json.dumps(data))
    pname = request.POST.get("pname","")
    ourl = Fileinfo_down.objects.filter(url=pname,user=username)
    if ourl:
        godown = request.POST.get("godown",None)
        if not godown:
            rs = "100102233"
            data = {'returncode':rs,"message":get_message(rs)}
            return HttpResponse(json.dumps(data))
#    print "pname :",pname
    fname,fsize = main_down.getDowFileName(pname)
#    print "FFFFF :",fname,fsize
    if fsize==0 or fname == 0:
        rs = "100102229"
        data = {'returncode':rs,"message":get_message(rs)}
        return HttpResponse(json.dumps(data))
    if pname:
        try:
            dt = datetime.datetime.now()
            df = Fileinfo_down()
            if len(ourl)>=1:
                df.name = "%s(%s)" %(os.path.splitext(fname)[0],len(ourl)-1)
            else:
                df.name = os.path.splitext(fname)[0]
            
            df.type = 0
            df.downloadstarttime = dt.strftime("%Y%m%d%H%M%S")
            df.url = pname
            df.totalfilesize = fsize
            df.percent = "0.0%"
            df.status = 2
            df.ftype = os.path.splitext(fname)[1]
            df.user = username
            df.userid = user
            df.downloadtotaltime = 0
            df.dtonk = dt.strftime("%Y%m%d%H%M%S%f")
            df.downloadedtime = str(time.time())
            df.timestamp = "0"
            
            df.save()
            
            main_down.check_dic(username)
            rs = "100100000"
        except Exception,e:
            print 'get downfile info err:',e
    
    data = {'returncode':rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json") 

# 开始下载
@csrf_exempt
def start_down(request):
    rs = "100102225"
    fids = request.POST.get("fids","")#
    if fids:
        fids = fids.split(",")
        try:
            dfs = Fileinfo_down.objects.filter(id__in=fids)
#            print 'dfs :',dfs
            for df in dfs:
                if df.status == 1:
                    rs = "100100000"
                    continue
                main_down.start_Down(df)
                rs = "100100000"
        except Exception,e:
            print 'start_down erro :',e
    
    data = {'returncode':rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json") 
    
    
# 停止下载
@csrf_exempt
def stop_down(request):
    rs = "100102226"
    fids = request.POST.get("fids","")#
    
    if fids:
        fids = fids.split(",")
        try:
            
            dfs = Fileinfo_down.objects.filter(id__in=fids)
            for df in dfs:
                if df.status == 3 or df.status == 1:
                    rs = "100100000"
                    continue
                
                main_down.stopDown(df)
                
                rs = "100100000"
        except Exception,e:
            print 'stop_down erro :',e
    
    data = {'returncode':rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json") 
    

# 删除下载文件
@csrf_exempt
def deldownfile(request):
    
    rs = "100102227"
    fids = request.POST.get("fids","")#
    #	print "fids :",fids

    if fids:
        fids = fids.split(",")
        dfs = Fileinfo_down.objects.filter(id__in=fids)
        for df in dfs:
            try:
                
                main_down.dropDown(df)
                
                rs = "100100000"
            except Exception,e:
                print 'del down file :',e

    data = {'returncode':rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")


#
@csrf_exempt
def downfile(request):
    user_name = getusername(request)
    #admin/photo/sss.jpg
    filepath = request.POST.get("filename",request.GET.get("filename",""))#"admin/photo/15-1109150Q30812.jpg"
    #print "filepath  :",filepath 
    if not filepath:
        return HttpResponse(0)
    fl = filepath.split('/')
    fname = fl[-1]
    #print 'fffffffffff :',fname
    fp = '/'.join(fl[0:-1])+"/"
    file_name,t = os.path.splitext(fname)
    #print "file_name :",file_name
    
    #fobj = Fileinfo_up.objects.filter(path=fp,name=file_name)
    #file_path = ""
    #if fobj:
    
    file_path = "%s%s" %(FILE_SAVE_PATH,filepath)
    #print '==================>',format(fname)
    
    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' %(fname.decode("utf8").encode("gbk"))
    return response

def file_iterator(file_path,chunk_size=102400):
    #print '----------',file_path
    f = open(file_path,'rb')
    #with open(file_path) as f:
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break
    f.close()




#  BT下载中心
@csrf_exempt
def btdownload_view(request):
	return check_user(request,"Default/BTDownload/Index.html")

@csrf_exempt
def btdownload_upload_view(request):
	return check_user(request,"Default/BTDownload/UploadFile.html")

# 迅雷下载 
@csrf_exempt
def thunderd_view(request):
	return check_user(request,"Default/ThunderDownload/Index.html")

@csrf_exempt
def thunderd_upload_view(request):
	return check_user(request,"Default/ThunderDownload/UploadFile.html")

@csrf_exempt
def thunderd_moveFolder_view(request):
	return check_user(request,"Default/ThunderDownload/MoveFolder.html")


# 文件管理中心
@csrf_exempt
def filecenter(request):
	return check_user(request,"Default/FileCenter/Index.html")

@csrf_exempt
def center_upload_view(request):
	return check_user(request,"Default/FileCenter/UploadFile.html")

@csrf_exempt
def center_movefolder_view(request):
    return check_user(request,"Default/FileCenter/MoveFolder.html")

@csrf_exempt
def publicmove(request):
    return check_user(request,"Default/FileCenter/PublicMove.html")

# 系统文件管理
@csrf_exempt
def tmp_main(request):
    try:
        
        return render_to_response("Default/System/Main.html",{},context_instance=RequestContext(request))
    except Exception,e:
        print 'eeee :',e
    
    return HttpResponse()
# 系统文件管理
@csrf_exempt
def system(request):
	return check_user(request,"Default/System/Index.html")

@csrf_exempt
def userlist(request):
	users = User.objects.filter()
	return render_to_response("Default/System/UserList.html",{"useerlist":users},context_instance=RequestContext(request))

@csrf_exempt
def adduser(request):
	return check_user(request,"Default/System/AddUserlist.html")

@csrf_exempt
def systemresources(request):
	return check_user(request,"Default/System/ResourcesMonitor.html")


#   共享与权限
@csrf_exempt
def winviewconfig(request):
	return check_user(request,"Default/System/WinViewConfig.html")

@csrf_exempt
def ftpviewconfig(request):
	return check_user(request,"Default/System/FtpViewConfig.html")

@csrf_exempt
def usergroup(request):
	return check_user(request,"Default/System/UserGroup.html")

@csrf_exempt
def sharefolder(request):
	return check_user(request,"Default/System/ShareFolder.html")

@csrf_exempt
def sharefolderedit(request):
    return check_user(request,"Default/System/ShareFolderEdit.html")


#  用户设置
@csrf_exempt
def insideuseredit(request):
	arg = {1,1}
	username = request.GET.get("username","")
	u = User.objects.filter(UserName=username)
	if u:
		u = u[0]
		arg = {"User":u}#.UserName,"realname"u.realname:,"email":u.email}
	
	return check_user(request,"Default/System/InsideUserEdit.html",arg)

@csrf_exempt
def usergrouplist(request):
	return check_user(request,"Default/System/UserGroupList.html")

@csrf_exempt
def insideusergroupedit(request):
	return check_user(request,"Default/System/InsideUserGroupEdit.html")

@csrf_exempt
def addusergroup(request):
	return check_user(request,"Default/System/AddUsergroup.html")

@csrf_exempt
def addsharefolder(request):
	return check_user(request,"Default/System/AddShareFolder.html")

# 注册/ 新增用户
@csrf_exempt
def register(request):
    postType = request.POST.get("devicetype",request.GET.get("devicetype","5"))
    username1 = request.POST.get("userName",request.POST.get("username",""))
    realname = request.POST.get("realName",request.POST.get("realname",""))
    email = request.POST.get("email","")
    username= re.sub('[^A-Za-z0-9]','',username1)
    print 1
    for e in system_user:
        if username.upper() == e.upper():
            data = {'returncode':'100100111','message':get_message('100100111')}
            return HttpResponse(json.dumps(data),content_type="application/json")
    ou = User.objects.filter(UserName=username)
    print 2
    if ou:
        data = {'returncode':'100100101','message':get_message('100100101')}
        return HttpResponse(json.dumps(data),content_type="application/json")
    u = User()
    u.UserName = username
    u.realname = realname
    u.Password = "123456"
    u.email = email
    print 3
    try:
        p = FILE_SAVE_PATH+username
        #mf = p.split("/mnt/")
        #o="zfs create %s"%(mf[1].decode("utf8"))
        #i="zfs set mountpoint=%s %s"%(p,mf[1].decode("utf8"))
        #os.system(o)
        #os.system(i)
        #os.makedirs(p)
        #o = "setfacl -d -m u:thunder:r-- %s"%(p)
        #os.system(o)
        #ua = "useradd -d %s %s"%(p.decode("utf8"),username.decode("utf8"))
        #os.system(ua)
        #up = pexpect.spawn('passwd %s' %(username.decode("utf8")))
        #up.expect('New')
        #up.sendline("123456")
        #up.expect('Retype')
        #up.sendline("123456")
        #up.interact()
        #sba = pexpect.spawn('smbpasswd -a %s' %(username.decode("utf8")))
        #sba.expect('New')
        #sba.sendline("123456")
        #sba.expect('Retype')
        #sba.sendline("123456")
        #sba.interact()
        print 4
        o="mininas_user_create %s 123456"%(username.decode("utf8"))
        #o="/mnt/operate_without_expect.sh 2 %s 123456 0"%(username.decode("utf8"))
        os.system(o)
        o="mininas_user_create_home %s %s"%(username.decode("utf8"),p)
        os.system(o)
        u.save()
        print 5
        if p:
            # create dir
            for d in system_path:
                pp = "%s/%s" %(p,d)
                if not os.path.exists(pp):
                    #mf=pp.split("/mnt/")
                    #o="zfs create %s"%(mf[1].decode("utf8"))
                    #i="zfs set mountpoint=%s %s"%(pp,mf[1].decode("utf8"))
                    #os.system(o)
                    #os.system(i)
                    os.makedirs(pp)
                    os.system("chown %s:%s %s"%(username,username,pp))
                    os.system("chmod 755 %s"%pp)
                    #os.system("chattr +a %s"%pp)
            syc_bak = "%s/sync" %(p)
            if os.path.exists(syc_bak):
                ff = open(syc_bak+"/addbook","w")
                ff.close()
#        input =open("/etc/proftpd/proftpd.conf")
#        ws= input.read()
#        input.close()
#        wl="<Directory %s>\n   <Limit ALL>\n      AllowUser %s\n   </Limit>\n</Directory>\n"%(p,username)
#        ws=ws+wl
#        input =open("/etc/proftpd/proftpd.conf","w")
#        input.write(ws)
#        input.close()
        data = {'returncode':'100100000','message':get_message()}
        return HttpResponse(json.dumps(data),content_type="application/json")
    except Exception,e:
        print 'UUUUUUU :',e
        pass
    data = {'returncode':'100100103','message':get_message('100100103')}
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def uploadfileforie(request):
    return check_user(request,"Default/FileCenter/UploadFileForIE.html")

@csrf_exempt
def createnewug(request):
	groupname=request.POST.get("groupName","")
	describe=request.POST.get("remark","")
	ou = Group.objects.filter(groupname=groupname)
	if ou:
		data = {'returncode':'100100001','message':get_message('100100001')}
		return HttpResponse(json.dumps(data),content_type="application/json")
	data={}
	g=Group()
	g.groupname=groupname
	g.describe=describe
	g.save()
	users=User.objects.filter()
	for user in users:
		ug=Usergroup()
		ug.groupname = groupname
		ug.username = user.UserName
		ug.groupid = g.id
		ug.save()
	ua = "groupadd %s "%(groupname.decode("utf8"))
	os.system(ua)
	data['returncode']=100100000
	return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def edituserug(request):
	check=request.POST.get("check","")
	uncheck=request.POST.get("uncheck","")
	username=request.POST.get("username","")
	if check:
		check1 = check.split(',')
		for c in check1:
			ug=Usergroup.objects.get(id=c)
			ug.ingroup=1
			ua = "usermod -a -G %s %s"%(ug.groupname.decode("utf8"),username.decode("utf8"))
			os.system(ua)
			ug.save()
	if uncheck:
		uncheck1 = uncheck.split(',')
		for uc in uncheck1:
			ug=Usergroup.objects.get(id=uc)
			ug.ingroup=0
			ua = "gpasswd -d %s %s"%(username.decode("utf8"),ug.groupname.decode("utf8"))
			os.system(ua)
			ug.save()
	data={}
	data['returncode']=100100000
	return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getuginfo(request):
	id=request.POST.get("groupid","")
	group=Group.objects.get(id = id)
	data={}
	data2={}
	if group:
		data2['groupname']=group.groupname
		data2['describe']=group.describe
		data['data']=data2
		data['returncode']=100100000
	return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def editug(request):
	id=request.POST.get("groupid","")
	name=request.POST.get("groupname","")
	des=request.POST.get("describe","")
	group=Group.objects.get(id = id)
	data={}
	if group:
		group.groupname=name
		group.describe = des
		ua = "groupmod -n %s %s"%(name.decode("utf8"),group.groupname.decode("utf8"))
		os.system(ua)
		ug = Usergroup.objects.filter(groupid=id)
		if ug:
			for pug in ug:
				pug.groupname=name
				pug.save()
		group.save()
		data['returncode']=100100000
	return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def delug(request):
	id=request.POST.get("groupid","")
	group = Group.objects.get(id = id)
	data={}
	if group:
		ua = "groupdel %s"%(group.groupname.decode("utf8"))
		os.system(ua)
		ug = Usergroup.objects.filter(groupid=id)
		if ug:
			for pug in ug:
				pug.delete()
		group.delete()
		data['returncode']=100100000
	return HttpResponse(json.dumps(data),content_type="application/json")


@csrf_exempt
def getuserug(request):
	name=request.POST.get("username","")
	ug=Usergroup.objects.filter(username=name)
	data={}
	olist=[]
	data['returncode']=100100000
	if ug:
		for u in ug:
			data2={}
			up=Group.objects.get(groupname=u.groupname)
			data2['groupid']=u.id
			data2['groupname']=u.groupname
			data2['describe']=up.describe
			data2['ingroup']=u.ingroup
			olist.append(data2)
	data['data']=olist
	return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getallug(request):
	ug=Group.objects.filter()
	data={}
	olist=[]
	data['returncode']=100100000
	for u in ug:
		data2={}
		data2['groupid']=u.id
		data2['groupname']=u.groupname
		data2['describe']=u.describe
		olist.append(data2)
	data['data']=olist
#	print data
	return HttpResponse(json.dumps(data),content_type="application/json")


#    存储设置

@csrf_exempt
def diskmanagement(request):
	return check_user(request,"Default/System/DiskManagement.html")

@csrf_exempt
def diskcouponmanagement(request):
	return check_user(request,"Default/System/DiskCouponManagement.html")



#      磁盘

@csrf_exempt
def insideeditdisk(request):
	return check_user(request,"Default/System/InsideEditDisk.html")

@csrf_exempt
def adddisk(request):
	return check_user(request,"Default/System/AddDisk.html")

@csrf_exempt
def editdisk(request):
    id=request.POST.get("id","")
    des=request.POST.get("description","")
    data={}
    sf=Diskinfo.objects.get(id=id)
    sf.describe = des
    sf.save()
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def deldisk(request):
    data={}
    rl=Zpoolinfo.objects.filter()
    if rl:
        data['returncode']="100101201"
        data['message']=get_message('100101201')
    else:
        id=request.POST.get("id","")
        sf=Diskinfo.objects.get(id=id)
        sf.delete()
        data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getdiskdes(request):
    id=request.POST.get("id","")
    data={}
    sf=Diskinfo.objects.get(id=id)
    if sf:
        data2={}
        data2['name']=sf.name
        data2['description']=sf.describe
        data['data']=data2
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getdiskdetail(request):
    sid=request.POST.get("sid","")
    data={}
    data2={}
#    c1=diskctl.getdiskname(sid)
#    if c1 == 0:
#        p1=diskctl.getlastrdinfo()
#        for p in p1.get('subset'):
#            if p.get('disk').get('sn') == sn:
#                data2['name'] = p.get('disk').get('snshort')
#                data2['devname'] = p.get('disk').get('model')
#                data2['capacity'] = p.get('disk').get('capacity')
#                data2['rotationrate'] = p.get('disk').get('rotationrate')
#                data2['bus'] = p.get('disk').get('bus')
#                data2['sn'] = p.get('disk').get('sn')
#                data2['status'] = "0"
#                data['data']=data2
#                data['returncode']="100100000"
#                print data
#                return HttpResponse(json.dumps(data),content_type="application/json")
#    else:
#        d1=diskctl.getdiskinfo(c1)
#        data2['name'] = d1.get('snshort')
#        data2['devname'] = d1.get('model')
#        data2['capacity'] = d1.get('capacity')
#        data2['rotationrate'] = d1.get('rotationrate')
#        data2['bus'] = d1.get('bus')
#        data2['sn'] = d1.get('sn')
#        data2['status'] = "1"
#        data['data']=data2
#        data['returncode']="100100000"
#        print data
#        return HttpResponse(json.dumps(data),content_type="application/json")
    data2['model'] = diskctl.getmodel(sid)
    data2['capacity'] = diskctl.getsize(sid)
    data2['rotationrate'] = diskctl.getrotationrate(sid)
    data2['serialshort'] = diskctl.getserialshort(sid)
    data2['uuid'] = diskctl.getuuid(sid)
    data2['subuuid'] = diskctl.getsubuuid(sid)
    #data2['status'] = 
    data['data']=data2
    data['returncode']="100100000"
    data['message']=get_message('100100000')
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def finddisk(request):
    data={}
    sflist=[]
    clist=[]
    check=0
    sl=os.popen("lsblk").readlines()
    si=os.popen("lsblk -ln -o NAME,TYPE | grep disk | awk '{print $1}'").readlines()
    if sl:
        for l in sl:
            if si:
                for dname in si:
                    xs=dname.split('\n')
                    if "/\n" not in l and xs[0] in l:
                            sf=Diskinfo.objects.filter(name=xs[0])
                            if not sf and xs[0] not in clist:
                                clist.append(xs[0])
                    elif "/\n" in l and xs[0] in l:
                            check=xs[0]
    clist.remove(check)
    for e in clist:
        ys="udevadm info --query=all --name=/dev/%s"%(e)
        yl=os.popen(ys).readlines()
        for y in yl:
            if 'ID_SERIAL=' in y:
                yyt=y.split('=')
                data2={}
                data2['name']=e
                data2['serial']=yyt[1]
                sflist.append(data2)
    data['data']=sflist
    data['returncode']=100100000
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def setdisk(request):
    name=request.POST.get("name","")
    des=request.POST.get("description","")
    o=Diskinfo()
    ys="udevadm info --query=all --name=/dev/%s"%(name)
    yl=os.popen(ys).readlines()
    for y in yl:
        if 'ID_SERIAL=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.serial=x[0]
        if 'ID_ATA_ROTATION_RATE_RPM=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.rotationrate=x[0]
        if 'ID_VENDOR=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.vendor=x[0]
        if 'ID_TYPE=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.type=x[0]
        if 'DEVNAME=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.path=x[0]
        if 'ID_MODEL=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.model=x[0]
        if 'ID_SERIAL_SHORT=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.serialshort=x[0]
        if 'ID_BUS=' in y:
            c=y.split('=')
            x=c[1].split('\n')
            o.bus=x[0]
    o.name=name
    o.status="normal"
    o.describe=des
    ss="lsblk -lnb | grep %s | grep disk| awk '{print $4}'"%name
    s = os.popen(ss).read()
    o.capacity = int(s)/(1024*1024*1024)
    o.save()
    data={}
    data['returncode']=100100000
    return HttpResponse(json.dumps(data),content_type="application/json")


#      磁盘 卷管理
@csrf_exempt
def adddiskcoupon(request):
    return check_user(request,"Default/System/AddDiskCoupon.html")

@csrf_exempt
def dlna(request):
    return check_user(request,"Default/System/DLNA.html")

@csrf_exempt
def timemachine(request):
    return check_user(request,"Default/System/TimeMachine.html")

@csrf_exempt
def tmget(request):
    d1= tmctl.loadjson()
    sflist=[]
    if d1 !=0:
        for e in d1.get('share'):
            data2={}
            data2['TM_FOLDER_NAME'] = e.get('TM_FOLDER_NAME')
            data2['TM_FOLDER_SIZE'] = str(int(e.get('TM_FOLDER_SIZE'))/1000)
            data2['TM_FOLDER_UUID'] = e.get('TM_FOLDER_UUID')
            data2['TM_FOLDER_USER'] = e.get('TM_FOLDER_USER')
            sflist.append(data2)
    data={}
    data['list']=sflist
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def tmadd(request):
    name=request.POST.get("name","")
    uname=request.POST.get("user","")
    size=request.POST.get("size","")
    tmctl.addtmf(uname,name,size)
    data={}
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def tmedit(request):
    name=request.POST.get("name","")
    size=request.POST.get("size","")
    uuid=request.POST.get("uuid","")
    tmctl.edittmf(name,uuid,size)
    os.system("systemctl restart netatalk.service")
    data={}
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def tmdel(request):
    fid=request.POST.get("uuid","")
    print fid
    tmctl.deltmf(fid)
    data={}
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def insideeditdiskcoupon(request):
    return check_user(request,"Default/System/InsideEditDiskCoupon.html")

@csrf_exempt
def editraid(request):
    id=request.POST.get("id","")
    des=request.POST.get("description","")
    data={}
    sf=Zpoolinfo.objects.get(id=id)
    sf.describe = des
    sf.save()
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def replacedisk(request):
    data={}
    result=diskctl.checkrdinfo()
    if result==101:
        re=diskctl.doreplace()
        if re == 1:
            data['returncode']='100100000'
            data['message']=get_message('100100000')
        else:
            data['returncode']='100101208'
            data['message']=get_message('100101208')
    elif result == 100:
        data['returncode']='100101206'
        data['message']=get_message('100101206')
    elif result == 102:
        data['returncode']='100101207'
        data['message']=get_message('100101207')
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def delraid(request):
    data={}
    o="umount /mnt/1 > /run/test.txt 2>&1"
    os.system(o)
    input =open("/run/test.txt")
    lines = input.readlines()
    input.close()
    os.system("mininas_pool_disable")
    for l in lines:
        if "busy" in l:
            data = {'returncode':'100101204','message':get_message('100101204')}
            return HttpResponse(json.dumps(data),content_type="application/json")
    try:
        fu=Fileinfo_up.objects.filter()
        if fu:
            for f in fu:
                f.delete()
        fd=Fileinfo_down.objects.filter()
        if fd:
            for f in fd:
                f.delete()
        sys=Syssetting.objects.get(id=1)
        sys.hasraid=0
        sys.save()
        #Sharefuser #Zfsinfo #BtFileinfo_down  shihl
        tsharefuser = Sharefuser.objects.filter()
        for t in tsharefuser:
            t.delete()
#        tzfsinfo = Zfsinfo.objects.filter()
#        for tz in tzfsinfo:
#            tz.delete()
        btf = BtFileinfo_down.objects.filter()
        for b in btf:
            b.delete()
#        input =open("/etc/samba/smb.conf")
#        hs = input.readlines()
#        input.close()
#        input =open("/etc/samba/smb.conf","w")
#        ws=""
#        i=0
#        for e in hs:
#            if "guest account" in e:
#                ws=ws+e
#                ws=ws+"\n"
#                break
#            ws=ws+e
#        input.write(ws)
#        input.close()
#        input =open("/etc/proftpd/proftpd.conf")
#        lines= input.readlines()
#        input.close()
#        ws=""
#        for l in lines:
#            if "DefaultRoot" in l:
#                ws=ws+l
#                break
#            ws=ws+l
#        input =open("/etc/proftpd/proftpd.conf","w")
#        input.write(ws)
#        input.close()
        sambactl.setnosf()
        tmp = Timer(5,sysreboot)
        tmp.start()
        data['returncode']="100100000"
    except Exception:
        data['returncode']="100101202"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getraiddes(request):
    id=request.POST.get("id","")
    data={}
    sf=Zpoolinfo.objects.get(id=id)
    if sf:
        data2={}
        data2['name']=sf.name
        sdf="/mnt/1/"%(sf.name)
        st = os.statvfs(sdf)
        data2['capacity']=str(int(st.f_blocks * st.f_frsize)/(1024*1024))+" MB"
        data2['used']=str(int((st.f_blocks * st.f_frsize)-(st.f_bavail * st.f_frsize))/(1024*1024))+" MB"
        data2['avail']=str(int(st.f_bavail * st.f_frsize)/(1024*1024))+" MB"
        data2['description']=sf.describe
        data['data']=data2
    data['returncode']=100100000
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getraidlist(request):
    data={}
    sflist=[]
    sf=Zpoolinfo.objects.filter()
    for s in sf:
        data2={}
        data2['id']=s.id
        data2['name']=s.name
        sdf="/mnt/1/"%(s.name)
        st = os.statvfs(sdf)
        data2['capacity']=str(int(st.f_blocks * st.f_frsize)/(1024*1024))+" MB"
        data2['used']=str(int((st.f_blocks * st.f_frsize)-(st.f_bavail * st.f_frsize))/(1024*1024))+" MB"
        data2['avail']=str(int(st.f_bavail * st.f_frsize)/(1024*1024))+" MB"
        data2['description']=s.describe
        sflist.append(data2)
    data['data']=sflist
    data['returncode']=100100000
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getrdinfo(request):
    data={}
    sflist=[]
    #sf=Diskinfo.objects.filter()
    #for s in sf:
        #data2={}
        #dl=Zpoolinfo.objects.filter()
        #if dl:
            #for d in dl:
                #if s.name in d.device:
                    #continue
                #else:
                    #data2['id']=s.id
                    #data2['name']=s.name
                    #data2['serial']=s.serial
                    #sflist.append(data2)
        #else:
            #data2['id']=s.id
            #data2['name']=s.name
            #data2['serial']=s.serial
            #sflist.append(data2)
    #data['data']=sflist
    #data['returncode']=100100000

#    data3={}
#    data3['mode']= diskctl.getvtype(1)
#    dlist=[]
#    dlist=diskctl.getreadydisks(1)
#    for e in dlist:
#        d= diskctl.ifdiskmounted(e)
#        if d == "1":
#            data2={}
#            data2['slot']=e
#            data2['serialshort'] = diskctl.getserialshort(e)
#            data2['model'] = diskctl.getmodel(e)
#            data2['rotationrate'] = diskctl.getrotationrate(e)
#            data2['size'] = diskctl.getsize(e)
#            data2['uuid'] = diskctl.getuuid(e)
#            data2['subuuid'] = diskctl.getsubuuid(e)
#            sflist.append(data2)
#    data3['disklist']=sflist

#    if result == 100:
#        rd1=diskctl.getlastrdinfo()
#        data3['mode']=rd1.get('mode')
#        data3['raidname']= rd1.get('label')
#        for r in rd1.get('subset'):
#            data2={}
#            data2['name'] = r.get('disk').get('snshort')
#            data2['sn'] = r.get('disk').get('sn')
#            data2['status'] = '1'
#            sflist.append(data2)
#        data3['disklist']=sflist
#    elif result == 101:
#        rd1=diskctl.getlastrdinfo()
#        data3['raidname']= rd1.get('label')
#        data3['mode']=rd1.get('mode')
#        for r in rd1.get('subset'):
#            re1 = diskctl.searchdisk(r.get('disk').get('sn'))
#            data2={}
#            data2['name'] = r.get('disk').get('snshort')
#            data2['sn'] = r.get('disk').get('sn')
#            if re1 ==1:
#                data2['status'] = '1'
#            else:
#                data2['status'] = '0'
#            sflist.append(data2)
#        data3['disklist']=sflist
#    elif result == 102:
#        rd1=diskctl.getlastrdinfo()
#        data3['raidname']= rd1.get('label')
#        data3['mode']=rd1.get('mode')
#        for r in rd1.get('subset'):
#            data2={}
#            data2['name'] = r.get('disk').get('snshort')
#            data2['sn'] = r.get('disk').get('sn')
#            data2['status'] = '0'
#            sflist.append(data2)
#        data3['disklist']=sflist
#    elif result == 103:
#        data3['mode']=""
#        data3['raidname']=""
#        data3['disklist']=sflist
#
#    data4={}
#    data4['readylist'] = data3
#    sflist=[]
    print 1
    dlist=diskctl.getdisklist()
    print 2
    if dlist:
        for e in dlist:
#            d= diskctl.ifdiskmounted(e)
#            if d != "1":
            d= diskctl.ifslotempty(e)
            if d==1:
                data2={}
                data2['slot']=e
                data2['serialshort'] = diskctl.getserialshort(e)
                data2['model'] = diskctl.getmodel(e)
                data2['rotationrate'] = diskctl.getrotationrate(e)
                data2['size'] = diskctl.getsize(e)
                data2['uuid'] = diskctl.getuuid(e)
                data2['subuuid'] = diskctl.getsubuuid(e)
                sflist.append(data2)
    data4={}
    data4['slotlist'] = sflist
    print 3
    data3={}
    data3['mode']= diskctl.getvtype(1)
    sflist=[]
    dlist=diskctl.gethistory(1)
    print 4
    for e in dlist:
        data2={}
        data2['slot']=e
        data2['serialshort'] = diskctl.getserialshorthistory(e)
        data2['model'] = diskctl.getmodelhistory(e)
        data2['rotationrate'] = diskctl.getrotationratehistory(e)
        data2['size'] = diskctl.getsizehistory(e)
        data2['uuid'] = diskctl.getuuidhistory(e)
        data2['subuuid'] = diskctl.getsubuuidhistory(e)
        sflist.append(data2)
    print 5
    data3['disklist']=sflist
    data4['history'] = data3
    data5={}
    d=diskctl.ifvolumeempty(1)
    print 6
    if d ==1:
        data5['total']=diskctl.getvolumetotal(1)
        data5['type']=diskctl.getvolumetype(1)
        data5['uuid']=diskctl.getvolumeuuid(1)
        data5['enable']=diskctl.getvolumestatus(1)
    print 7
    data4['volumeinfo']=data5
    data['data'] = data4
    data['returncode']='100100000'
    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getnewrd(request):
    data={}
    sflist=[]
    tpdlist=[]
    dlist=diskctl.getdisklist()
    if dlist:
        for e in dlist:
            data2={}
            data2['serialshort'] = diskctl.getserialshort(e)
            data2['model'] = diskctl.getmodel(e)
            data2['rotationrate'] = diskctl.getrotationrate(e)
            data2['size'] = diskctl.getsize(e)
            data2['uuid'] = diskctl.getuuid(e)
            data2['subuuid'] = diskctl.getsubuuid(e)
            data2['status'] = 'new'
            sflist.append(data2)
#        rd1=diskctl.getlastrdinfo()
#        for r in rd1.get('subset'):
#            tpdlist.append(r.get('disk').get('sn'))
#    dlist=diskctl.getalldisks()
#    for d in dlist:
#        data2={}
#        d1=diskctl.getdiskinfo(d)
#        if d1.get('sn') not in tpdlist:
#            data2['name'] = d1.get('snshort')
#            data2['serial'] = d1.get('sn')
#            sflist.append(data2)
    data['data']=sflist
    data['returncode']='100100000'
    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def ifraid(request):
    rst=diskctl.ifpoolsmounted(1)
    data={}
    data2={}
    data2['raid']=rst
    data['data']=data2
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def createraid(request):
    rtype=request.POST.get("rtype","")#0single,1raid1
    disks=request.POST.get("disks","")
#    des=request.POST.get("description","")
    rst=diskctl.ifpoolsmounted(1)
    if rst == "1":
        data = {'returncode':'100101201','message':get_message('100101201')}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data={}
    disk = disks.split(',')
#        dd=Diskinfo.objects.get(id=d)
#        ys="udevadm info --query=all --name=/dev/%s"%(dd.name)
#        yl=os.popen(ys).readlines()
#        for y in yl:
#            if 'ID_SERIAL=' in y:
#                yy=y.split("\n")
#                yyt=yy[0].split('=')
#                #print dd.serial
#                #print yyt[1]
#                if dd.serial == yyt[1]:
#                    continue
#                else:
#                    data = {'returncode':'100101203','message':get_message('100101203')}
#                    return HttpResponse(json.dumps(data),content_type="application/json")
#    obj = Zpoolinfo.objects.filter()
#    if not obj:
    if len(disk) == 1:
        print "s1"
        d1=diskctl.ifdiskmounted(disk[0])
        if d1 is not "1":
            dp=diskctl.ifdiskpath(disk[0])
            if dp:
                os.system("mininas_pool_make_volume -d single %s"%disk[0])
        else:
            data['returncode']="100101111"
            return HttpResponse(json.dumps(data),content_type="application/json")
    elif len(disk) == 2:
        if rtype == '0':
            d1 = diskctl.ifdiskmounted(disk[0])
            d2 = diskctl.ifdiskmounted(disk[1])
            if d1 is not "1" and d2 is not "1":
                dp1=diskctl.ifdiskpath(disk[0])
                dp2=diskctl.ifdiskpath(disk[1])
                if dp1 and dp2:
                    os.system("mininas_pool_make_volume -d single %s %s"%(disk[0],disk[1]))
            else:
                data['returncode']="100101111"
                return HttpResponse(json.dumps(data),content_type="application/json")
        elif rtype == '1':
            d1 = diskctl.ifdiskmounted(disk[0])
            d2 = diskctl.ifdiskmounted(disk[1])
            if d1 is not "1" and d2 is not "1":
                dp1=diskctl.ifdiskpath(disk[0])
                dp2=diskctl.ifdiskpath(disk[1])
                if dp1 and dp2:
                    os.system("mininas_pool_make_volume -d raid1 %s %s"%(disk[0],disk[1]))
            else:
                data['returncode']="100101111"
                return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data['returncode']="100101111"
            return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        data['returncode']="100101111"
        return HttpResponse(json.dumps(data),content_type="application/json")
#        if rtype == '0':
#            os.system(z)
#        elif rtype == '1':
#            os.system(o)
#        j="zfs set acltype=posixacl %s"%(name)
#        os.system(j)
#        dlist=[]
#        dslist=[]
#        zp=Zpoolinfo()
#        zp.name=name
#        zp.raidtype=rtype
#        zp.describe=des
#        zp.path= name
#        sdf="/mnt/%s/"%(name)
#        zp.mountpoint=sdf
#        sf="zfs create %s/Share"%(name)
#        i="zfs set mountpoint=/mnt/%s/Share %s/Share"%(name,name)
#        o = "setfacl -m d:u:thunder:r-- %sShare"%(sdf)
#        os.system(sf)
#        os.system(i)
#        os.system(o)
#        sf="zfs create %s/update"%(name)
#        i="zfs set mountpoint=/mnt/%s/update %s/update"%(name,name)
#        o = "setfacl -m d:u:thunder:r-- %supdate"%(sdf)
#        os.system(sf)
#        os.system(i)
#        os.system(o)
#        sf1="zfs create %s/Share/Movie"%(name)
#        i1="zfs set mountpoint=/mnt/%s/Share/Movie %s/Share/Movie"%(name,name)
#        os.system(sf1)
#        os.system(i1)
#        sf2="zfs create %s/Share/Photo"%(name)
#        i2="zfs set mountpoint=/mnt/%s/Share/Photo %s/Share/Photo"%(name,name)
#        os.system(sf2)
#        os.system(i2)
#        sf3="zfs create %s/Share/Music"%(name)
#        i3="zfs set mountpoint=/mnt/%s/Share/Music %s/Share/Music"%(name,name)
#        os.system(sf3)
#        os.system(i3)
#        st = os.statvfs(sdf)
#        zp.capacity = (st.f_blocks * st.f_frsize)
#        for d in disk:
#            d1=Diskinfo.objects.get(id=d)
#            dlist.append(str(d1.name))
#            dslist.append(str(d1.serial))
#        #print 'dlist :',dlist
#        #print 'dslist :',dslist
#        zp.device=dlist
#        zp.deviceserial=dslist
#        zp.save()
    sys=Syssetting.objects.get(id=1)
    sys.uploadrootpath="/mnt/1/"
    sys.hasraid=1
    sys.save()
#    input =open("/etc/proftpd/proftpd.conf")
#    lines=input.readlines()
#    input.close()
#    input =open("/etc/proftpd/proftpd.conf","w")
#    ws=""
#    for line in lines:
#        if 'DefaultRoot    ' in line:
#            line="DefaultRoot     %s\n<Directory %s*>\n   <Limit ALL>\n      DenyAll\n   </Limit>\n</Directory>\n"%(sdf,sdf)
#        ws=ws+line
#    input.write(ws)
#    input.close()
    input=open("%swelcome.msg"%(sys.uploadrootpath),"w")
#        #ll=" "
#        #input.write(ll)
    global FILE_SAVE_PATH
#        #print 'nnnnnnnnnn :',name
    FILE_SAVE_PATH="/mnt/1/"
#        o="zfs set aclinherit=passthrough %s/Share"%name
#        os.system(o)
#        try:
#            settings.FILE_SAVE_PATH = urp.uploadrootpath
#            urp=Syssetting.objects.get(id=1)
#            urp.uploadrootpath = FILE_SAVE_PATH
#            urp.save()
#        except:pass
#    #    print FILE_SAVE_PATH
#        input.close()
#    else:
#        obj = obj[0] #one 磁盘卷名  sdb 磁盘名
#        #print '--------------->',obj.name
#        disks = Diskinfo.objects.filter(id__in=disk)
#        for d in disks:
#            if d.name in obj.device or d.serial in obj.deviceserial:
#                continue
#            o = "zpool add %s %s -f" %(obj.name,d.name)
#            #print 'ooooooooooooooooo :',o
#            os.system(o)
    users = [u.UserName for u in User.objects.filter()]
    if not users:
        users.append("admin")
        now_user = getusername(request)
        if now_user != "admin":
            users.append(now_user)
#    input =open("/etc/proftpd/proftpd.conf")
#    ws= input.read()
#    input.close()
#    input =open("/etc/proftpd/proftpd.conf","w")
    for u in users:
        p = FILE_SAVE_PATH+u
        
        if not os.path.exists(p):
#            #mf=p.split("/mnt/")
#            #o="zfs create %s"%(mf[1].decode("utf8"))
#            #i="zfs set mountpoint=%s %s"%(p,mf[1].decode("utf8"))
#            #os.system(o)
#            #os.system(i)
            os.makedirs(p)
            o="mininas_user_create_home %s %s"%(u,p)
            os.system(o)
            os.system("chown %s:%s %s"%(u,u,p))
            os.system("chmod 755 %s"%p)
            #os.system("chattr +a %s"%p)
#            if u == "admin":
#                os.system("mkdir -p /mnt/1/admin")
#                os.system("chown admin:admin /mnt/1/admin")
#                os.system("chmod 775 /mnt/1/admin")
#                os.makedirs(p+"/Public")
#                os.system("chown root:admin %s/Public"%p)
#                os.system("chmod 755 %s/Public"%p)
#            if u != "admin":
            if u:
                for pp in system_path:
                    pp = "%s/%s" %(p,pp)
    #                #mf=pp.split("/mnt/")
    #                #o="zfs create %s"%(mf[1].decode("utf8"))
    #                #i="zfs set mountpoint=%s %s"%(pp,mf[1].decode("utf8"))
    #                #os.system(o)
    #                #os.system(i)
                    os.makedirs(pp)
                    os.system("chown %s:%s %s"%(u,u,pp))
                    os.system("chmod 755 %s"%pp)
                    #os.system("chattr +a %s"%pp)
                syc_bak = "%s/sync" %(p)
                if os.path.exists(syc_bak):
                    ff = open(syc_bak+"/addbook","w")
                    ff.close()
    os.makedirs("/mnt/1/timemachine")
    os.system("chown root:admin /mnt/1/timemachine")
    os.system("chmod 755 /mnt/1/timemachine")
    os.makedirs("/mnt/1/nobody")
    os.system("chown root:admin /mnt/1/nobody")
    os.system("chmod 755 /mnt/1/nobody")
    os.makedirs("/mnt/1/nobody/Public")
    os.system("chown root:admin /mnt/1/nobody/Public")
    os.system("chmod 755 /mnt/1/nobody/Public")
#            o="setfacl -R -m d:u:%s:rwx %s"%(u,p)
#            os.system(o)
#        wl="<Directory %s>\n   <Limit ALL>\n      AllowUser %s\n   </Limit>\n</Directory>\n"%(p,u)
#        ws=ws+wl
#    input.write(ws)
#    input.close()
    for a in range(0,100):
        if a<10:
            pp=FILE_SAVE_PATH+"nobody/smbshare00"+str(a)
            p="smbshare00"+str(a)
            os.makedirs(pp)
            os.system("chown admin:%s %s"%(p,pp))
            os.system("chmod 2775 %s"%(pp))
        else:
            pp=FILE_SAVE_PATH+"nobody/smbshare0"+str(a)
            p="smbshare0"+str(a)
            os.makedirs(pp)
            os.system("chown admin:%s %s"%(p,pp))
            os.system("chmod 2775 %s"%(pp))
    rst=diskctl.ifpoolsmounted(1)
    if rst != "1":
        data = {'returncode':'100101202','message':get_message('100101202')}
        return HttpResponse(json.dumps(data),content_type="application/json")
    tmp = Timer(5,restart)
    tmp.start()
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def addtimemachine(request):
    return check_user(request,"Default/System/AddTimeMachine.html",arg={1:1})

@csrf_exempt
def addraid(request):
    disk = request.POST.get("disk","")
    d = diskctl.ifdiskmounted(disk)
    data={}
    if d is not "1":
        os.system("mininas_pool_add_device %s"%disk)
        data['returncode']='100100000'
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        data['returncode']='100101209'
        return HttpResponse(json.dumps(data),content_type="application/json")

def restart():
    os.system("systemctl restart disk-watcher.service")
    os.system("systemctl restart mininas.service")

#    系统设置
@csrf_exempt
def getsflist(request):
    data={}
    sflist=[]
    data['data']=sambactl.getsflist()
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getsfuname(request):
    data={}
    us=User.objects.filter()
    unlist=[]
    for u in us:
        if u.UserName != "admin":
            data2={}
            data2['id']=u.id
            data2['name']=u.UserName
            unlist.append(data2)
    data['data']=unlist
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getuseracl(request):
    data={}
    name=request.POST.get("name","")
    data2={}
    d=sambactl.loadjson()
    for i in d.share:
        if i.get('SMB_FOLDER_NAME') == name:
            id=i.get('SMB_SID')
    data2['group'] = os.popen("mininas_share_members -n %s"%id)
    data2['groupro'] = os.popen("mininas_share_members -n %s -r"%id)
    data['data']=data2
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def setsharefolder(request):
    name = request.POST.get("name","")
    print name
    if name.upper()=="HOME" or name.upper()=="PUBLIC":
        data['returncode']='100100211'
        return HttpResponse(json.dumps(data),content_type="application/json")
    des = request.POST.get("description","")
    print des
    available = request.POST.get("available","")
    option = request.POST.get("option","")
    allowguest = request.POST.get("allowguest","")
    allowguest = "1"#1=never 0=bad user
    group = request.POST.get("group","")
    rogroup = request.POST.get("rogroup","")
    print 0
    sf = Sharefuser.objects.filter()
    sidlist=[]
    print 1
    if sf:
        for s in sf:
            sidlist.append(s.sfid)
    for i in range(0,100):
        if i not in sidlist:
            break
    print 2
    nsf = Sharefuser()
    nsf.foldername = name
    nsf.sfid = i
    print 3
    nsf.available = available
    nsf.option = int(option)
    nsf.allowguest = int(allowguest)
    nsf.save()
    data={}
    print i,allowguest,option,name,des,available,group,rogroup
    print 4
    sambactl.addsf(i,allowguest,option,name,des,available,group,rogroup)
    os.system("systemctl restart smbd.service")
    os.system("systemctl restart nmbd.service")
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def editsharefolder(request):
    name=request.POST.get("name","")
    sid = request.POST.get("sid","")
    des=request.POST.get("description","")
    available = request.POST.get("available","")
    option = request.POST.get("option","")
    allowguest = request.POST.get("allowguest","")
    group = request.POST.get("group","")
    rogroup = request.POST.get("rogroup","")
    sambactl.editsf(name,des,available,option,allowguest,group,rogroup)
    data={}
    os.system("systemctl restart smbd.service")
    os.system("systemctl restart nmbd.service")
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def delsharefolder(request):
    nsid=request.POST.get("sid","")
    print nsid
    sambactl.delsf(nsid)
    print 11
    sf=Sharefuser.objects.filter(sfid=int(nsid))
    print 1
    if sf:
        print 2
        i=int(nsid)
        print 3
        if i<10:
            sid = "00"+str(i)
        else:
            sid = "0"+str(i)
        path="/mnt/1/nobody/smbshare%s/"%sid
        print path
        os.system("rm -rf %s..?* %s.[!.]* %s*"%(path,path,path))
        data={}
        sf[0].delete()
        os.system("systemctl restart smbd.service")
        os.system("systemctl restart nmbd.service")
        data['returncode']='100100000'
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        data={}
        data['returncode']='100100214'
        return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def powersupplysetup(request):
    return check_user(request,"Default/System/PowerSupplySetup.html")

@csrf_exempt
def upgradepress(request):
    return check_user(request,"Default/System/UpgradePress.html")

@csrf_exempt
def rebootorhalt(request):
    type=request.POST.get("type","")
    data={}
    if str(type) == '0':
        tt=Timer(5,sysreboot)
    elif str(type) == '1':
        tt=Timer(5,syshalt)
    data['returncode']='100100000'
    tt.start()
    return HttpResponse(json.dumps(data),content_type="application/json")

def sysreboot():
    os.system('reboot')

def syshalt():
    os.system('poweroff')

@csrf_exempt
def timemachineedit(request):
    return check_user(request,"Default/System/TimeMachineEdit.html")

@csrf_exempt
def anupgradesetup(request):
    return check_user(request,"Default/System/AnUpgradeSetup.html")

@csrf_exempt
def checkversion(request):
#    input =open("/etc/mininas/version")
#    lines = input.readlines()
#    input.close()
#    data={}
#    data2={}
#    for l in lines:
#        if "MiniNAS" in l:
#            sp=l.split(" ")
#            data2['version']=sp[1]+"."+sp[2]+"."+sp[3]
    data={}
    data2={}
    data2['curr_version']=str(os.popen("cat /etc/mininas/sysupgrade/curr_version").read().rstrip())
    data2['next_version']=str(os.popen("cat /etc/mininas/sysupgrade/next_version").read().rstrip())
    data2['status']=str(os.popen("cat /etc/mininas/sysupgrade/status").read().rstrip())
    data['data']=data2
    data['returncode']="100100000"
    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def doupgrade(request):
    #os.system("wget http://www.winsuntech.cn/NasUpdate/version.txt -P /etc/mininas/update")
    #input =open("/etc/mininas/update/version.txt")
    #lines = input.readlines()
    #data={}
    #for l in lines:
#        if "lastest" in l:
#            sp=l.split(" ")
#        if sp:
#            if sp[1] in l:
#                s=l.split(" ")
#    o="wget %s -P /etc/mininas/update"%(s[1])
#    os.system(o)
#    t="/etc/mininas/update/mininasupguide.sh /etc/mininas/update/mininas-%s.tar.gz"%(sp[1])
#    os.system(t)
#    i="rm /etc/mininas/update/mininas-%s.tar.gz"%(sp[1])
#    os.system(i)
#    os.system("rm /etc/mininas/update/version.txt")
#    data['returncode']="100100000"
#----------------------------------------------
#    ver=request.POST.get('version','')
#    HOST='127.0.0.1'
#    PORT=51234
#    #print 11111
#    print ver
#    w="10102:%s"%(ver)
#    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#    s.connect((HOST,PORT))
#    s.sendall(w)
#    data=s.recv(1024)
#    s.close()
    tt=Timer(5,goupd)
    tt.start()
    data={}
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

def goupd():
    os.system("mininas_sysupgrade")
    
@csrf_exempt
def dorestore(request):
    tmp_system = False
    tt=Timer(5,gorestore)
    data={}
    tt.start()
#    if tmp_system:
    data['returncode']="100100000"
    data['message']=get_message.get("100102244")
#        return HttpResponse(json.dumps(data),content_type="application/json")
#    
#    data['returncode']="100102243"
#    data['message']=get_message.get("100102243")
    return HttpResponse(json.dumps(data),content_type="application/json")
    

def gorestore():
    rs = os.system("/etc/mininas/rfs/mininasrfsguide.sh")
#    if rs==0:
#        tmp_system = True
#    else:
#        tmp_system = False

@csrf_exempt
def checkupdate(request):
#    os.system("wget http://www.winsuntech.cn/NasUpdate/version.txt -P /etc/mininas/update")
#    input =open("/etc/mininas/update/version.txt")
#    lines = input.readlines()
#    data={}
#    data2={}
#    for l in lines:
#        if "lastest" in l:
#            sp=l.split(" ")
#            data2['version']=sp[1]
#    os.system("rm /etc/mininas/update/version.txt")
#    data['data']=data2
#    data['returncode']="100100000"
    HOST='127.0.0.1'
    PORT=51234
    print 1
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    s.sendall("10100")
    data=s.recv(1024)
    print 2
    s.close()
    return HttpResponse(data,content_type="application/json")


@csrf_exempt
def restoredefaultsetup(request):
    return check_user(request,"Default/System/RestoreDefaultSetup.html")

@csrf_exempt
def thunderset(request):
    return check_user(request,"Default/System/ThunderSet.html")

@csrf_exempt
def winviewedit(request):
    utype = request.POST.get('usertype','')
    bios = request.POST.get('bios','')
    workgroup = request.POST.get('workgroup','')
    utype = "0"
    sambactl.editconf(workgroup,bios,utype)
    os.system("systemctl restart smbd.service")
    os.system("systemctl restart nmbd.service")
    data={}
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getwinview(request):
    d1=sambactl.loadjson()
    data={}
    data2={}
    ww = Syssetting.objects.get(id=1)
    #data2['trigger']=ww.samba
    data2['workgroup']=d1.get('SMB_WORKGROUP')
    data2['bios']=d1.get('SMB_NETBIOS_NAME')
    if d1.get('SMB_MAP_TO_USER') == 'bad user':
        data2['usertype'] = 1
    else:
        data2['usertype'] = 0
    data['returncode']="100100000"
    data['data']=data2
    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def triggerwinview(request):
    trigger = request.POST.get('trigger','')
    ww  = Syssetting.objects.get(id=1)
    ww.samba=trigger
    ww.save()
    if trigger == "1":
        os.system("service samba start")
        os.system("chkconfig -a samba")
    elif trigger == "0":
        os.system("service samba stop")
        os.system("chkconfig -d samba")
    data={}
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def ftpviewedit(request):
    port = request.POST.get('port','')
    maxclient = request.POST.get('maxclients','')
    maxconnection = request.POST.get('maxconnections','')
    maxlogin = request.POST.get('maxlogin','')
    timeout = request.POST.get('timeout','')
    welmessage = request.POST.get('welmessage','')
    utype = request.POST.get('usertype','')
    ww = Syssetting.objects.get(id=1)
    input=open("%swelcome.msg"%(ww.uploadrootpath),"w")
    input.write(welmessage)
    input.close()
    ftpctl.editconf(timeout,port,maxclient,maxconnection,maxlogin,ww.uploadrootpath,utype)
    os.system("systemctl restart proftpd.service")
    data={}
    data['returncode']="100100000"
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getftpview(request):
    d1=ftpctl.loadjson()
    ww = Syssetting.objects.get(id=1)
    data={}
    data2={}
    data2['trigger']=ww.ftp
    data2['port']=d1.get('FTP_PORT')
    data2['maxclients']=d1.get('FTP_MAX_CLIENTS')
    data2['maxconnections']=d1.get('FTP_MAX_HOST')
    data2['maxlogin']=d1.get('FTP_MAX_LOGIN')
    data2['timeout']=d1.get('FTP_TIMEOUT_IDLE')
    if d1.get('FTP_ANONYMOUS_PATH'):
        data2['usertype']=1
    else:
        data2['usertype']=0
    data['returncode']="100100000"
    input=open("%swelcome.msg"%(ww.uploadrootpath))
    ws=""
    if input:
        lines = input.readlines()
        input.close()
        for line in lines:
            ws=ws+line
    data2['welmessage']=ws
    data['data']=data2
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def triggerftpview(request):
    trigger = request.POST.get('trigger','')
    ww  = Syssetting.objects.get(id=1)
    ww.ftp=trigger
    ww.save()
    if trigger == "1":
        os.system("service proftpd start")
        os.system("chkconfig -a proftpd")
    elif trigger == "0":
        os.system("service proftpd stop")
        os.system("chkconfig -d proftpd")
    data={}
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getcpuinfo(request):
    data={}
    data2={}
    data2['Cpu']=str(100-psutil.cpu_percent(1))
    data['data']=data2
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def memoryusage(request):
    return check_user(request,"Default/System/MemoryUsage.html")

@csrf_exempt
def getmeminfo(request):
    data={}
    data2={}
    py=psutil.virtual_memory()
    data2['memtotal']=str(py.total)
    data2['memused']=str(py.used)
    data['data']=data2
    data['returncode']='100100000'
    #print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def bandwidth(request):
	return check_user(request,"Default/System/Bandwidth.html")

@csrf_exempt
def getnetinfo(request):
    data={}
    data2={}
    nt=psutil.net_io_counters()
    data2['rxdatanum']=str(nt.bytes_recv)
    data2['txdatanum']=str(nt.bytes_sent)
    data['data']=data2
    data['returncode']='100100000'
    #print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def thunderkey(request):
    tk=os.popen("/opt/xware/portal").readlines()
    data2={}
    for line in tk:
        if 'YOUR CONTROL PORT IS' in line:
            temp =line.split(": ")
            p=Syssetting.objects.get(id=1)
            p.tdport=temp[1]
            p.save()
        if 'THE ACTIVE CODE IS' in line:
            temp =line.split(": ")
            data2['code']=temp[1]
        if 'THIS DEVICE HAS BOUND TO USER' in line:
            temp =line.split(": ")
            data2['name']=temp[1]
    data={}
    data['returncode']='100100000'
    data['data']=data2
#    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def thunderunbound(request):
    p=Syssetting.objects.get(id=1)
    o="wget http://127.0.0.1:%s/unbind -P /tmp/"%(p.tdport)
    os.system(o)
    data={}
    os.system("rm /tmp/unbind")
    os.system("rm -rf thunder")
    data['returncode']='100100000'
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def netset(request):
    ip = request.POST.get('ip','')
    netmask = request.POST.get('submask','')
    gateway = request.POST.get('gateway','')
    dns1 = request.POST.get('dns1','')
    dns2 = request.POST.get('dns2','')
    type = request.POST.get('type','')
#    print type
#    input =open("/etc/network/interfaces")
#    lines = input.readlines()
#    input.close()
#    ws=""
#    data={}
#    input =open("/etc/network/interfaces","w")
    #lines= lines[:-3]
#    for line in lines:
    if type == '0':
        input=open("/etc/mininas/templates/network/dhcp_default")
        lines=input.read()
        input.close()
        input =open("/etc/network/interfaces","w")
        input.read(lines)
        input.close()
    elif type=='1':
        input = open("/etc/mininas/templates/network/static_default")
        lines=input.read()
        input.close()
        p=lines.replace("%%IP_ADDRESS%%",ip).replace("%%NETMASK%%",netmask).replace("%%GATEWAY%%",gateway)
        input =open("/etc/network/interfaces","w")
        input.read(p)
        input.close()
#ws=ws+line
#input.write(ws)
#input.close()
    data['returncode']="100100000"
    input = open("/etc/resolv.conf")
    lines = input.readlines()
    ws = ""
    input.close()
    input = open("/etc/resolv.conf","w")
    i=0
    for line in lines:
        if 'nameserver' in line:
            if i is 0:
                
                line = "nameserver %s\n"%(dns1)
                i=i+1
            else :
                line = "nameserver %s\n"%(dns2)
        ws=ws+line
    input.write(ws)
    input.close()
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def netget(request):
    input =open("/etc/network/interfaces")
    lines = input.readlines()
    input.close()
    data={}
    data2={}
    for line in lines:
        if "eth0" not in lines:
            data2['type']=0
            ls=os.popen("ip route").readlines()
            for l in ls:
                if "default via" in l and "eth0" in l:
                    s=l.split(" ")
                    data2['gateway']=s[2]
            ls=os.popen("ifconfig").readlines()
            i=0
            for l in ls:
                if i == 1:
                    s=l.split(":")
                    t=s[1].split(" ")
                    data2['ip']=t[0]
                    t=s[3].split("\n")
                    data2['submask']=t[0]
                    i=0
                    break
                if "eth0" in l:
                    i =1
            break
        elif 'eth0' in lines:
            data2['type']=1
        if 'address' in line:
            temp =line.split(" ")
            data2['ip']=temp[1]
        if 'netmask' in line:
            temp =line.split(" ")
            data2['submask']=temp[1]
        if 'gateway' in line:
            temp =line.split(" ")
            data2['gateway']=temp[1]
    data['returncode']="100100000"
    input = open("/etc/resolv.conf")
    lines = input.readlines()
    input.close()
    i=1
    for line in lines:
        if 'nameserver' in line:
            temp = line.split(" ")
            ss=temp[1].split("\n")
            data2['dns'+str(i)]=ss[0]
            i=i+1
    data['data']=data2
#    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def timeareasetup(request):
    return check_user(request,"Default/System/TimeAreaSetup.html")

@csrf_exempt
def networksetup(request):
    return check_user(request,"Default/System/NetworkSetup.html")

@csrf_exempt
def filecenter(request):
    return check_user(request,"Default/FileCenter/Index.html")

@csrf_exempt
def getntptime(request):
    data={}
    data2={}
    if request.method == 'POST':
        obj = Ntpinfo.objects.get(id=1)
        data2['address']=str(obj.address)
        data2['port']=obj.port
        data2['refresh_seq']=obj.refreshtime
        data['data']=data2
    data['returncode']='100100000'
#    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def setntptime(request):
    data={}
    if request.method == 'POST':
        try:
            ip=request.POST.get('server','')
            port=request.POST.get('port','')
            refresh=request.POST.get('refresh','')
            c= ntplib.NTPClient()
            response = c.request('time.windows.com')
            ts= response.tx_time
            dat1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ts))
            tt=time.strptime(dat1,'%Y-%m-%d %H:%M:%S')
            dat="date -s %u-%02u-%02u"%(tt.tm_year,tt.tm_mon,tt.tm_mday)
            time1="date -s %02u:%02u:%02u"%(tt.tm_hour,tt.tm_min,tt.tm_sec)
            os.system(dat)
            os.system(time1)
            obj = Ntpinfo.objects.get(id=1)
            obj.address=ip
            obj.port=port
            obj.refreshtime=refresh
            obj.save()
            data['returncode']="100100000"
        except Exception,e:
            print 'EEEEE :',e
            data['returncode']="100100000"
            pass
    #print 1111
    #print data
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def setlocaltime(request):
    data={}
    if request.method == 'POST':
        sec=int(request.POST.get('second',''))+8*60*60
        dat1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(sec))
        tt=time.strptime(dat1,'%Y-%m-%d %H:%M:%S')
        dat="date -s %u-%02u-%02u"%(tt.tm_year,tt.tm_mon,tt.tm_mday)
        time1="date -s %02u:%02u:%02u"%(tt.tm_hour,tt.tm_min,tt.tm_sec)
        os.system(dat)
        os.system(time1)
        data['returncode']="100100000"
        data['message']=get_message("100100000")
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def getnowtime(request):
    data={}
    data2={}
    data2['second']=str(time.strftime('%Y-%m-%d %X',time.localtime(time.time())))
    data['data']=data2
    data['returncode']='100100000'
#    print data
    return HttpResponse(json.dumps(data),content_type="application/json")

# 获取文件大小
def fSize(p):
    
    if not os.path.isfile(p):
        return "0 b"

    size=os.path.getsize(p)
    tmp_size = str(size)
    rs = "1 B"
    m_s = len(tmp_size)/3
    if m_s<= 1:
        rs = "%.2f KB"% (size/1024.0)
    elif m_s == 2:
        rs = "%.2f MB"% (size/1024.0/1024.0)
    else:
        rs = "%.2f GB"% (size/1024.0/1024.0/1024.0)
    return rs

#把秒换时间格式
def fTime(ss):
    if not ss:
        return "00:00:00"
    
    h = "00"
    m = "00"
    s = "00"
    th = ss%3600
    if th>0:
        h = str(int(ss/3600))
        if len(h)<2:
            h = "0%s"%h
        th = ss%3600
        if th%60>0:
            m = str(int(th/60))
            if len(m)<2:
                m = "0%s"%m
            s = str(th%60)
            if len(s)<2:
                s = "0%s"%s
    return "%s:%s:%s" %(h,m,s)

#上传
@csrf_exempt
def uploadfile(request):
    try:
        user = getusername(request)
        print 1
        if not user:
            rs = "100102246"
            data = {'returncode':rs,'message':get_message(rs)}
            return HttpResponse(json.dumps(data),content_type="application/json")
        rs = u"100100000"
        user_name = getusername(request)
        user = User.objects.filter(UserName = user_name)
        if user:
            user = user[0]
        print 2
        act = request.POST.get("act",None)
        obj = request.FILES.get("file",None)
        t = request.POST.get("type",0)
    except e:
        print e
    try:
        t = int(t)
    except:
        t = 0
    print 3
    dir_type = upload_dir.get(t)  # 获取文件该放到那个种类中
    if dir_type:
        p = '%s%s/%s/' % (FILE_SAVE_PATH,user_name,dir_type)
    else:
        p = '%s%s/' % (FILE_SAVE_PATH,user_name)
    if act and act !="/":
        p = '%s%s' % (FILE_SAVE_PATH,act)
    print 4
    fileName = request.POST.get("name")
    file_path = '%s%s' %(p,fileName)
    file_name,ftype=os.path.splitext(fileName)
    fu = Fileinfo_up.objects.filter(path=act,name=file_name,ftype=ftype)
    print 5
    path = ("%s%s"%(p,fileName)).decode("utf8")
    tfi=Tmpfileinfo.objects.filter(path=path)
    if fu and not tfi:
        try:
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fu = fu[0]
            fu.uploadstarttime = t
            fu.uploadedtime = t
            fu.save()
        except:
            pass
        data = {"returncode":rs,"message":get_message(rs)}
        os.system("sync")
        os.system("echo 3 > /proc/sys/vm/drop_caches")
        print 6
        return HttpResponse(json.dumps(data),content_type="application/json")
    try:
        chunk_count = request.POST.get("chunks",0)
        chunknum = request.POST.get("chunk",0)
        postType = request.POST.get("devicetype","5")
        print 61
        if postType=="4":
            print chunk_count
            print chunknum
            if chunk_count:
                chunk_count = int(chunk_count)
            if chunknum:
                chunknum = int(chunknum)
        elif postType=="5":
            if chunk_count:
                chunk_count = int(chunk_count)
            if chunknum:
                chunknum = int(chunknum)
        print 7
        path = ("%s%s"%(p,fileName)).decode("utf8")
        tfi=Tmpfileinfo.objects.filter(path=path)
        if tfi:
            if chunk_count> chunknum+1 and chunknum<=tfi[0].count:
                print 8
                data = {"returncode":rs,"message":get_message(rs)}
                os.system("sync")
                os.system("echo 3 > /proc/sys/vm/drop_caches")
                return HttpResponse(json.dumps(data),content_type="application/json")
            elif chunk_count>chunknum+1 and chunknum > tfi[0].count:
                print 9
                tmpf = open(path,"ab")
                for chunk in obj.chunks():
                    tmpf.write(chunk)
                tmpf.close()
                tfi[0].count = chunknum
                tfi[0].save()
                data = {"returncode":rs,"message":get_message(rs)}
                if chunk:
                    del chunk
                if tmpf:
                    del tmpf
                if tfi:
                    del tfi
                os.system("sync")
                os.system("echo 3 > /proc/sys/vm/drop_caches")
                return HttpResponse(json.dumps(data),content_type="application/json")
            elif chunk_count==chunknum+1:
                print 10
                tmpf = open(path,"ab")
                for chunk in obj.chunks():
                    tmpf.write(chunk)
                tmpf.close()
                tfi[0].delete()
                if chunk:
                    del chunk
                print 11
        elif not tfi and chunk_count>1:
            print 12
            tmpf = open(path,"ab")
            for chunk in obj.chunks():
                tmpf.write(chunk)
            print 13
            tmpf.close()
            ntfi = Tmpfileinfo()
            ntfi.path = path
            ntfi.count = 0
            ntfi.save()
            print 14
            os.system("sync")
            os.system("echo 3 > /proc/sys/vm/drop_caches")
            data = {"returncode":rs,"message":get_message(rs)}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            print 15
            tmpf = open(path,"ab")
            for chunk in obj.chunks():
                tmpf.write(chunk)
            tmpf.close()
        print 16
        file_name,ftype=os.path.splitext(fileName) # 获取文件名 和 后缀
        if act:
            pppath = "%s" %(act)
        else:
            pppath = "%s/%s/" %(user_name,dir_type)
        os.system("chown %s:%s %s"%(user_name,user_name,path))
        os.system("chmod 644 %s"%path)
#        fu = Fileinfo_up.objects.filter(name=file_name,ftype=ftype,path=pppath)
#        if fu:
#        fu.size = os.path.getsize(file_path)#fSize(file_path)
#        fu.type = t
#        fu.ftype = ftype
#        fu.owner = user_name
#        fu.lastwritetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        fu.uploadstarttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        fu.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        fu.uploadtotaltime = 1
#        fu.status = 1
#        fu.filestatus = 0
#        m=hashlib.md5()
#        input =open(file_path,'rb')
#        while 1:
#            blk = input.read(4096)
#            if not blk:
#                break
#            m.update(blk)
#        n=m.hexdigest()
#        input.close()
#        fu.md5=n
#        if t==3:
#            fu = muicOption(fu)
#        if t==1:
#            picOption(fu)
#        try: 
#            fu.save()
#            rs = "100100000"
#        except Exception,e:# 处理保存失败
#            print "UP :",e
        
        #os.rename(path+".tmpctcl",path)
        #input=open(path)
        #input.close()
        print 17
        rs = "100100000"
        os.system("sync")
        os.system("echo 3 > /proc/sys/vm/drop_caches")
        data = {"returncode":rs,"message":get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    except Exception,e:
        print "EEEEEEEEE",e
    os.system("sync")
    os.system("echo 3 > /proc/sys/vm/drop_caches")
    data = {"returncode":rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

# 图片缩略图
def picOption(fu):#(p,fileName):#(file_path):
    try:
        p = "%s%s" %(FILE_SAVE_PATH,fu.path)
        file_path = '%s%s%s' %(p,fu.name,fu.ftype)
        img = Image.open(file_path)
        path_im = "%sim/" %(p)
            
        if not os.path.exists(path_im):
            os.makedirs(path_im)
        fp = "%s%s1%s" %(path_im,fu.name,fu.ftype)
        if not os.path.isfile(fp):
            #print fp,type(fp)
            img.thumbnail((180,180),Image.ANTIALIAS)
            img.save(fp.decode("utf8"))#)
        
        fp = "%s%s2%s" %(path_im,fu.name,fu.ftype)
        if not os.path.isfile(fp):
            #print fp,type(fp)
            img.thumbnail((80,80),Image.ANTIALIAS)
            img.save(fp.decode("utf8"))#)
    except Exception,e:
        print "UP Photo :",e

#音频信息
def muicOption(fu):
    try:
        file_path = '%s%s%s%s' %(FILE_SAVE_PATH,fu.path,fu.name,fu.ftype)
        f = eyed3.load(file_path)
        if f.tag:
            try:
                c=eval(repr(f.tag.artist)[1:])
                if "\u" in c:
                    fu.singer = c.decode("unicode-escape")
                else :
                    fu.singer = c.decode('gbk')
            except:pass
                #print f.tag.artist
            try:
                c=eval(repr(f.tag.album)[1:])
                if "\u" in c:
                    fu.ablum = c.decode("unicode-escape")
                else :
                    fu.ablum = c.decode('gbk')
            except:pass
            try:
                if f.tag.genre:
                    c=eval(repr(f.tag.genre.name)[1:])
                    if "\u" in c:
                        fu.style = c.decode("unicode-escape")
                    else :
                        fu.style = c.decode('gbk')
            except:pass
            try:
                c=eval(repr(f.tag.recording_date)[1:])
                if "\u" in c:
                    fu.age = c.decode("unicode-escape")
                else :
                    fu.age = c.decode('gbk')
            except:pass
        fu.duration = fTime(f.info.time_secs)
    except Exception,e:
        print 'Music ：',e
    return fu

#
#
#  逻辑
#
#上传
@csrf_exempt
def testupload(request):
    rs = u"100100000"
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES.get("file",None)
            
            filename = file.name
            
            o="/mnt/estor/aaa/%s"%(filename).decode('utf8')
            
            fd = open(o,"wb")
            
            for chunk in file.chunks():
                #print chunk
                fd.write(chunk)
            
            fd.close()
            
    data = {"returncode":rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

# 获取文件列表
@csrf_exempt
def getfile(request):
    user = getusername(request)
    if not user:
        rs = "100102246"
        data = {'returncode':rs,'message':get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    path = request.REQUEST.get("filePath","/")
    dedelete = 0#request.POST.get("dedelete",0)  # 是否是回收站
    type = request.POST.get("type",110)
    search = request.POST.get("keyword",None)
    order = request.POST.get("order",None)
    isTime = request.POST.get("istime",None)
    try:
        type = int(type)
    except:
        type = 110
    objs = []
    try:
        #print "path :",path,"type :",type,"filestatus :",dedelete
        fus = Fileinfo_up.objects.filter(filestatus=dedelete)#,
        if path and not search:
            fus = fus.filter(path=path)
        #print "fus :",len(fus)
#        if type !=4 and type!=110:
#            fus = fus.filter(type=type)
        #print "fus :",fus[0]
        if search and path:
            fus = fus.filter(path__icontains=path,name__icontains=search)
        #print 'FFFFFFFFFFFFFF'
        if order:
            fus = fus.order_by(order)
        #print 'GGGGGGGGGGGGGG'
        fus,pageTotal = paginator(request,fus)
        #print 'HHHHHHHHHHHHHH',type
        objs = format_obj(fus,type)
        
    except Exception,e:
        print 'EEEEEEEEE :',e
        return formatResponse()
    return formatResponse(objs,pageTotal)

# 获取相片——时间轴时间
@csrf_exempt
def gettimephono(request):
    
    fp = request.POST.get("path","")
    t = request.POST.get("mouth","")
    type = request.POST.get("type","1")
    limit = request.POST.get("limit",20)
    # path:"",mouth:"2015-8",type:1
#    print fp,t,type

    sql = """
        SELECT  name,uploadstarttime,uploadedtime,owner,path,ftype,id,size from mini_fileinfo_up
        where type=1 and date_format(uploadstarttime,'%%Y-%%m') = "%s" 
    """ %(t)
    if fp:
        sql += " and path = '%s' " %(fp)
    
    sql += " limit %s" %(limit)
    
#    print sql
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
#    rows = rows[:20]
#    print 'rows :',rows
    objs = []
    for row in rows:
        d = {}
        d["name"] = row[0]
        d["uploadstarttime"] = row[1]
        d["uploadedtime"] = row[2]
        d["owner"] = row[3]
        d["path"] = row[4]
        d["type"] = row[5]
        d["id"] = row[6]
        d["size"] = row[7]
        objs.append(d)
    data = {}
    data2 = {}
    data2['rows'] = objs
    data['returncode'] = "100100000"
    data['data'] = data2

#    print "DDDDDDDDDD :",data
    return HttpResponse(json.dumps(data),content_type="application/json")


#获取相片时间轴
@csrf_exempt
def timeresponse(request):
    user = getusername(request)
    if not user:
        rs = "100102246"
        data = {'returncode':rs,'message':get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    fp = request.POST.get("path","")
    ms = "100102231"
    sql = """
        SELECT  date_format(uploadstarttime,'%Y') as y,date_format(uploadstarttime,'%m') as m, count(id) from mini_fileinfo_up
         where type = 1 
    """
    if fp:
        sql += "and path = '%s' " %(fp)
    sql += " group BY y,m ORDER BY y,m desc  "
    rs = {"returncode":"100100000",}
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        L = cursor.fetchall()
        cursor.close()
        connection.close()
        
        data = {}
        
        for i in range(len(L)):
            
            data2 = {}
            data2["month"] = L[i][1]
            data2["number"] = L[i][2]
            
            if not data.has_key(L[i][0]):
                data[L[i][0]] = []
            
            if data.has_key(L[i][0]):
                data[L[i][0]].append(data2)
            
    #    print data
        
        keys = data.keys()
        d = []
        for j in keys:
            d2 = {}
            d2["year"] = j
            d2["data"] = []
            
    #        print "data[j] :",data[j]
            ll = data[j]
            for z in range(len(ll)):
                d3 = {}
                d3["number"] = ll[z].get("number")
                d3["month"] = ll[z].get("month")
                d2["data"].append(d3)
            
    #        print d2
            d.append(d2)
    #    print d
        rs["data"] = d
    except Exception,e:
        print 'time。。。',e

    data = {"returncode":ms,"message":get_message(ms)}
    return HttpResponse(json.dumps(rs),content_type="application/json")




def format_obj(objs,type=1):
    fobjs = []
    for obj in objs:
        data = {}
        if type == 1:
            data["id"] =obj.id
            data["name"] = obj.name
            data["type"] = obj.ftype
            data["size"] = fSize(FILE_SAVE_PATH+obj.path+obj.name+obj.ftype)
            data["size2"] = obj.size
            data["owner"] = obj.owner
            data["uploadedtime"] = str(obj.uploadedtime)
            data["path"] = str(obj.path)
            data["uploadstarttime"] = obj.uploadstarttime
            data["md5"] = obj.md5
            #
        elif type==3:
            data['id'] = obj.id
            data['name'] = obj.name
            data['type'] = obj.ftype
            data['size'] = fSize(FILE_SAVE_PATH+obj.path+obj.name+obj.ftype)
            data["size2"] = obj.size
            data['singer'] = obj.singer
            data['last_write_time'] = str(obj.lastwritetime)
            data['path'] = str(obj.path)
            data['owner'] = obj.owner
            data['ablum']=obj.ablum
            if obj.style:
                data['style']=obj.style.decode('utf8')
            else:
                data['style']=obj.style
            data['age']=obj.age
            data['duration']=obj.duration
            data['uploadstarttime'] = obj.uploadstarttime
            data["md5"] = obj.md5
            
        elif type==6: #下载
            data['id'] = obj.id
            data['name'] = obj.name
            data['ftype'] = obj.ftype
            data['user'] = obj.user
            data['percent'] = obj.percent
            data['downloadtotaltime'] = obj.downloadtotaltime
            data['totalfilesize'] = obj.totalfilesize
            data['status'] = down_type.get(obj.status)
            
            
        else:
            data["id"] =obj.id
            data["name"] = obj.name
            data["type"] = obj.ftype
            data["size"] = fSize(FILE_SAVE_PATH+obj.path+obj.name+obj.ftype)
            data["size2"] = obj.size
            data["owner"] = obj.owner
            data["uploadedtime"] = obj.uploadedtime
            data["path"] = str(obj.path)
            data["uploadstarttime"] = obj.uploadstarttime
            data["md5"] = obj.md5
        
        fobjs.append(data)
    
    return fobjs


def formatResponse(objs=[],pageTotal=0):
    
    data = {}
    data2 = {}

    data2['pageTotal'] = pageTotal
    data2['rows'] = objs
    data['returncode'] = "100100000"
    
    data['data'] = data2
    
    #print "DDDDDDDDDD :",data
    #HttpResponse(json.dumps(data))
    return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def fcentergfl(req):
    if req.method == 'POST':
        type=req.REQUEST.get('thunder','')
        name=req.REQUEST.get('filePath','')
        num=req.REQUEST.get('pageNumber',0)
        size=req.REQUEST.get('pageSize',10)
        #print 'ttttttt:',type
        if type =='1':
            #print '1'*30
            rt="%s%s"%(FILE_SAVE_PATH,name)
            os.chdir(rt)
            dirs=os.listdir(rt)
            data={}
            data2={}
            list=[]
            for d in dirs:
                isfile=os.path.isfile(d)
                if isfile and d != "welcome.msg":
                    list.append(d)
            
            size = int(size)
            num = int(num)
            if len(list)%size==0:
                pagetotal = str(int(len(list)/size))
            else:
                pagetotal = str(int(len(list)/size)+1)
            
            data2['pageTotal'] = pagetotal
            fl=[]
            list.sort()
            #print 'list :',len(list)
            if len(list)>0:
                for e in list[(num-1)*size:num*size]:
                    #print 'EEEEEEE :',e
                    data3={}
                    #t=e.split(".")
                    file_name,ftype=os.path.splitext(e)
                    #print '1'*30
                    data3['name']=file_name#t[0]
                    data3['ext']=ftype#t[1]
                    gs=u"%s"%(e)
                    #print '2'*30,e
                    data3['size']=os.path.getsize((FILE_SAVE_PATH+name+e).decode("utf8"))#gs.decode("utf8"))
                    lstc="stat %s"%(d)
                    #print '3'*30
                    lst=os.popen(lstc).readlines()
                    for line in lst:
                        if 'Modify:' in line:
                            tmp = line.split(" ")
                            spt = tmp[2].split(".")
                            data3['uploadedtime']= tmp[1]+' '+spt[0]
                    fl.append(data3)
            
            data2['rows']=fl
            data['data']=data2
            data['returncode']='100100000'
        else:
            #print 'A'*30
            data={}
            data2={}
            list=[]
            data['result']='success'
            filelist=getfilelist(name)
            data2['pageTotal']=str((len(filelist)/10)+1)
            filelist.sort()
            print 'filelist :',filelist
            if len(filelist)>0:
                for e in filelist:
                    filed=getfiledetailfc(e,name)
                    if filed.get('id') != '-1':
                        list.append(filed)
            data2['rows']=list
            data['data']=data2
            #print '----->',data
            data['returncode']='100100000'
    
    os.chdir(root_path)
    if data:
        #print data
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        return HttpResponse("1")

@csrf_exempt
def fcentergfdl(req):
    
    user = getusername(req)
    if not user:
        rs = "100102246"
        data = {'returncode':rs,'message':get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    
    if req.method == 'POST':
        type=req.REQUEST.get('thunder','')
        path=req.REQUEST.get('filePath','')
        
        if type=='1':
            data={}
            flist=[]
            rt="%s%s"%(FILE_SAVE_PATH,path)
            
            dirs=os.listdir(rt)
            for d in dirs:
                os.chdir(rt)
                isdir=os.path.isdir(d)
                unlist = [u.UserName for u in User.objects.filter()]
                if isdir and d != "ThunderDB" and d not in unlist and d != "Share" and d != "im" and d != "sync" and d != "bt" and d != "qqrec" and d != "update" and d!= "timemachine" and d!="nobody":
                    data2={}
                    lstc="stat '%s'"%(d)
                    lst=os.popen(lstc).readlines()
                    for line in lst:
                        if 'Modify:' in line:
                            tmp =line.split(" ")
                            spt = tmp[2].split(".")
                            data2['last_write_time']=tmp[1]+' '+spt[0]
                    path3=rt+d#path2+'/'+d
                    os.chdir(path3)
                    tk=os.popen("ls -d */").readlines()
                    if tk:
                        data2['subfolder']=1
                    else:
                        data2['subfolder']=0
                    sz=os.popen("du -hs").readlines()
                    temp = None
                    for line in sz:
                        temp =line.split("\t.\n")
                    if temp:
                        data2['size']=temp[0]
                    else:
                        data2['size']=0
                    data2['foldername']=d
                    data2['thumb']=''
                    flist.append(data2)
            data['returncode']='100100000'
            data['data']=flist
            os.chdir(root_path)
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            
            if not path or path == "" or path == u"" or path == "/":
                rs = "100102240"
                data = {"returncode":rs,"message":get_message(rs)}
                return HttpResponse(json.dumps(data),content_type="application/json")            
            
            try:
                name=req.REQUEST.get('filePath','a')
                #print 'NNNNNNNNNNNNN :',name
                data={}
                data2={}
                data['returncode']='100100000'
                filelist=getfolderlist(name)
                data['data']=filelist
                #print 'dddddddddddd :',data
                os.chdir(root_path)
                return HttpResponse(json.dumps(data),content_type="application/json")
            except Exception,e:
                'FFFFff :',e
#        print 'eeeeeeeeeeeeeeeee'
        if data:
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            return HttpResponse("1")

@csrf_exempt
def getfolderdeep(name):
    
    return HttpResponse("1")

@csrf_exempt
def getdirs(req):
    if req.method == 'POST':
        path=req.REQUEST.get('filePath','a')
        data={}
        data['result']='success'
        subfolders=getdir(path)
        data['length']=subfolders
    if data:
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        return HttpResponse("1")

def getfolderlist(name):
    #print 'name ------>',name
    #print 'FILE_SAVE_PATH >>>>',FILE_SAVE_PATH
    if name is not 'a':
        path=FILE_SAVE_PATH
        path2=path+name
        dirs=os.listdir(path2)
    else:
        dirs=os.listdir(FILE_SAVE_PATH)
        path2=FILE_SAVE_PATH
    list=[]
    #print "dirs :",dirs
    for d in dirs:
        print d
        if d == "ThunderDB" or d == "im" or d == "sync" or d == "qqrec" or d == "update" or d== "timemachine" or d=="nobody":
            continue
        os.chdir(path2)
        isdir=os.path.isdir(d)
        if isdir:
            data={}
            lstc="stat '%s'"%(d)
            lst=os.popen(lstc).readlines()
            for line in lst:
                if 'Modify:' in line:
                    tmp =line.split(" ")
                    spt = tmp[2].split(".")
                    data['last_write_time']=tmp[1]+' '+spt[0]
            #print '1'*30
            path3=path2+d#path2+'/'+d
            #print 'AAAAAAAAAAA',path3
            size = os.path.getsize(d)
            #print 'BBBBBBBBBBB',size
            os.chdir(path3)
            #print 'CCCCCCCCCCCCC'
            if 'Windows' in platform.system():
                tk=os.popen("dir /b").readlines()
            else:
                # 判断是否有子文件夹
                tk=os.popen("ls -d */").readlines()
                #print 'DDDDDDDDDDDDDD',tk
                
            #print '2'*30
            if tk: 
                for t in tk:
                    if t != "im/\n" and tk != "ThunderDB/\n":
                        data['subfolder']=1
            else:
                data['subfolder']=0
            sz=os.popen("du -hs").readlines()
            temp = None
            #print '3'*30
            for line in sz:
                temp =line.split("\t.\n")
            if temp:
                data['size']=temp[0]
            else:
                data['size']=0
            #print '4'*30,d
            data['foldername']=d
            data['thumb']=''
            #print '5'*30,data
            list.append(data)
    
    #print 'list :------>',list
    os.chdir(root_path)
    return list

def getfilelist(name):
    if name is not 'a':
        path2=FILE_SAVE_PATH
        path3=path2+name
        dirs=os.listdir(path3)
        os.chdir(path3)
    else:
        dirs=os.listdir(FILE_SAVE_PATH)
        path2=FILE_SAVE_PATH
        os.chdir(path2)
    list=[]
    for d in dirs:
        isfile=os.path.isfile(d)
        if isfile:
            list.append(d)
    
    os.chdir(root_path)
    return list

def getdir(path):
    a=0
    if path is not 'a':
        path2=FILE_SAVE_PATH
        path3=path2+path
        dirs=os.listdir(path3)
        os.chdir(path3)
    for d in dirs:
        isdir=os.path.isdir(d)
        if isdir:
            a=1
    os.chdir(root_path)
    return a

def getfiledetailfc(name,path):

    if path is not 'a':
        path2=FILE_SAVE_PATH
        path3=path2+path
        os.chdir(path3)
    else:
        path3=FILE_SAVE_PATH
        os.chdir(path3)
        path="/"

    data={}
    p1,p2=os.path.splitext(name)
    p1 = p1

    obj = Fileinfo_up.objects.filter(name=p1,path=path,ftype=p2,filestatus=0)
    if obj :
        
        obj=obj[0]
        data['id']=obj.id
        data['name']=obj.name
        data['type']=obj.ftype
        data['size']=obj.size
        data['singer']=obj.singer  
        data['last_write_time']=str(obj.lastwritetime)
        data['path']=str(obj.path)
        data['md5']=obj.md5
        data['ablum']=obj.ablum
        data['style']=obj.style
        data['age']=obj.age
        data['duration']=obj.duration
    else:
        
        data['id'] = str(-1)

    os.chdir(root_path)
    return data

# 检查 分页 页码数据
def checkPage(request):
	pageNumber = request.REQUEST.get('pageNumber',1)
	if pageNumber:
		try:
			pageNumber = int(pageNumber)
			if pageNumber<1:
				pageNumber = 1
		except:
			pageNumber = 1
	
	pageSize = request.REQUEST.get('pageSize',10)
	if pageSize:
		try:
			pageSize = int(pageSize)
		except:
			pageSize = 10
	
	return pageNumber,pageSize

# 分页
# return 对象列表
def paginator(request,objs):
    pageNumber,pageSize = checkPage(request)
    p = Paginator(objs,pageSize)
    pageTotal = 0
    try:
        pageTotal = p.num_pages
        #if pageNumber>pageTotal:
        #    pageNumber=1
        
        objs = p.page(pageNumber)
    except PageNotAnInteger:
        objs = p.page(1)
    except EmptyPage:
        return [],pageTotal
        #objs = p.page(1)#paginator.num_pages)

    return objs.object_list,pageTotal

#是否设置密保问题
def isSetQuestion():
    u = User.objects.get(UserName="admin")
    if u:
        #if u.q1.split('_')==2 and u.q2.:
        if u.q1 and u.q2 and u.q3:
            return True
    return False

def getusername(request):
    name = request.COOKIES.get("UserName","")
    #print 'name :',name
    if name:
        user = User.objects.filter(UserName=name)
        if user and user[0].login==1:
            if name == "admin":
                user = user[0]
                if user.q1 and user.q2 and user.q3:
                    return name
        else:
            return ""
    if not name:
        #print 'not name...'
        mname=request.POST.get("username","")
        mpwd = request.POST.get("password","")
        user = User.objects.filter(UserName=mname,Password=mpwd)
        if user:
            try:
                user = user[0]
                user.login = 0
                user.save()
                return user.UserName
            except:
                pass
        deviceid = request.POST.get("deviceid","")
        user = User.objects.filter(deviceid=deviceid)
        if user:
            name = user[0].UserName
            return name
    #return reverse('mini.views.index', args=[]))
    #return redirect('/')
    return name
    #return HttpResponseRedirect("/")
    

def checkLogin(request):
    rs = getusername(request)
    if not rs:
        return HttpResponseRedirect("/")

def getrealname(request):
    realname = request.COOKIES.get("realname","a")
    return realname

# 验证admin
#deviceid，uname，pwd
def isadmin(deviceid='',uname='',pwd=''):
    if deviceid or (uname and pwd):
        user = None
        if deviceid:
            user = User.objects.filter(deviceid=deviceid)
        elif uname and pwd:
            user = User.objects.filter(UserName=uname,Password=pwd)
        if user:
            user = user[0]
            if user.id==1:
                return True
    return False

# 验证  UserName   Password    deviceid
def checkinfo(deviceid='',uname='',pwd=''):
    if deviceid or (uname and pwd):
        user = None
        if deviceid:
            user = User.objects.filter(deviceid=deviceid)
        elif uname and pwd:
            user = User.objects.filter(UserName=uname,Password=pwd)
        if user:
            return True
    return False


#  测试 升级用例


@csrf_exempt
def getversion(request):
    
    data = manage_update("version")
    
    return HttpResponse(json.dumps(data),content_type="application/json")
    
    

# 通信 升级管理服务
def manage_update(todo):
    if todo == "version":
        return {"returncode":"100100000","data":{"id":"1234567890","system_version":"1.0.0","type":"on"}}
    
    return {"returncode":"100100000","data":{"id":"1234567890","system_version":"1.0.0","type":"on"}}
    