#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader,Context
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect,requires_csrf_token,csrf_exempt
from django import forms
from models import User#,FileUpload
import os,json,re,sys,shutil,datetime
from aaa import settings


class UserForm(forms.Form):
	UserName = forms.CharField(label='UserName',max_length=100,widget=forms.TextInput(attrs={'class':"inp"}))
	Password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':"inp"}))


# Create your views here.
#@csrf_protect
#def index(request):
#	return render_to_response('Default/Account/Login.html',context_instance=RequestContext(request))
@csrf_exempt
def index(req):
	if req.method == 'POST':
		#UserName=req.REQUEST.get('UserName','a')
		#Password=req.REQUEST.get('Password','1')
		#user=User.objects.filter(UserName__exact=UserName,Password__exact=Password)
		#if user:
		 #       response = HttpResponseRedirect('Default/Home/Index.html')
                  #      response.set_cookie('UserName',UserName,3600)
                  #      return response
               # else:
                   #     return HttpResponseRedirect('')
		
		uf = UserForm(req.POST)
		if uf.is_valid():
			UserName = uf.cleaned_data['UserName']
			Password = uf.cleaned_data['Password']
			user = User.objects.filter(UserName__exact = UserName,Password__exact=Password)
			if user:
				response = HttpResponseRedirect('default/home/Index.html')
				response.set_cookie('UserName',UserName,3600)
				return response
			else:
				return HttpResponseRedirect('')
	else:
		uf = UserForm()
	return render_to_response('Default/Account/Login.html',{'uf':uf},context_instance=RequestContext(req))

def home(req):
	name=getusername(req)
	return render_to_response("Default/Home/Index.html",{'UserName':name},context_instance=RequestContext(req))

def photo(req):
	name=getusername(req)
	list=getfolderlist()
	return render_to_response("Default/Photo/Index.html",{'UserName':name,'flist':list},context_instance=RequestContext(req))

def photou(req):
	name=getusername(req)
	return render_to_response("Default/Photo/UploadFile.html",context_instance=RequestContext(req))

@csrf_exempt
def photoa(req):
	if req.method == 'POST':
		name=req.REQUEST.get('name','a')
		os.mkdir(r'/home/wenshang/upload/'+name)
		name=getusername(req)
		list=getfolderlist()
	return render_to_response("Default/Photo/Index.html",{'UserName':name,'flist':list},context_instance=RequestContext(req))

@csrf_exempt
def photod(req):
	if req.method == 'POST':
		name=req.REQUEST.get('name','a')
		shutil.rmtree(r'/home/wenshang/upload/'+name)
	data={}
	data['status']='success'
	return HttpResponse(json.dumps(data),content_type="application/json")

@csrf_exempt
def photor(req):
	if req.method == 'POST':
		oname=req.REQUEST.get('oldName','a')
		nname=req.REQUEST.get('newName','a')
		path="/home/wenshang/upload/"
		os.rename(os.path.join(path,oname),os.path.join(path,nname))
	data={} 
	data['status']='success'
	return HttpResponse(json.dumps(data),content_type="application/json")


def getfolderlist():
#	dirs=os.listdir(r'/home/wenshang/upload/')
	dirs=os.listdir(settings.FILE_SAVE_PATH)
	list=[]
	for d in dirs:
		list.append(d)
	return list

def getusername(request):
	name = request.COOKIES.get("UserName","aa")
	return name




#######################################################
###
###     shihl
###
#######################################################
@csrf_exempt
def check_user(request,u):
	user = getusername(request)		
	if user!="aa":
		return render_to_response(u,{"UserName":user},context_instance=RequestContext(request))
	
	response = HttpResponseRedirect('Default/Home/Index.html')
	response.set_cookie('UserName','',3600)
	return response #render_to_response('Default/Account/Login.html',{},context_instance=RequestContext(request))

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
	

@csrf_exempt
def changePwd(request):
	username = getusername(request)
	password = request.POST.get('oldpwd','a')
	new_password = request.POST.get('newpwd','a')
	try:
		result = False
		message = ""
		user = User.objects.filter(UserName = username,Password = password)
		if user:
			user = user[0]
			user.Password = new_password
			user.save()
			message = u"修改成功！"
	except Exception,e:
		print 'eeeeeeee :',e
		message = u"系统异常,请联系管理员!"
	
	data = {'result':'success','message':message}
	return HttpResponse(json.dumps(data))


