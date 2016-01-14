#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # examples:
    url(r'^default/login/infor/', 'mini.views.login_info', name='login_info'), 
    url(r'^$', 'mini.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^default/photou/','mini.views.photou',name='photou'),
    url(r'^default/photoa/','mini.views.photoa',name='photoa'),
    url(r'^default/photod/','mini.views.photod',name='photod'),
    url(r'^default/photor/','mini.views.photor',name='photor'),
    url(r'^default/photo/','mini.views.photo',name='photo'),
    url(r'^default/home/', 'mini.views.home', name='home'),    
    
    # shihl
#    /default/music/player.html
#    /default/music/uploadfile.html
    # 公共login-infor.html
    url(r'^default/login/infor/', 'mini.views.login_info', name='login_info'), 
    # 注销
    url(r'^/default/login/default/home/', 'mini.views.home', name='index'),   
    url(r'^default/login/', 'mini.views.index', name='index'), 
    
    # 修改密码
    url(r'^default/accountc/manage/', 'mini.views.changepwd', name='changepwd'),
    # 音频 上传
    url(r'^default/music/player/', 'mini.views.player', name='player'),
    url(r'^default/music/uploadfile/upfile/', 'mini.views.uploadfile', name='uploadfile'),
    #/default/music/uploadfile/upfile
    # shihl
    url(r'^default/music/uploadfile/', 'mini.views.uploadview', name='uploadview'),
    url(r'^default/music/', 'mini.views.playerview', name='playerview'),
    
    # 图片上传 /default/photou/uploadfile.html
    url(r'^default/photou/upfile/', 'mini.views.upphotou', name='upphotou'),
    
    #  视频中心 default/video/
    url(r'^default/video/player/', 'mini.views.video_player_view', name='video_player_view'),
    url(r'^default/video/uploadfile/', 'mini.views.video_upload_view', name='video_upload_view'),
    url(r'^default/video/', 'mini.views.video_view', name='video_view'),
    
    #  下载中心 /default/download/  getdownloadfilelist
    url(r'^default/download/getfilelist/','mini.views.getdownloadfilelist'),
    url(r'^default/download/', 'mini.views.download_view', name='download_view'),
    
    # bt 下载
    url(r'^default/btdownload/uploadfile/', 'mini.views.btdownload_upload_view', name='btdownload_upload_view'),
    url(r'^default/btdownload/', 'mini.views.btdownload_view', name='btdownload_view'),
    
    # 迅雷下载 default/thunderdownload
    url(r'^default/thunderdownload/uploadfile/', 'mini.views.thunderd_upload_view', name='thunderd_upload_view'),
    url(r'^default/thunderdownload/movefolder/', 'mini.views.thunderd_movefolder_view', name='thunderd_movefolder_view'),
    
    url(r'^default/thunderdownload/', 'mini.views.thunderd_view', name='thunderd_view'),
    
    # 文件管理中心  default/filecenter/index.html
    url(r'^default/filecenter/movefolder/', 'mini.views.center_movefolder_view', name='center_movefolder_view'),
    url(r'^default/filecenter/uploadfile/', 'mini.views.center_upload_view', name='center_upload_view'),
    url(r'^default/filecenter/', 'mini.views.filecenter', name='filecenter'),
    
    # 系统文件管理   default/system/index.html
    
    
    url(r'^default/system/', 'mini.views.system', name='system'),
    
    
    
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{ 'document_root':settings.STATIC_ROOT}),
    
)
    #urlpatterns += staticfiles_urlpatterns()
