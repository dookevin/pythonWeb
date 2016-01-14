#coding:utf-8

from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect,requires_csrf_token,csrf_exempt
from models import User,Fileinfo_up,BtFileinfo_down,Syssetting
import os,json,re,sys,shutil,datetime,atexit,time,pexpect,urllib2,multiprocessing
import psutil,struct,ntplib,re,platform,random
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from aaa.settings import FILE_SAVE_PATH
from constant import getMessage as get_message 
import libtorrent as lt
import time,signal
from django.db import connection
import ctypes,subprocess


import os,sys,datetime,time,urllib2,threading,inspect,ctypes

from models import User,Fileinfo_up,BtFileinfo_down,Syssetting
from aaa.settings import FILE_SAVE_PATH


root_path = "/mnt/"
if 'Windows' in platform.system():
    FILE_SAVE_PATH = "d:/upload/"
    root_path = FILE_SAVE_PATH
else:
    urp=Syssetting.objects.get(id=1)
    FILE_SAVE_PATH=str(urp.uploadrootpath)
    root_path = "/mnt/"



public_dic_bt = {}
count_down_bt = 1


port_lsit = [[6881,6891],]



# 检测 需要下载的项目
def check_bt_dic(uname):
    
    tmp_keys = public_dic_bt.keys()
    tmp_count_dic = len(tmp_keys)
    #print "tmp_count_dic 111:",tmp_count_dic
    
    if tmp_count_dic>0:
        #结束没下载项
        for k in tmp_keys:
            try:
                
                obj = public_dic_bt.get(k)
                #print 'AAAAAAAAA :',obj[1]
                if not obj[1]:
                    # 判断线程是否还是活跃状态
                    stop_thread(obj[0])
                    kvalue = public_dic_bt.pop(k)
            
            except Exception,e:
                print 'end public_dic_bt err :',e
    
    tmp_count_dic = len(public_dic_bt.keys())
    need_dow = count_down_bt - tmp_count_dic
    
    #把需要下载在排队的
    if need_dow>0:
        try:
            
            dfs = BtFileinfo_down.objects.filter(status__in=(2,4,5))
            if uname:
                dfs.filter(user = uname)
            
            bts = dfs[0:need_dow]
#            print 'down file count :',len(dfs),dfs
            for b in bts:
                
                thread = threading.Thread(target=downBTFile,args=(b,))
                public_dic_bt[b.id] = [thread,True]
                thread.start()
        
        except Exception,e:
            print 'check public err :',e
            
#        print 'public_dic :',public_dic



