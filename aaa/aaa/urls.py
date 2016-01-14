#coding:utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings,platform
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mini.models import Syssetting
#import debug_toolbar

if 'Windows' in platform.system():
    settings.FILE_SAVE_PATH = "d:/upload/"
else:
    urp=Syssetting.objects.get(id=1)
    settings.FILE_SAVE_PATH=str(urp.uploadrootpath)



urlpatterns = patterns('',
    # examples:
#    url(r'^default/login/infor/', 'mini.views.login_info', name='login_info'), 
    
    url(r'^$', 'mini.views.index', name='index'),   
    #--
    url(r'^default/home/', 'mini.views.home', name='home'),  
    
    # shihl
    url(r'^default/login/infor/', 'mini.views.login_info', name='login_info'), 
    
    url(r'^/default/login/default/home/', 'mini.views.home', name='home'),
    url(r'^default/login/', 'mini.views.index', name='index'), 
    # 注销
    url(r'^default/logout/', 'mini.views.logout', name='logout'),  
    
    # 修改密码
    url(r'^default/accountc/manage/', 'mini.views.changepwd', name='changepwd'),
    # 密保页面
    #url(r'^default/accountc/manage/', 'mini.views.changepwd', name='changepwd'),
    # 密保问题保存
    url(r'^default/accountc/saveanswer/', 'mini.views.setQuestion', name='setQuestion'),
    # 获取 选择的密保问题
    url(r'^default/accountc/checkanswer/', 'mini.views.check_answer', name='check_answer'),
    # 密保问题验证
    url(r'^default/accountc/getquestion/', 'mini.views.getQuestion', name='getQuestion'),
    # 重置密码
    url(r'^default/accountc/resetpwduser/', 'mini.views.reSetPwdUser', name='reSetPwdUser'),# 重置密码普通用户
    url(r'^default/accountc/resetpwd/', 'mini.views.reSetPwd', name='reSetPwd'),# 重置密码
    
    # 注册用户
    url(r'^default/accountc/register/', 'mini.views.register', name='register'),
    
    # 上传
    url(r'^default/uploadfile/upfile', 'mini.views.uploadfile', name='uploadfile'),
    url(r'^default/uploadfile/testupload', 'mini.views.testupload', name='testupload'),
    # 音频 上传
    url(r'^default/music/player/', 'mini.views.player', name='player'),
#    url(r'^default/music/uploadfile/upfile', 'mini.views.uploadmusic', name='uploadmusic'),
    url(r'^default/music/uploadfile/', 'mini.views.uploadview', name='uploadview'),
    
    #  逻辑
    #-- 删除文件
    url(r'^default/music/deletefile', 'mini.views.deletefile', name='deleteusic'),
    url(r'^default/delete/deletefile', 'mini.views.deletefile', name='deleteusic'),
    
    url(r'^default/music/', 'mini.views.playerview', name='playerview'),
    
    # 照片上传
#    url(r'^default/photo/upfile/', 'mini.views.upphotou', name='upphotou'),
    url(r'^default/photo/player/','mini.views.pplayer',name='pplayer'),
    url(r'^default/photo/uploadfile/','mini.views.photou',name='photou'),
    url(r'^default/photoa/','mini.views.photoa',name='photoa'),
    url(r'^default/photod/','mini.views.photod',name='photod'),
    url(r'^default/photor/','mini.views.photor',name='photor'),
    # 重命名文件
    url(r'^default/filerename/','mini.views.filerename',name='filerename'),
    # 移动文件 photom  文件中心
    url(r'^default/photom/','mini.views.photom',name='photom'),
    # 单模块文件移动
    url(r'^default/publicmove/','mini.views.publicmove',name='publicmove'), #PublicMove.html
    url(r'^default/photofo/','mini.views.photofo',name='photofo'),
    # shihl
#    /default/photo/downloadfile?fileName=2015080923485772026.jpg HTTP/1.1" 200 47087
    url(r'^default/photo/downloadfile/','mini.views.getphoto',name='getphoto'),
    url(r'^default/photo/list/','mini.views.photolist',name='photolist'),
    url(r'^default/photo/timeline/','mini.views.phototimeline',name='phototimeline'),
    url(r'^default/photo/timeshaft/','mini.views.timeresponse',name='timeresponse'),
    url(r'^default/photo/gettimephono/','mini.views.gettimephono',name='gettimephono'),
    
    url(r'^default/photo/','mini.views.photo',name='photo'),
    
    #  视频中心 default/video/
    url(r'^default/video/player/', 'mini.views.video_player_view', name='video_player_view'),
    url(r'^default/video/uploadfile/', 'mini.views.video_upload_view', name='video_upload_view'),
    url(r'^default/video/', 'mini.views.video_view', name='video_view'),
    
    #  下载中心 /default/download/  getdownloadfilelist
    url(r'^default/download/getfilelist/','mini.views.getdownfilelist'),
    url(r'^default/download/deldownfile/','mini.views.deldownfile'),
    url(r'^default/download/adddownload/','mini.views.adddownload'),
    url(r'^default/download/startdown/','mini.views.start_down'),
    url(r'^default/download/stopdown/','mini.views.stop_down'),
    url(r'^default/download/downfile/','mini.views.downfile'),
    #-- 逻辑  ### shihl  ###
    url(r'^default/download/downfile','mini.views.downfile',name ='downfile'),
    #-- 
    url(r'^default/download/', 'mini.views.download_view', name='download_view'),
    
    # bt 下载
    url(r'^default/btadddownload/getfilelist/', 'mini.btdown.getfilelist', name='getfilelist'),
    url(r'^default/btadddownload/add/', 'mini.btdown.addBt', name='addBt'),
    url(r'^default/btadddownload/stop/', 'mini.btdown.btStopDown', name='btStopDown'),
    url(r'^default/btadddownload/start/', 'mini.btdown.btStartDown', name='btStartDown'),
    url(r'^default/btadddownload/del/', 'mini.btdown.btDelDown', name='btDelDown'),
    
    url(r'^default/btdownload/uploadfile/', 'mini.views.btdownload_upload_view', name='btdownload_upload_view'),
    url(r'^default/btdownload/', 'mini.views.btdownload_view', name='btdownload_view'),
    # 迅雷下载 default/thunderdownload
    url(r'^default/thunderdownload/uploadfile/', 'mini.views.thunderd_upload_view', name='thunderd_upload_view'),
    #url(r'^default/thunderdownload/movefolder/', 'mini.views.thunderd_movefolder_view', name='thunderd_movefolder_view'),
    url(r'^default/thunderdownload/', 'mini.views.thunderd_view', name='thunderd_view'),
    # 文件管理中心  default/filecenter/index.html
    url(r'^default/filecenter/uploadfileforie/', 'mini.views.uploadfileforie', name='uploadfileforie'),
    url(r'^default/filecenter/movefolder/', 'mini.views.center_movefolder_view', name='center_movefolder_view'),
    url(r'^default/filecenter/uploadfile/', 'mini.views.center_upload_view', name='center_upload_view'),
    #-- 逻辑
    url(r'^default/filecenter/getfolderlist','mini.views.fcentergfdl',name='fcentergfdl'),
    url(r'^default/filecenter/getfilelist','mini.views.getfile',name='getfile'),
    url(r'^default/filecenter/getdirs','mini.views.getdirs',name='getdirs'),
    #--
    url(r'^default/filecenter/foldersearch','mini.views.foldersearch',name='foldersearch'),

    url(r'^default/filecenter/', 'mini.views.filecenter', name='filecenter'),
    #url(r'^default/filecenter/', 'mini.views.fcenter', name='fcenter'),
    
    # 系统文件管理   default/system/index.html
    
    url(r'^default/system/resourcesmonitor', 'mini.views.systemresources', name='systemresources'),
    url(r'^default/system/getcpuinfo', 'mini.views.getcpuinfo', name='getcpuinfo'),
    url(r'^default/system/memoryusage', 'mini.views.memoryusage', name='memoryusage'),
    url(r'^default/system/getmeminfo', 'mini.views.getmeminfo', name='getmeminfo'),
    url(r'^default/system/bandwidth', 'mini.views.bandwidth', name='banwidth'),
    url(r'^default/system/getnetinfo', 'mini.views.getnetinfo', name='getnetinfo'),
    url(r'^default/system/networksetup', 'mini.views.networksetup', name='networksetup'),
    url(r'^default/system/timeareasetup', 'mini.views.timeareasetup', name='timeareasetup'),
    url(r'^default/system/getntptime', 'mini.views.getntptime', name='getntptime'),
    url(r'^default/system/setntptime', 'mini.views.setntptime', name='setntptime'),
    url(r'^default/system/setlocaltime', 'mini.views.setlocaltime', name='setlocaltime'),
    url(r'^default/system/getnowtime', 'mini.views.getnowtime', name='getnowtime'),    
    url(r'^default/system/netset', 'mini.views.netset', name='netset'),
    url(r'^default/system/netget', 'mini.views.netget', name='netget'),
    url(r'^default/system/addtimemachine', 'mini.views.addtimemachine', name='addtimemachine'),

    #  用户
    url(r'^default/system/insideuseredit', 'mini.views.insideuseredit', name='insideuseredit'),
    url(r'^default/system/usergrouplist', 'mini.views.usergrouplist', name='usergrouplist'),
    url(r'^default/system/insideusergroupedit', 'mini.views.insideusergroupedit', name='insideusergroupedit'),
    url(r'^default/system/addusergroup', 'mini.views.addusergroup', name='addusergroup'),
    url(r'^default/system/createnewug', 'mini.views.createnewug', name='createnewug'),
    url(r'^default/system/edituserug', 'mini.views.edituserug', name='edituserug'),
    url(r'^default/system/getuserug', 'mini.views.getuserug', name='getuserug'),
    url(r'^default/system/getallug', 'mini.views.getallug', name='getallug'),
    url(r'^default/system/getuginfo', 'mini.views.getuginfo', name='getuginfo'),
    url(r'^default/system/editug', 'mini.views.editug', name='editug'),
    url(r'^default/system/delug', 'mini.views.delug', name='delug'),
    #url(r'^default/system/getinfo', 'mini.views.getinfo', name='getinfo'),
    url(r'^default/system/syncaddbook', 'mini.views.syncaddbook', name='syncaddbook'),
    url(r'^default/system/getaddbook', 'mini.views.getaddbook', name='getaddbook'),
    url(r'^default/system/deladdbook', 'mini.views.deladdbook', name='deladdbook'),
    url(r'^default/system/getbackuplist', 'mini.views.getbackuplist', name='getbackuplist'),
    url(r'^default/system/userlist', 'mini.views.userlist', name='userlist'),
    url(r'^default/system/register', 'mini.views.register', name='register'),
    url(r'^default/system/adduser', 'mini.views.adduser', name='adduser'),
    url(r'^default/system/addsharefolder', 'mini.views.addsharefolder', name='addsharefolder'),
    # 删除用户
    url(r'^default/system/deluser', 'mini.views.deluser', name='deluser'),
    # 编辑用户
    url(r'^default/system/edituser', 'mini.views.edituser', name='edituser'),
    
    #  共享与权限
    url(r'^default/system/getsflist', 'mini.views.getsflist', name='getsflist'),
    url(r'^default/system/getsfuname', 'mini.views.getsfuname', name='getsfuname'),
    url(r'^default/system/getuseracl', 'mini.views.getuseracl', name='getuseracl'),
    url(r'^default/system/editsharefolder', 'mini.views.editsharefolder', name='editsharefolder'),
    url(r'^default/system/setsharefolder', 'mini.views.setsharefolder', name='setsharefolder'),
    url(r'^default/system/delsharefolder', 'mini.views.delsharefolder', name='delsharefolder'),
    url(r'^default/system/winviewconfig', 'mini.views.winviewconfig', name='winviewconfig'),
    url(r'^default/system/ftpviewconfig', 'mini.views.ftpviewconfig', name='ftpviewconfig'),
    url(r'^default/system/usergroup', 'mini.views.usergroup', name='usergroup'),
    url(r'^default/system/sharefolderedit', 'mini.views.sharefolderedit', name='sharefolderedit'),
    url(r'^default/system/sharefolder', 'mini.views.sharefolder', name='sharefolder'),
    url(r'^default/system/winviewedit', 'mini.views.winviewedit', name='winviewedit'),
    url(r'^default/system/triggerwinview', 'mini.views.triggerwinview', name='triggerwinview'),
    url(r'^default/system/getwinview', 'mini.views.getwinview', name='getwinview'),
    url(r'^default/system/ftpviewedit', 'mini.views.ftpviewedit', name='ftpviewedit'),
    url(r'^default/system/triggerftpview', 'mini.views.triggerftpview', name='triggerftpview'),
    url(r'^default/system/getftpview', 'mini.views.getftpview', name='getftpview'),
    url(r'^default/system/getselfacls', 'mini.views.getselfacls', name='getselfacls'),

    #    存储设置
    url(r'^default/system/diskmanagement', 'mini.views.diskmanagement', name='diskmanagement'),
    url(r'^default/system/diskcouponmanagement', 'mini.views.diskcouponmanagement', name='diskcouponmanagement'),
    
    url(r'^default/sss/playvideo', 'mini.views.playvideo', name='playvideo'),
    url(r'^default/system/upgradepress/', 'mini.views.upgradepress', name='upgradepress'),
    #      磁盘卷
    url(r'^default/system/adddiskcoupon', 'mini.views.adddiskcoupon', name='adddiskcoupon'),
    url(r'^default/system/insideeditdiskcoupon', 'mini.views.insideeditdiskcoupon', name='insideeditdiskcoupon'),
    url(r'^default/system/getraidlist', 'mini.views.getraidlist', name='getraidlist'),
    url(r'^default/system/createraid', 'mini.views.createraid', name='createraid'),
    url(r'^default/system/addraid', 'mini.views.addraid', name='addraid'),
    url(r'^default/system/getrdinfo', 'mini.views.getrdinfo', name='getrdinfo'),
    url(r'^default/system/getnewrd', 'mini.views.getnewrd', name='getnewrd'),
    url(r'^default/system/editraid', 'mini.views.editraid', name='editraid'),
    url(r'^default/system/delraid', 'mini.views.delraid', name='delraid'),
    url(r'^default/system/getraiddes', 'mini.views.getraiddes', name='getraiddes'),
    url(r'^default/system/ifraid', 'mini.views.ifraid', name='ifraid'),
    url(r'^default/system/dlna', 'mini.views.dlna', name='dlna'),
    url(r'^default/system/timemachineedit', 'mini.views.timemachineedit', name='timemachineedit'),
    url(r'^default/system/timemachine', 'mini.views.timemachine', name='timemachine'),
    url(r'^default/system/replacedisk', 'mini.views.replacedisk', name='replacedisk'),
    #      磁盘
    url(r'^default/system/insideeditdisk', 'mini.views.insideeditdisk', name='insideeditdisk'),
    url(r'^default/system/adddisk', 'mini.views.adddisk', name='adddisk'),
    url(r'^default/system/getdiskdetail', 'mini.views.getdiskdetail', name='getdiskdetail'),
    url(r'^default/system/finddisk', 'mini.views.finddisk', name='finddisk'),
    url(r'^default/system/setdisk', 'mini.views.setdisk', name='setdisk'),
    url(r'^default/system/editdisk', 'mini.views.editdisk', name='editdisk'),
    url(r'^default/system/deldisk', 'mini.views.deldisk', name='deldisk'),
    url(r'^default/system/getdiskdes', 'mini.views.getdiskdes', name='getdiskdes'),

    #  迅雷
    url(r'^default/system/thunderset', 'mini.views.thunderset', name='thunderset'),
    url(r'^default/system/thunderkey', 'mini.views.thunderkey', name='thunderkey'),
    url(r'^default/system/thunderunbound', 'mini.views.thunderunbound', name='thunderunbound'),
    url(r'^default/system/getthunderfile','mini.views.fcentergfl',name='getthunderfile'),
    url(r'^default/system/thunderdrename', 'mini.views.thunderdrename', name='thunderdrename'),
    url(r'^default/system/thunderddel', 'mini.views.thunderddel', name='thunderddel'),
    #url(r'^default/system/thunderfdel', 'mini.views.thunderfdel', name='thunderfdel'),
    url(r'^default/system/thunderdown', 'mini.views.thunderdown', name='thunderdown'),
    #url(r'^default/system/thunderfrename', 'mini.views.thunderfrename', name='thunderfrename'),

    #  tm
    url(r'^default/system/tmadd', 'mini.views.tmadd', name='tmadd'),
    url(r'^default/system/tmget', 'mini.views.tmget', name='tmget'),
    url(r'^default/system/tmedit', 'mini.views.tmedit', name='tmedit'),
    url(r'^default/system/tmdel', 'mini.views.tmdel', name='tmdel'),
        
    #    系统设置
    url(r'^default/system/powersupplysetup', 'mini.views.powersupplysetup', name='powersupplysetup'),
    url(r'^default/system/anupgradesetup', 'mini.views.anupgradesetup', name='anupgradesetup'),
    url(r'^default/system/doupgrade', 'mini.views.doupgrade', name='doupgrade'),
    url(r'^default/system/checkversion', 'mini.views.checkversion', name='checkupdate'),
    #url(r'^default/system/checkupdate', 'mini.views.checkupdate', name='checkupdate'),
    url(r'^default/system/dorestore', 'mini.views.dorestore', name='dorestore'),
    url(r'^default/system/restoredefaultsetup', 'mini.views.restoredefaultsetup', name='restoredefaultsetup'),
    url(r'^default/system/rebootorhalt', 'mini.views.rebootorhalt', name='rebootorhalt'),
    
    url(r'^default/system/main', 'mini.views.tmp_main', name='tmp_main'),
    
    url(r'^default/system/', 'mini.views.system', name='system'),
    url(r'^default/diskoperationboot', 'mini.views.diskoperationboot', name='diskoperationboot'),
    
    
    url(r'^admin/', include(admin.site.urls)),
    # 获取升级版本信息 用例
    url(r'^default/getversion/', 'mini.views.getversion', name='getversion'),
    
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{ 'document_root':settings.STATIC_ROOT}),
    
    url(r'^userfiles/(?P<path>.*)$','django.views.static.serve',{ 'document_root':settings.FILE_SAVE_PATH}),

    url(r'^test/(?P<path>.*)$','django.views.static.serve',{ 'document_root':"/tmp/"}),
    
    url(r'^default/tstaticdown','mini.views.downfile'),
    
#    /UserFiles/Photo//%E7%9A%84%E9%A1%B6%E9%A1%B6%E9%A1%B6%E9%A1%B6%E9%A1%B6/2015092105282083727.jpg
#  url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.FILE_UPLOAD_TEMP_DIR})
)
    #urlpatterns += staticfiles_urlpatterns()
#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += patterns('',
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    )