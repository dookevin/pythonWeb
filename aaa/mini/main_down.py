# coding:utf-8


import os,sys,datetime,time,urllib2,threading,inspect,ctypes,httplib

from models import User,Fileinfo_down,Fileinfo_up
from aaa.settings import FILE_SAVE_PATH

public_dic = {}
count_down = 5

# 检测 需要下载的项目
def check_dic(uname):
    
    tmp_keys = public_dic.keys()
    tmp_count_dic = len(tmp_keys)
#    print "tmp_count_dic 111:",tmp_count_dic
    
    if tmp_count_dic>0:
        #结束没下载项
        for k in tmp_keys:
            try:
                
                obj = public_dic.get(k)
                if not obj[1]:
                    # 判断线程是否还是活跃状态
                    stop_thread(obj[0])
                    kvalue = public_dic.pop(k)
            
            except Exception,e:
                print 'clear public_dic err :',e
    
    tmp_count_dic = len(public_dic.keys())
#    print "tmp_count_dic 222:",tmp_count_dic
    need_dow = count_down - tmp_count_dic
#    print "need_dow :",need_dow
    
    #把需要下载在排队的
    if need_dow>0:
        try:
            
            dfs = Fileinfo_down.objects.filter(status=2)
            if uname:
                dfs.filter(user = uname)
            
            dfs = dfs[0:need_dow]
#            print 'down file count :',len(dfs),dfs
            for df in dfs:
                
                thread = threading.Thread(target=startDown,args=(df,))
                public_dic[df.id] = [thread,True]
                thread.start()
                
        except Exception,e:
            print 'check public err :',e
            
#        print 'public_dic :',public_dic


#启动一个下载
def start_Down(df):
    
    if df:
        
        df.status = 2
        df.downloadedtime = str(time.time())
        
        try:
            df.save()
            
        except Exception,e:
            print "start new down :",e
        
        check_dic(df.user)

#停止下载
def stopDown(df):
    
#    try:
    df.status = 3

    obj = public_dic.get(df.id)
#    print 'obj :',obj
    if obj:
        if obj[1]:
#            print public_dic,'------->',df.id
            public_dic[df.id][1] = False
            stop_thread(obj[0])
#            print 'sssssssssssssssssss'
#    print 'F'*10
    if df:
        
        df.downloadtotaltime = int(float(df.downloadtotaltime)) + int(time.time()-int(float(df.downloadedtime)))
#        df.downloadedtime = str(time.time())
        df.save()
    check_dic(df.user)
#    except Exception,e:
#        
#        print 'stop down err :',e
# 删除一个下载
def dropDown(df):
    
    try:
        uname = ""
        obj = public_dic.get(df.id)
        #    print 'obj :',obj
        if obj:
            if obj[1]:
        #            print public_dic,'------->',df.id
                public_dic[df.id][1] = False
                stop_thread(obj[0])
                uname = df.user
        
        tmp_path = FILE_SAVE_PATH+df.user+"/download/"+df.dtonk
        fnames = [ "%s_%d" %(tmp_path,i) for i in xrange(0,5)]
        fnames.append(FILE_SAVE_PATH+df.user+"/download/"+df.name+df.ftype)
        for f in fnames:
            if os.path.isfile(f):
                os.remove(f)
        
        if df:
            df.delete()
        
        check_dic(uname)
        
        
    except Exception,e:
        print 'dorp down file err :',
    
    check_dic(uname)

# 根据URL 获取文件大小
def getUrlFileSize(url): 
    size = 0
    try:
#        print 'c'*30
        res = urllib2.urlopen(url)
        headers =res.info().headers #heaer info array
#        print ">>>>>>", type(headers),headers
        for o in headers:
            if "Content-Length" in o:
                size = int(o.split(":")[1].strip())
                break
        return size
    except Exception,e:
        print 'get file size error:',e
    
    return size


# 获取 下载文件名
def getDowFileName(URL):
    
    class HeadRequest(urllib2.Request):
        def get_method(self):
            return "HEAD"
    
    try:
        if URL[0:4].upper()!="HTTP":
            return 0,0
        hr = HeadRequest(URL)
        res = urllib2.urlopen(hr)
        headers = dict(res.headers)
        size = int(headers.get('content-length', 0))
        
        name = None
        
        if headers.has_key('content-disposition'):
            name = headers['content-disposition'].split('filename=')[1]
            if name[0] == '"' or name[0] == "'":
                name = name[1:-1]
        #print name,size
        if name:
            return name,size
        
        t,url,endurl = strfurl(URL)
        #print t,url,endurl
        conn = httplib.HTTPConnection(url)
        conn.request("GET",endurl)
        
        r = conn.getresponse()
        
        response_status = r.status
        rs_url = ""
        #print "response_status :",response_status
        if response_status == 302:
            objs = r.getheaders()
            for o in objs:
                if o[0] == 'location':
                    rs_url = o[1]
                    break
            
        elif response_status == 200:
            rs_url = t+url+endurl
        
        file_name = rs_url.split('/')[-1].split('?')[0]
        
        return file_name,size
    except Exception,e:
        print 'get down file name ',e
    
    return 0,0
    