# 分析文件
def downBTFile(b):
    
    ses = lt.session()
    ses.listen_on(port_lsit[0][0],port_lsit[0][1])
    p = "%s%s%s"%(FILE_SAVE_PATH,b.torrent,b.name)
    s = "%s%s"%(FILE_SAVE_PATH,b.path)
    e = lt.bdecode(open(p, 'rb').read())
    info = lt.torrent_info(e)
    #print 'PPPPPPPPPPP :',p
    #print 'ssssssssssp :',s
    params = {'save_path': str(s),'storage_mode': lt.storage_mode_t.storage_mode_sparse,'ti': info }#,lt.storage_mode_t(2)
    
    h = ses.add_torrent(params)
    params = {'save_path': 'ttt',
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,#lt.storage_mode_t(2),
        'ti': info }
    
    while (not h.is_seed()) and public_dic_bt.get(b.id)[1]:
        s = h.status()
        #print 'b'*30
        
        try:
            if s.state ==3: #载中的返回值
                
                b.resources = "%s/%s" %(s.num_pieces,len(s.pieces))
                b.requestUp = s.total_upload
                b.requestDown = s.total_download
                b.speedUp = '%.2f kB/s' %(s.upload_rate / 1000)
                b.speedDown = '%.2f kb/s' %(s.download_rate / 1000)
                b.percent = '%.2f%%'%(s.progress * 100)
                b.status = 2
                b.save()
                #print '====>',b.speedDown
            else:
                
                b.speedUp = '-'
                b.speedDown = '-'
                b.status = 4
                b.save()
            time.sleep(1)
        except:pass
        time.sleep(1)
    
    #print 'down over...'
    
    b.status = 1
    b.speedUp = '-'
    b.speedDown = '-'
    b.requestDown = '-'
    b.requestUp = '-'
    b.percent = "100%"
    b.resources = "-"
    b.save()
    
    #  存放 Fileinfo_up
    bfp = "%s%s/" %(b.path,b.fname)
    fp = "%s%s" %(FILE_SAVE_PATH,bfp)
    lfs = os.listdir(fp)
    for f in lfs:
        try:
            
            #print '0'*30,f.decode('utf8')
            name,ftype = os.path.splitext(f)
            
            fu = Fileinfo_up()
            
            fu.name = name
            fu.ftype = ftype
            fu.size = b.totalSize
            fu.type = 0
            fu.owner = b.user
            fu.status = 1
            fu.path = bfp
            tmp_tiem = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fu.lastwritetime = tmp_tiem
            fu.uploadstarttime = tmp_tiem
            fu.timestamp = 0
            fu.userid = User.objects.get(UserName=b.user)
            
            fu.save()
            
        except Exception,e:
            print 'ddddddddddddd :',e
            pass
    

#全部  空  下载中 2  展亭   3  已经完成  1  连接中  4  等待中   5

# 开始下载
def startBT(o):
    #print '===== o.status >>>>',o.status
    if o.status !=1:
        obj = public_dic_bt.get(o.id)
        if obj:
            check_bt_dic(o.user)
            return
        
        o.speedUp = '-'
        o.speedDown = '-'
        o.status = 5
        o.save()
        
        check_bt_dic(o.user)
        


# 停止下载
def stopBT(o):
    #print 'A'*30
    if o.status !=1:
        #try:
        obj = public_dic_bt.get(o.id)
        if obj:
            #print 'tttttt :',obj
            t = obj[0]
#            if t.isAlive():
#                #t.terminate()
#                t.join()
            public_dic_bt[o.id][1]=False
            #print 'TTTTTT :',obj
            stop_thread(obj[0])
            #print '0000000000000'
        
        #print '11111'
        o.status = 3
        o.speedUp = '-'
        o.speedDown = '-'
        o.save()
        #print '33333'
        check_bt_dic(o.user)
        #print '44444+'
#        except Exception,e:
#            print 'stop down bt :',e
#        finally:
#            pass
#    check_bt_dic(o.user)

# 删除下载  
def deleteBT(o):
    try:
        obj = public_dic_bt.get(o.id)
        if obj:
            public_dic_bt[o.id] = [obj[0],False]
            stop_thread(obj[0])
            public_dic_bt.pop(o.id)
        
        try:
            
            os.chdir(root_path)
            #print "o.path :",o.path
            #删除下载
            if o.status !=1:
                
                file_path = "%s%s%s" %(FILE_SAVE_PATH,o.path,o.fname)#.decode("utf8")
                #print 'sssssssssssssss',file_path
                if os.path.exists(file_path):
                    #print "shutil.rmtree :",FILE_SAVE_PATH,'+',o.user,'+',"/",'+',o.torrent+o.name
                    shutil.rmtree(file_path)#FILE_SAVE_PATH+o.torrent+o.name)
            #删除种子
            file_bt = ("%s%s%s" %(FILE_SAVE_PATH,o.torrent,o.name)).decode("utf8")
            #print 'ffffffffffffff',file_bt
            if os.path.isfile(file_bt):
                os.remove(file_bt)
        except:pass
        
        if o:
            o.delete()
        
        check_bt_dic(o.user)
        
    except Exception,e:
        print 'del bt error ...',e
    finally:
        pass


