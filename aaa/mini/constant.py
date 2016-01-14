# coding:utf-8

#错误号	英文代码	中文描述	备注

import sys
reload(sys);

sys.setdefaultencoding('utf8');

CONSTANT = {
"img":[0,20],
"100100000":["SUCCESS",u"成功"],
#用户相关	
"100100100":["NAME_OR_PASSWORD_ERROR",u"用户名或密码错误"],
"100100101":["USER_EXIST",u"用户已存在"],
"100100102":["USER_NOT_EXIST",u"用户不存在"],
"100100103":["CREAT_USER_FAILED",u"创建用户失败"],
"100100104":["DELETE_USER_FAILED",u"删除用户失败"],
"100100105":["CHANGE_PASSWORD_FAILED",u"更改密码失败"],
"100100106":["CHANGE_RIGHTS_FAILED",u"更改权限失败"],
"100100107":["VALID_USER",u"合法用户"],
"100100108":["INVALID_USER",u"不合法用户"],
"100100109":["NO_RIGHTS_USER",u"没有权限用户"],
"100100110":["ACL_ERROR",u"权限错误"],
"100100111":["",u"该用户不可创建"],
#用户组群
"100100001":["",u"用户组已存在！"],
"200100002":["",u"admin账号不可以删！"],

#"文件相关	
"100102222":["",u"文件移动失败"],
"100102223":["",u"文件夹移动失败"],
"100102224":["",u"新增下载文件失败"],
"100102225":["",u"下载文件失败"],
"100102226":["",u"停止下载失败"],
"100102227":["",u"删除失败"],
"100102228":["",u"文件上传失败"],
"100102229":["",u"无效URL!"],
"100102230":["",u"文件夹已存在!"],
"100102231":["",u"获取相片时间轴失败!"],
"100102232":["",u"下载已经完成!"],
"100102233":["",u"下载文件已经存在!"],
"100102234":["",u"文件已经存在!"],
"100102235":["",u"退出登录失败!"],
"100102236":["",u"新文件夹名已经存在!"],
"100102237":["",u"目标文件已不存在!"],
"100102238":["",u"获取文件失败!"],
"100102239":["",u"登录状态已失效,请重新登录!"],
"100102240":["",u"无效请求!"],
"100102241":["",u"修改密码失败!"],
"100102242":["",u"旧密码错误!"],
"100102243":["",u"恢复出厂设置失败!"],
"100102244":["",u"后台正在恢复出厂设置!"],
"100102245":["",u"Fuck You!"],
"100102246":["",u"登录已过期!"],
"100102247":["",u"磁盘卷名称!"],
"100102248":["",u"未设置密保,请先登录再设置密保问题!"],
"100102249":["",u"密保答案错误!"],
"100102250":["",u"非admin账户无权限操作!"],
"100102251":["",u"设置密保出错!"],
"100102252":["",u"重置密码失败!"],
"100102253":["",u"密保验证超时!"],

"100100200":["OPEN_FILE_FAILED",u"打开文件失败"],
"100100201":["CLOSE_FILE_FAILED",u"关闭文件失败"],
"100100202":["IS_FILE",u"是否是文件"],
"100100203":["OPEN_DIR_FAILED",u"打开目录失败"],
"100100204":["CLOSE_DIR_FAILED",u"关闭目录失败"],
"100100205":["IS_FOLDER",u"是否是文件夹"],
"100100206":["CREATE_FILE_FAILED",u"创建文件失败"],
"100100207":["READ_FILE_FAILED",u"读取文件失败"],
"100100208":["WRITE_FILE_FAILED",u"写入文件失败"],
"100100209":["DELETE_FILE_FAILED",u"删除文件失败"],
"100100210":["RENAME_FILE_FAILED",u"重命名文件失败"],
"100100211":["CREATE_FOLDER_FAILED",u"创建文件夹失败"],
"100100212":["READ_FOLDER_FAILED",u"读取文件夹失败"],
"100100213":["WRITE_FOLDER_FAILED",u"写入文件夹失败"],
"100100214":["DELETE_FOLDER_FAILED",u"删除文件夹失败"],
"100100215":["RENAME_FOLDER_FAILED",u"重命名文件夹失败"],
"100100216":["GET_FILE_STATUS_FAILED",u"获取文件状态失败"],
"100100217":["FOUND_FILE_FAILED",u"查找文件失败"],
"100100218":["CHANGE_DIR_FAILED",u"更改目录失败"],
"100100219":["UNDEFINED_FILE_TYPE",u"未定义的文件类型"],
"100100220":["UNDEFINED_OPERATE_FILE_OPTION",u"未定义的文件操作选项"],
"100100221":["INVALID_FILE_NAME",u"不合法文件名"],
"100100222":["INVALID_PATH_NAME",u"不合法路径名称"],
"100100223":["COPY_FILE_FAILED",u"拷贝文件失败"],
"100100224":["COPY_FOLDER_FAILED",u"拷贝文件夹失败"],
#"Shell相关			
"100100300":["EXECUTING_SHELL_FAILED",u"执行脚本失败"],
"100100301":["CLOSE_SHELL_FAILED",u"关闭脚本失败"],
"100100302":["SHELL_NO_RETURNv脚本无返回"],
#"Common 相关			
"100100400":["PARAMETER_ERROR",u"参数错误"],
"100100401":["NOT_FOUND",u"未找到"],
"100100402":["FILTER_ERROR",u"过滤错误"],
"100100403":["DATA_FORMAT_ERROR",u"数据格式错误"],
"100100404":["GIVEN_SPACE_ERROR",u"传入空间错误"],
"100100405":["NOT_EQUAL",u"不相等"],
"100100406":["STRING_TRANSFOR_ERROR",u"字符转换错误"],
"100100407":["STRING_SLICE_ERROR",u"字符分割错误"],
"100100408":["REBOOT_ERROR",u"重启失败"],
"100100409":["POWEROFF_ERROR",u"关机失败"],
"100100410":["UPDATE_SYSTEM_ERROR",u"系统升级失败"],
"100100411":["SET_LOCAL_TIME_FAILED",u"设置本地时间失败"],
"100100412":["START_SERVICE_FAILED",u"运行服务失败"],
"100100413":["STOP_SERVICE_FAILED",u"关闭服务失败"],
"100100414":["RESTART_SERVICE_FAILED",u"重启服务失败"],
#"Memory Related			
"100100500":["ALLOCATE_MEMORY_FAILED",u"分配内存空间失败"],
#"MySQL Related			
"100100600":["NO_DEFAULT_PARAMETERS",u"无默认参数"],
"100100601":["NOT_USE_MYSQL",u"未使用mysql"],
"100100602":["CONNECTING_FAILED",u"连接mysql失败"],
"100100603":["INVALID_PATH_TYPE",u"非法路径类型"],
"100100604":["FOUND_MORE_DATA",u"数据非唯一"],
"100100605":["WRONG_SQL_FORMAT",u"sql格式错误"],
"100100606":["SQL_QUERY_FAILED",u"查询失败"],
"100100607":["GET_PATH_INFOR_FAILED",u"获取路径信息失败"],
"100100608":["DATA_EXIST",u"数据已存在"],
#"cJSON Related			
"100100700":["PARSE_JSON_FAILED",u"解析json失败"],
#"Notify Related			
"100100800":["NOTIFY_INIT_ERROR",u"文件通知初始化失败"],
"100100801":["READ_NOTIFY_ERROR",u"读取通知事件失败"],
#"Samba Related			
"100100900":["SAMBA_FOLDER_EXIST",u"文件夹已存在"],
"100100901":["SAMBA_FOLDER_NOT_EXIST",u"文件夹不存在"],
#"NTP Related			
"100101000":["GET_NTP_INFOR_FAILED",u"获取ntp信息失败"],
"100101001":["SET_NTP_INFOR_FAILED",u"设置ntp信息失败"],
"100101002":["CONNECT_NTP_SERVER_FAILED",u"连接ntp服务器失败"],
"100101003":["SELECT_FROM_NTP_FAILED",u"查找ntp信息失败"],
"100101004":["RECEIVE_FROM_NTP_FAILED",u"从服务器获取信息失败"],
"100101005":["SEND_NTP_PACKET_FAILED",u"发送ntp包失败"],
#"Socket Related			
"100101100":["CREATE_SOCKET_FAILED",u"创建套接字失败"],
"100101101":["BIND_SOCKET_FAILED",u"绑定套接字失败"],
"100101102":["GET_HOST_BY_NAME_FAILED",u"获取本机信息失败"],
"100101103":["IP_ADDRESS_ERROR",u"ip地址错误"],
#"Undefined			
"100200000":["UNDEFINED_ERROR",u"未定义错误"],


#system
"100101201":["ERROR",u"请先删除磁盘卷"],
"100101202":["ERROR",u"请先重启设备"],
"100101203":["ERROR",u"磁盘卷创建失败，现有硬盘与原硬盘不符"],
"100101204":["ERROR",u"磁盘卷删除失败"],
"100101205":["ERROR",u"获取磁盘信息错误"],
"100101206":["ERROR",u"磁盘复制失败，磁盘卷未受损"],
"100101207":["ERROR",u"磁盘复制失败，两块磁盘均损坏"],
"100101208":["ERROR",u"磁盘复制失败，新盘容量过小"],
"100101209":["ERROR",u"磁盘添加失败"],
}


