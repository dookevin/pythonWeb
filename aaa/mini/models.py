#coding:utf-8
from django.db import models
import datetime

file_path = "D:/aaa/mini/static/meta"



# Create your models here.

class User(models.Model):
	UserName = models.CharField(max_length=50,unique=True)
	realname = models.CharField(max_length=50)
	Password = models.CharField(max_length=50,default = "000000000")
	email = models.CharField(max_length=50,null = False)
	deviceid = models.CharField(max_length=100,null = True)
	login = models.IntegerField(default = 0)
	acls = models.CharField(max_length=50,default = "000000000")
	q1 = models.CharField(max_length=200,null = True)   #问题,答案,提示
	q2 = models.CharField(max_length=200,null = True)
	q3 = models.CharField(max_length=200,null = True)
	t = models.IntegerField(null = True)                   # 验证时间
	key_code = models.CharField(max_length=20,null = True) # 验证字符
	def __unicode__(self):
		return self.UserName


class Fileinfo_up(models.Model):
	name = models.CharField(max_length=100,null = False)
	path = models.CharField(max_length=1000,null = False)#models.FileField(upload_to=file_path,null = False)
	size = models.CharField(max_length=30,null = False)
	type = models.IntegerField(null = False)                     # 0:其它 1:图片 2：视频 3：音频  4：全部
	ftype = models.CharField(max_length=20,null = True)         # 后缀  .jpg .zip .mp3
	owner = models.CharField(max_length=50)
	lastwritetime = models.CharField(max_length=20)
	uploadedtime = models.CharField(max_length=20,null = True)
	uploadstarttime = models.CharField(max_length=20)
	timestamp = models.CharField(max_length=20)
	uploadtotaltime = models.IntegerField(default=0)
	status = models.IntegerField(null = False)                   # 0:宸茬粡鏆傚仠 1 涓婁紶瀹屾垚 2 涓婁紶涓?
	filestatus = models.IntegerField(default=0)                  # 0:姝ｅ父浣跨敤 1 鍥炴敹绔?2 鍏跺畠
	singer = models.CharField(max_length=150,null = True)        #	婕斿敱	涓撹緫	娴佹淳	骞翠唤	鑰楁椂
	ablum = models.CharField(max_length=50,null = True)
	style = models.CharField(max_length=50,null = True)
	age = models.CharField(max_length=20,null = True)
	duration = models.CharField(max_length=20,null = True)
	md5 = models.CharField(max_length=200,null = True)

class Fileinfo_down(models.Model):
	name = models.CharField(max_length=100,null = False)
	type = models.IntegerField(null = False)                     #  0 普通URL下载，1 BT种子下载
	ftype = models.CharField(max_length=30,null = False)
	user = models.CharField(max_length=50,null = False)
	url = models.CharField(max_length=1000,null = False)
	dtonk = models.CharField(max_length=30)
	percent = models.CharField(max_length=10,null = False)
	downloadedtime = models.CharField(max_length=20,null = True)
	downloadstarttime = models.CharField(max_length=20,null = True)
	timestamp = models.CharField(max_length=20,null = True)
	downloadtotaltime = models.IntegerField(default=0)
	status = models.IntegerField(default=0)                        # 0:鍏跺畠 1 涓嬭浇瀹屾垚 2 涓嬭浇涓? 3  鏆傚仠
	totalfilesize = models.IntegerField(default=0)

class BtFileinfo_down(models.Model):
	name = models.CharField(max_length=100,null = False)           #文件名
	user = models.CharField(max_length=50,null = False)
	fname = models.CharField(max_length=100)#,null = False)        #种子存放位置的文件夹名
	dname = models.CharField(max_length=200,null = True)           #要下载的种子文件名
	ftype = models.CharField(max_length=30)#,null = False          #种子文件后缀
	torrent = models.CharField(max_length=100,default="")          #种子存放位置 admin/btdownload/bt/
	path = models.CharField(max_length=100,default="")             #下载位置    admin/btdownload/
	hash = models.CharField(max_length=30,default="")              #
	percent = models.CharField(max_length=10)                      # 完成度百分比
	totalSize = models.CharField(max_length=50,default="")         # 原文件大小
	status = models.IntegerField(default=0)                        # 全部  空  下载中 2  展亭   3  已经完成  1  连接中  4  等待中   5
	upsize = models.IntegerField(default=0)                        # 已经下载大小
	resources = models.CharField(max_length=51)                    # 资源数
	requestUp = models.CharField(max_length=20)                    # 已经上传 
	requestDown = models.CharField(max_length=20)                  # 已经下载
	speedUp =  models.CharField(max_length=20)                     # 上传速度
	speedDown =  models.CharField(max_length=20)                   # 下载速度
	downloadedtime = models.CharField(max_length=20)

	
