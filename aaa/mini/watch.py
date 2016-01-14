#coding=utf-8
import socket,httplib,json,urllib,os,hashlib,sys,pyinotify
import MySQLdb
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime,time,chardet,eyed3
from threading import Timer
from multiprocessing import Process 
from PIL import Image

IMAGE = [".BMP",".PCX",".TIFF",".GIF",".JPEG",".JPG",".TGA",".EXIF",".FPX",".SVG",".PSD",".CDR",".PCD",".DXF",".UFO",".EPS",".AI",".PNG",".HDRI",".RAW"]

MUSIC = [".MP3",".WMA",".WAV",".MOD",".RA",".CD",".MD",".ASF",".AAC",".Mp3Pro",".VQF",".FLAC",".APE",".MID","vOGG",".M4A",".AAC+",".AIFF",".AU",".VQF"]

VIDEO = [".AVI",".RMVB",".RM",".ASF",".DIVX",".MPG",".MPEG",".MPE",".WMV",".MP4",".MKV",".VOB"]

class autosyncdb(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        if os.path.isfile(event.pathname):
            p = event.path.split("/")
            print 1
            #if len(p)>3 and "/im/" not in event.path+"/" and ".tmpctcl" not in event.name:
            if len(p)>3 and "/im/" not in event.path+"/":
                filename,ftype=os.path.splitext(event.name)
                size= os.path.getsize(event.pathname)
                type = 0
                print 2
                for e in IMAGE:
                    if e == ftype.upper():
                        type=1
                for e in VIDEO:
                    if e == ftype.upper():
                        type=2
                for e in MUSIC:
                    if e == ftype.upper():
                        type=3
                path=event.path.split("/",3)
                owner = p[3]
                time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                uploadtotaltime = 0
                status = 1
                filestatus = 0
                m=hashlib.md5()
                input =open(event.pathname,'rb')
                while 1:
                    blk = input.read(4096)
                    if not blk:
                        break
                    m.update(blk)
                n=m.hexdigest()
                input.close()
                md5=n
                artist="None"
                album="None"
                style="None"
                age="None"
                duration="None"
                c=eval(repr(filename))
#                if "\u" in c:
#                    fname1 = c.decode("unicode-escape")
#                else :
#                    fname1 = c.decode('gbk')
                fname1=c.decode('utf8')
                c=eval(repr(path[3]))
#                if "\u" in c:
#                    fpath1 = c.decode("unicode-escape")
#                else :
#                    fpath1 = c.decode('gbk')
                fpath1=c.decode('utf8')
                if type==3:
                    artist,album,style,age,duration=muicOption(event.path+"/",filename,ftype)
                if type==1:
                    picOption(event.path+"/",filename,ftype)
                conn=MySQLdb.connect(charset='utf8',host='localhost',user='root',passwd='wenshang',db='mininas',port=3306)
                cur=conn.cursor()
                o="select * from mini_fileinfo_up where name='%s' and path='%s' and ftype='%s'"%(fname1,fpath1+"/",ftype)
                cur.execute(o)
                rpath=cur.fetchone()
                print rpath
                if not rpath:
                    o="insert into mini_fileinfo_up (name,path,size,type,ftype,owner,lastwritetime,uploadedtime,uploadstarttime,timestamp,uploadtotaltime,status,filestatus,singer,ablum,style,age,duration,md5) value ('%s','%s','%s',%d,'%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s','%s','%s','%s','%s')"%(fname1,fpath1+"/",size,type,ftype,owner,str(time1),str(time1),str(time1),time.time(),uploadtotaltime,status,filestatus,artist,album,style,age,duration,md5)
                    cur.execute(o)
                conn.commit()
                cur.close()
                conn.close()

    def process_IN_DELETE(self, event):
        filename,ftype=os.path.splitext(event.name)
        conn=MySQLdb.connect(charset='utf8',host='localhost',user='root',passwd='wenshang',db='mininas',port=3306)
        cur=conn.cursor()
        p=event.path.split("/",3)
        o="delete from mini_fileinfo_up where name='%s' and ftype='%s' and path ='%s'"%(filename,ftype,p[3]+"/")
        cur.execute(o)
        conn.commit()
        cur.close()
        conn.close()
        filename,ftype=os.path.splitext(event.name)
        os.system("rm %s/im/%s1%s"%(event.path,filename,ftype))
        os.system("rm %s/im/%s2%s"%(event.path,filename,ftype))

def fuckmysql(a):
    b=a.split("'")
    c=""
    for i in range(0,len(b)):
        c=c+b[i]
    return c

# 图片缩略图
def picOption(path,name,type):#(p,fileName):#(file_path):
    try:
        p = path
        fname = name
        ftype=type
        file_path = '%s%s%s'%(p,name,ftype)
        img = Image.open(file_path)
        pp = path.split("/")
        path_im = "%sim/" %(p)
        if not os.path.exists(path_im):
            os.makedirs(path_im)
            os.system("chown %s:%s %s"%(pp[3],pp[3],path_im))
            os.system("chmod 755 %s"%path_im)
        fp = "%s%s1%s" %(path_im,name,ftype)
        if not os.path.isfile(fp):
            #print fp,type(fp)
            img.thumbnail((180,180),Image.ANTIALIAS)
            img.save(fp.decode("utf8"))#)
            os.system("chown %s:%s %s"%(pp[3],pp[3],fp))
            os.system("chmod 644 %s"%fp)
        fp = "%s%s2%s" %(path_im,name,ftype)
        if not os.path.isfile(fp):
            #print fp,type(fp)
            img.thumbnail((80,80),Image.ANTIALIAS)
            img.save(fp.decode("utf8"))#)
            os.system("chown %s:%s %s"%(pp[3],pp[3],fp))
            os.system("chmod 644 %s"%fp)
    except Exception,e:
        print "UP Photo :",e

#音频信息
def muicOption(path,name,type):
    try:
        file_path = '%s%s%s' %(path,name,type)
        f = eyed3.load(file_path)
        artist="None"
        album="None"
        style="None"
        age="None"
        duration="None"
        if f.tag:
            try:
                c=eval(repr(f.tag.artist)[1:])
                if "\u" in c:
                    artist = c.decode("unicode-escape")
                else :
                    artist = c.decode('gbk')
            except:pass
                #print f.tag.artist
            try:
                c=eval(repr(f.tag.album)[1:])
                if "\u" in c:
                    album = c.decode("unicode-escape")
                else :
                    album = c.decode('gbk')
            except:pass
            try:
                if f.tag.genre:
                    c=eval(repr(f.tag.genre.name)[1:])
                    if "\u" in c:
                        style = c.decode("unicode-escape")
                    else :
                        style = c.decode('gbk')
            except:pass
            try:
                c=eval(repr(f.tag.recording_date)[1:])
                if "\u" in c:
                    age = c.decode("unicode-escape")
                else :
                    age = c.decode('gbk')
            except:
                pass
            duration = fTime(f.info.time_secs)
    except Exception,e:
        print 'Music ：',e
    return fuckmysql(artist),fuckmysql(album),fuckmysql(style),fuckmysql(age),fuckmysql(duration)

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

#mini_fileinfo_up
conn=MySQLdb.connect(charset='utf8',host='localhost',user='root',passwd='wenshang',db='mininas',port=3306)
cur=conn.cursor()
cur.execute('select * from mini_syssetting where id=1')
rpath=cur.fetchone()
cur.close()
conn.close()
wmg=pyinotify.WatchManager()
mask = pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE 
ptm = autosyncdb()
notifier = pyinotify.Notifier(wmg, ptm)
#o='%sShare'%(rpath[1])
watpath= unicode('/mnt', sys.getfilesystemencoding())
wdd = wmg.add_watch(watpath, mask, rec=True,auto_add=True)
PIDFILE='./pidfile'
notifier.loop(pid_file=PIDFILE)