IMAGE = (".BMP",".PCX",".TIFF",".GIF",".JPEG",".JPG",".TGA",".EXIF",".FPX",".SVG",".PSD",".CDR",".PCD",".DXF",".UFO",".EPS",".AI",".PNG",".HDRI",".RAW") 
MUSIC = (".MP3",".WMA",".WAV",".MOD",".RA",".CD",".MD",".ASF",".AAC",".Mp3Pro",".VQF",".FLAC",".APE",".MID",".vOGG",".M4A",".AAC+",".AIFF",".AU",".VQF")
VIDEO = (".AVI",".RMVB",".RM",".ASF",".DIVX",".MPG",".MPEG",".MPE",".WMV",".MP4",".MKV",".VOB")
QUESTIONS = {#
    "q1":[u"父亲的姓名?",u"母亲的姓名?",u"身份证号码后四位?"],
    "q2":[u"小学是在哪所学校?",u"中学是在哪所学校?",u"大学是在哪所学校"],
    "q3":[u"您所从事的是什么行业?",u"您公司的名称",u"您的职位名称"],
}

QUESTIONS_LIST = {
    u"父亲的姓名?":0,
    u"母亲的姓名?":1,
    u"身份证号码后四位?":2,
    u"小学是在哪所学校?":0,
    u"中学是在哪所学校?":1,
    u"大学是在哪所学校":2,
    u"您所从事的是什么行业?":0,
    u"您公司的名称":1,
    u"您的职位名称":2
}

def getQuestions(k,i):
    if k:
        return QUESTIONS.get(k)[i]
    return QUESTIONS


#
def getMessage(k='100100000',en='ch'):
    if not k:
        return None
    if en=='ch':
        return CONSTANT.get(k)[1]
    elif en=='en':
        return CONSTANT.get(k)[0]
    return CONSTANT.get(k)[1]


#print getMessage("100100100")
#print getMessage("100100100",'en')