# 退出进程
def kill_thread(tid, exctype):
    #print 'kkkkkkkkkkkkkkkkkkkkkkk'
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    #print '-------->',ctypes.py_object(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    #print 'kokokokokokokkokokokok'

# 停止线程公共入口
def stop_thread(thread):
    try:
        #raise_exc(SystemExit)
        
        #
        kill_thread(thread.ident, SystemExit)
    except Exception,e:
        print 'public stop thread err :',e



# 新建bt
@csrf_exempt
def addBt(request):
    rs = "100102224"
    username = getusername(request)
    if not username:
        rs = "100102239"
        data = {"returncode":rs,"message":get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    
    bt_path = "%s/btdownload/bt/" %(username)
    bt_down_path = "%s/btdownload/" %(username)
    os.chdir(root_path)
    try:
        
#        if not os.path.exists(bt_path):
#            #print 'create dir :',bt_path
#            os.makedirs(bt_path)
        
        obj = request.FILES.get("file",None)
        
        fileName = obj.name
        #print "fileName :",fileName
        
        b = BtFileinfo_down.objects.filter(name=fileName,user=username)
        
        if b:
            
            godown = request.POST.get("godown",None)
            if not godown:
                rs = "100102233"
                data = {'returncode':rs,"message":get_message(rs)}
                return HttpResponse(json.dumps(data))
            
            if godown == "111": # 重新下
                deleteBT(b)
            
            else:# 继续
                
                data = {"returncode":rs,"message":get_message(rs)}
                return HttpResponse(json.dumps(data),content_type="application/json") 
            
        
        file_path = (u"%s%s%s" %(FILE_SAVE_PATH,bt_path,fileName)).decode("utf8")
        
        if not os.path.exists(FILE_SAVE_PATH+bt_path):
            os.makedirs(FILE_SAVE_PATH+bt_path)
        
        f = open(file_path,"wb+")
        f.write(obj.read())
        f.close()
        
        bt = BtFileinfo_down()
        info = lt.torrent_info(file_path)
#        files = info.files()
#        if files :
#            #print "FFFFFFFFFFFFF :",files
#            f = files[0]
#            #print '-------------->',f.path.split('/')
#            bt.dname = f.path.split('/')[-1]
        
        bt.name = fileName
        bt.fname = info.name()
        bt.user = username
        bt.torrent = bt_path
        bt.path = bt_down_path
        bt.percent = ""
        #bt.upsize = 0
        
        bt.resources = "/"
        bt.requestUp = "-"
        bt.requestDown = "-"
        bt.speedUp = "-"
        bt.speedDown = "-"
        
        bt.status = 2
        #bt.hash = info.info_hash()
        #print 'info.total_size():',info.total_size()
        bt.totalSize = info.total_size()
        bt.downloadedtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bt.save()
        
        startBT(bt)
        
        rs = "100100000"
    except Exception,e:#add new bt err... list index out of range
        print 'add new bt err...',e
    
    data = {"returncode":rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")
    


def getObjs(request):
    objs = []
    
    bfids = request.POST.get("bfids","")
    
    if bfids:
        bfids = bfids.split(",")
    else:
        rs = "100102240"
        data = {"returncode":rs,"message":get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    
    objs = BtFileinfo_down.objects.filter(id__in=bfids)
    
    if not objs:
        rs = "100102237"
        data = {"returncode":rs,"message":get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")
    
    return objs


# 开始 下载
@csrf_exempt
def btStartDown(request):
    rs = ""
    try:
        objs = getObjs(request)
        for o in objs:
            startBT(o)
        rs = "100100000"
    except Exception,e:
        print e
    
    data = {"returncode":rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")


#暂停 下载
@csrf_exempt
def btStopDown(request):
    rs = ""
    try:
        objs = getObjs(request)
        #print '------>',objs
        for o in objs:
            #print 'OOOOOOO :',o.id
            if o.status not in(1,3):
                stopBT(o)
        rs = "100100000"
    except Exception,e:
        print e
    
    data = {"returncode":rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")


# 删除 下载
@csrf_exempt
def btDelDown(request):
    
    rs = "100102227"
    try:
        objs = getObjs(request)
        for o in objs:
            deleteBT(o)
        rs = "100100000"
    except Exception,e:
        print e
    
    data = {"returncode":rs,"message":get_message(rs)}
    return HttpResponse(json.dumps(data),content_type="application/json")

#全部  空,下载中:2,暂停:3,已经完成:1,连接中:4,查找资源:5

# 文件列表
@csrf_exempt
def getfilelist(request):
#    ks = public_dic_bt.keys()
#    for k in ks:
#        print "public_dic_bt :",public_dic_bt.get(k)
    
    user = getusername(request)
    if not user:
        rs = "100102246"
        data = {'returncode':rs,'message':get_message(rs)}
        return HttpResponse(json.dumps(data),content_type="application/json")    
    
    rs = "100102238"
    ftype = request.POST.get("status",'')
    keyword = request.POST.get("keyword",'')
    dfs = BtFileinfo_down.objects.filter(user=user)
    #print 'DDDFFF :',dfs
    if dfs and ftype:
        dfs = dfs.filter(status = ftype)
    if keyword:
        dfs = dfs.filter(name__icontains=keyword)
    try:
        
        dfs,pageTotal = paginator(request,dfs)
        objs = format_obj(dfs)
        rs = "100100000"
    except Exception,e:
        print 'get bt down center file err :',e
        return formatResponse()
    
    return formatResponse(objs,pageTotal)


def updataBySQL(sql):
    try:
        
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.close()
    except Exception,e:
        print 'Update SQL :',e
    
def findBtF(sql):
    rows = []
    try:
        
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception,e:
        print 'SQL :',e
    if rows:
        return rows[0]
    return rows

tmp_status = {
    1:u"已经完成",
    2:u"下载中",
    3:u"暂停",
    4:u"连接中",
    5:u"等待中",
}

def format_obj(objs,type=1):
    fobjs = []
    for obj in objs:
        data = {}
        data['id'] = obj.id
        data['name'] = obj.name              #文件名
        data['percent'] = obj.percent        #完成度百分比
        data['totalSize'] = obj.totalSize    #原文件大小
        data['status'] = tmp_status.get(obj.status)          #状态 (#全部  空,下载中:2,暂停:3,已经完成:1,连接中:4,查找资源:5)
        data['upsize'] = obj.upsize          #已经下载大小
        data['resources'] = obj.resources    #资源数
        data['requestUp'] = obj.requestUp    #已经上传 
        data['requestDown'] = obj.requestDown#已经下载
        data['speedUp'] = obj.speedUp        #上传速度
        data['speedDown'] = obj.speedDown    #载速度
        
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
    return HttpResponse(json.dumps(data),content_type="application/json")


# 检查 分页 页码数据
def checkPage(request):
    pageNumber = request.REQUEST.get('pageNumber',1)
    if pageNumber:
        #print "pageNumber :",pageNumber
        try:
            pageNumber = int(pageNumber)
            if pageNumber<1:
                pageNumber = 1
        except Exception,e:
            print e
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
    #print "pageNumber,pageSize :",pageNumber,pageSize
    p = Paginator(objs,pageSize)
    pageTotal = 0
    try:
        pageTotal = p.num_pages
        objs = p.page(pageNumber)
    except PageNotAnInteger:
        objs = p.page(1)
    except EmptyPage:
        objs = p.page(paginator.num_pages)

    return objs.object_list,pageTotal


def getusername(request):
    name = request.COOKIES.get("UserName",None)
    if not name:
        
        deviceid = request.POST.get("deviceid","")
        user = User.objects.filter(deviceid=deviceid)
        if user:
            name = user[0].UserName
            return name
    
    if name:
        return name
    
    return ""