def strfurl(url):
    
    tmp = url.split("//")
    tmp2 = "".join(tmp[1:]).split("/")
    u2 = tmp2[0]
    u3 = "/"+"/".join(tmp2[1:])
    
    return tmp[0]+"//",u2,u3


# 退出进程
def kill_thread(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

# 停止线程公共入口
def stop_thread(thread):
    try:
        kill_thread(thread.ident, SystemExit)
    except Exception,e:
        print 'public stop thread err :',e


class Download(threading.Thread):  
    """docstring for Download"""  
    def __init__(self, threadname,url,ranges,filename,df):  
        super(Download, self).__init__()  
        self.threadname = threadname  
        self.url = url  
        self.ranges = ranges  
        self.filename = filename  
        self.downloadsize = 0
        self.df = df
        
    def run(self):  
        try:  
            self.downloadsize = os.path.getsize( self.filename )  
            print 'self down size :',self.downloadsize
        except OSError:
            self.downloadsize = 0  
        
        self.startpoint = self.ranges[0] +self.downloadsize  
#        print 'thread_%s downloading from %d to %d' %(self.threadname,self.startpoint,self.ranges[1])  
        
        try:  
            request = urllib2.Request(self.url)  
            request.add_header("Range", "bytes=%d-%d" % (self.startpoint, self.ranges[1]))              
            response = urllib2.urlopen(request)  
            self.oneTimeSize = 16384 #16kByte/time  
            data = response.read(self.oneTimeSize)  
            while data:
                if not isGo(self.df):
                    break
                handle = open(self.filename,'ab+')  
                handle.write(data)  
                handle.close()  
                
                self.downloadsize += len(data)   
                data = response.read(self.oneTimeSize)              
        except Exception, e:  
            print 'download error:',e  
            return False  
        return True 

# 判断是否断掉下载
def isGo(df):
    try:
        isgo = public_dic.get(df.id)[1]
        return isgo
    except:
        pass
    
    return False


def splitBlock(totalsize,blocks):  
    blocksize = totalsize/blocks  
    ranges = []  
    for x in xrange(0,blocks-1):  
        ranges.append([x*blocksize,x*blocksize+blocksize-1])  
    ranges.append([blocksize*(blocks-1),totalsize]) #deal with last block   
    
    return ranges

def islive(tasks):  
    for task in tasks:  
        if task.isAlive():  
            return True  
    return False  

#下载入口
def startDown(df,blocks=1):
#    print 'start down...',df.id
    url = df.url
    size = df.totalfilesize
    ranges = splitBlock(size,blocks)
    
    tmp_path = "thread"
    if df.dtonk:
        tmp_path = FILE_SAVE_PATH+df.user+"/download/"+df.dtonk
    else:
        tmp_path = FILE_SAVE_PATH+df.user+"/download/"+datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    filename = [ "%s_%d" %(tmp_path,i) for i in xrange(0, blocks) ]  
#    print filename
    tasks = []
    for x in xrange(0,blocks):
        t = Download(x,url,ranges[x],filename[x],df)
        t.setDaemon(True) 
        t.start()
        tasks.append(t)  
    
    time.sleep(2)  
    while islive(tasks) :
        if not isGo(df):
            break
        
        downloaded = sum([task.downloadsize for task in tasks] )  
        process = downloaded/float(size)*100
#        show = u'\r Completed:%.2f%%' % (process)
#        sys.stdout.write(show)  
        sys.stdout.flush() 
        df.percent = '%.2f%%' %(process)
        df.save()
        time.sleep( 0.5 )  
    
    output = FILE_SAVE_PATH + df.user + "/download/" + df.name + df.ftype
    filehandle = open( output, 'wb+' )  
    for i in filename:
        if not isGo(df):
            return
        
        f = open( i, 'rb' )  
        filehandle.write( f.read() )  
        f.close()  
        try:  
            os.remove(i)  
            pass  
        except:  
            pass  
    
    df.percent = '100.00%%' %()
    df.status = 1
#    print "1111 :",df.downloadtotaltime
    
    df.downloadtotaltime = int(float(df.downloadtotaltime) + int(time.time()-int(float(df.downloadedtime))))
    df.downloadedtime = str(time.time())    
    
    df.save()
    
    filehandle.close()
    if public_dic.get(df.id):
        public_dic.pop(df.id)
    
    # 存放文件重新
    try:
        fu = Fileinfo_up()
        fu.name = df.name
        fu.path = "%s/download/" %(df.user)
        p = "%s%s/%s%s" %(FILE_SAVE_PATH,fu.path,df.name,df.ftype)
        fu.size = os.path.getsize(p)#fSize(p)#df.totalfilesize
        fu.type = 0
        fu.ftype = df.ftype
        fu.owner = df.user
        fu.status = 1
        ss = df.downloadstarttime
        fu.uploadstarttime = "%s-%s-%s %s:%s:%s" %(ss[0:4],ss[4:6],ss[6:8],ss[8:10],ss[10:12],ss[12:14])
        fu.userid = User.objects.filter(UserName=df.user)[0]
        fu.save()
        
    except Exception,e:
        print 'ddddddddddddd :',e
        pass
    
def fSize(p):
	if not p:
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

#if __name__ == '__main__':  
#    url = ['http://w.x.baidu.com/alading/anquan_soft_down_all/13442']
#    output = 'SafariSetup.exe'  
#    startDown( url, output) 