class Ntpinfo(models.Model):
	address = models.IPAddressField()
	port = models.IntegerField(default=0)
	refreshtime = models.IntegerField(default=-1)

class Group(models.Model):
	groupname = models.CharField(max_length=100,unique=True)
	describe = models.CharField(max_length=100)

class Usergroup(models.Model):
	username = models.CharField(max_length=100)
	groupname = models.CharField(max_length=100)
	ingroup = models.IntegerField(default=0)
	groupid = models.IntegerField(default=0)

class Syssetting(models.Model):
	uploadrootpath = models.CharField(max_length=100)
	samba = models.IntegerField(default=0)
	ftp = models.IntegerField(default=0)
	tdport = models.IntegerField(default=0)
	hasraid = models.IntegerField(default=0)

class Zfsinfo(models.Model): #
	name = models.CharField(max_length=100)
	path = models.CharField(max_length=100)
	mountpoint = models.CharField(max_length=100)
	quota = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	type = models.IntegerField(default=0)
	share= models.IntegerField(default=0)
	defaultacl = models.IntegerField(default=0)
	owner = models.CharField(max_length=100,null=True)

class Diskinfo(models.Model):
	name = models.CharField(max_length=100,null=True)
	path = models.CharField(max_length=100,null=True)
	model = models.CharField(max_length=100,null=True)
	rotationrate = models.CharField(max_length=100,null=True)
	vendor = models.CharField(max_length=100,null=True)
	capacity = models.CharField(max_length=100,null=True)
	status= models.CharField(max_length=100,null=True)
	serialshort = models.CharField(max_length=100,null=True)
	bus = models.CharField(max_length=100,null=True)
	serial = models.CharField(max_length=100,null=True)
	describe=models.CharField(max_length=100,null=True)
	type=models.CharField(max_length=100,null=True)

class Raidinfo(models.Model):
	name = models.CharField(max_length=100,null=True)
	raidtype = models.CharField(max_length=100,null=True)
	path = models.CharField(max_length=100,null=True)
	mountpoint = models.CharField(max_length=100,null=True)
	capacity = models.CharField(max_length=100,null=True)
	device = models.CharField(max_length=100,null=True)
	deviceserial= models.CharField(max_length=100,null=True)
	describe=models.CharField(max_length=100,null=True)

class Zpoolinfo(models.Model):
	name = models.CharField(max_length=100,null=True)
	raidtype = models.CharField(max_length=100,null=True)
	path = models.CharField(max_length=100,null=True)
	mountpoint = models.CharField(max_length=100,null=True)
	capacity = models.CharField(max_length=100,null=True)
	device = models.CharField(max_length=100,null=True)
	deviceserial= models.CharField(max_length=100,null=True)
	describe=models.CharField(max_length=100,null=True)

class Sharefuser(models.Model):#
	foldername = models.CharField(max_length=100,null=True)
	sfid = models.IntegerField(default=0)              #0禁止 1可读 2控制
	aviliable = models.IntegerField(default=0)
	option = models.IntegerField(default=0)
	allowguest = models.IntegerField(default=0)

class Addressbook(models.Model):
	deviceid = models.CharField(max_length=100,null=True)
	friendname = models.CharField(max_length=100,null=True)
	email = models.CharField(max_length=100,null=True)
	phonenumber = models.CharField(max_length=100,null=True)
	shihongliang = models.CharField(max_length=200,null=True)

class Tokenbackup(models.Model):
	token = models.CharField(max_length=100,null=True)

class Tmpfileinfo(models.Model):
	path = models.CharField(max_length=255)
	count = models.IntegerField()

#
#Fileinfo_up
#lastwritetime = models.CharField(max_length=20)
#uploadedtime = models.CharField(max_length=20,null = True)
#uploadstarttime = models.CharField(max_length=20)
#timestamp = models.CharField(max_length=20)
#
#
#Fileinfo_down
#downloadedtime = models.CharField(max_length=20,null = True)
#downloadstarttime = models.CharField(max_length=20,null = True)
#timestamp = models.CharField(max_length=20,null = True)
#