def playerview(request):
	name = getusername(request)
	return render_to_response("Default/Music/Index.html",{'UserName':name},context_instance=RequestContext(request))

def player(request):
	name = getusername(request)
	return render_to_response("Default/Music/Player.html",{'UserName':name},context_instance=RequestContext(request))

@csrf_exempt
def uploadview(request):
	name = getusername(request)
	return render_to_response("Default/Music/UploadFile.html",{'UserName':name},context_instance=RequestContext(request))

@csrf_exempt
def upphotou(request):
	
	file_path = "%s%s" %(settings.FILE_SAVE_PATH,obj.name)
	
	return UploadFile(request,file_path)
	

def uploadfile(request,file_path):
	
	rs = ""
	try:
		
		obj = request.FILES.get("file",None)
		if obj:
			
			file_name = obj.name
			file_size = "%s kb" %(len(obj)/1024)#len(obj)
			
#			file_path = "%s%s" %(settings.FILE_SAVE_PATH,obj.name)                  #   上传文件存放 URL录
			f = open(file_path,"wb")
			f.write(obj.read())
			f.close()
			
			fileu = FileUpload()
			fileu.fileName = file_name
			fileu.filePath = file_path
			fileu.fileSize = fSize(file_path)
			fileu.userName = request.COOKIES.get("UserName","0000")
			fileu.fileType = 1
			fileu.upload_time = datetime.datetime.now()
			fileu.save()
			rs = "success"
	except Exception,e:
		print "EEEEEEEEE",e
		rs = ""
		
	return HttpResponse(rs)

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

#  下载中心
@csrf_exempt
def download_view(request):
	return check_user(request,"Default/Download/Index.html")

@csrf_exempt
def getDownLoadFileList(request):
	print 'going...'
	if "UserName" in request.COOKIES:
		name = request.COOKIES["UserName"]
	else:
		name = "aa"
	
	status = request.POST.get("status",0)
	pageNumber = request.POST.get("pageNumber",1)
	pageSize = 10
	
	file = ["user_id","user_name","file_id","file_name","file_type","file_size","downloads_status","downloads_rate","downloads_type",
	"downloads_speed","downloads_status_code","downloads_start_time","downloads_again_time","downloads_url"
	]
	
	ss = {"pageTotal":"3","rows":[{"file_id":"1","file_type":"GIF","file_size":"445.76 KB","user_id":"12","user_name":"12","file_name":"001.jpg","downloads_status":"下载中","downloads_rate":"37.5","downloads_type":"HTTP","downloads_speed":"45","downloads_status_code":"0","downloads_start_time":"2015-04-10 04:58:18","downloads_again_time":"2015-04-11 04:58:18","downloads_url":"/mnt/nasfile/Photo/testepic/001.jpg"}]}
	
	data = {"result":"success","data":ss}
	sql = """
	select u.userid,u.UserName,f.fileid,f.file_name,f.file_type,f.file_size,f.downloads_status, from fileinfo f
	left join userinfo u on u.userid = f.userid	
	"""
	
#	data = [["1111","2222","123","100.00%%",u"OK","admin","2015-09-014 16:24:26","12",1,10,3]]
	
	pageNumber = 1
	pageSize = 10
	status = 3
	
	if status == 0:
		pass
	
	
	#print data
	#rs = {"data":json.dumps(data),"result":"success"}
	
	rrr = json.dumps(data)
	print rrr
	print '------------->',type(rrr)
	
	return HttpResponse(json.dumps(data))





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

# 系统文件管理
@csrf_exempt
def system(request):
	return check_user(request,"Default/System/Index.html")


def fSize(p):
	
	size=os.path.getsize(p)
	tmp_size = str(size)
	rs = "1 KB"
	m_s = len(tmp_size)/4
	
	if m_s<= 1:
	    rs = "%.2f KB"% (size/1024.0)
	elif m_s == 2:
	    rs = "%.2f MB"% (size/1024.0/1024.0)
	else:
	    rs = "%.2f GB"% (size/1024.0/1024.0/1024.0)
	
	return rs



