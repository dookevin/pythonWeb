


 function isMousOut(event,nodiv,dsdiv) {
//     var div = document.getElementById(nodiv);
//    var x = event.clientX;
//    var y = event.clientY;
//    var divx1 = div.offsetLeft;
//    var divy1 = div.offsetTop;
//    var divx2 = div.offsetLeft + div.offsetWidth;
//    var divy2 = div.offsetTop + div.offsetHeight;
//    if (x < divx1 || x > divx2 || y < divy1 || y > divy2) {        
//        $(dsdiv).css("display", "none");
//    }
 }



//写入cookies
 function setCookie(name, value, time) {
     var strsec = getsec(time);
     var exp = new Date();
     exp.setTime(exp.getTime() + strsec * 1);
     document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString()+";path=/;";
 }
 //读取cookies 
 function getCookie(name) {
     var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)"); 
     if (arr = document.cookie.match(reg))

         return unescape(arr[2]);
     else
         return null;
 }

 //删除cookies 
 function delCookie(name) {
     var exp = new Date();
     exp.setTime(exp.getTime() - 1);
     var cval = getCookie(name);
     if (cval != null)
         document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
 }



/*\
|*|
|*|  :: cookies.js ::
|*|
|*|  A complete cookies reader/writer framework with full unicode support.
|*|
|*|  https://developer.mozilla.org/en-US/docs/DOM/document.cookie
|*|
|*|  This framework is released under the GNU Public License, version 3 or later.
|*|  http://www.gnu.org/licenses/gpl-3.0-standalone.html
|*|
|*|  Syntaxes:
|*|
|*|  * docCookies.setItem(name, value[, end[, path[, domain[, secure]]]])
|*|  * docCookies.getItem(name)
|*|  * docCookies.removeItem(name[, path], domain)
|*|  * docCookies.hasItem(name)
|*|  * docCookies.keys()
|*|
\*/

var docCookies = {
  getItem: function (sKey) {
    return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
  },
  setItem: function (sKey, sValue, vEnd, sPath, sDomain, bSecure) {
    if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) { return false; }
    var sExpires = "";
    if (vEnd) {
      switch (vEnd.constructor) {
        case Number:
          sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
          break;
        case String:
          sExpires = "; expires=" + vEnd;
          break;
        case Date:
          sExpires = "; expires=" + vEnd.toUTCString();
          break;
      }
    }
    document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
    return true;
  },
  removeItem: function (sKey, sPath, sDomain) {
    if (!sKey || !this.hasItem(sKey)) { return false; }
    document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + ( sDomain ? "; domain=" + sDomain : "") + ( sPath ? "; path=" + sPath : "");
    return true;
  },
  hasItem: function (sKey) {
    return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
  },
  keys: /* optional method: you can safely remove it! */ function () {
    var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
    for (var nIdx = 0; nIdx < aKeys.length; nIdx++) { aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]); }
    return aKeys;
  }
};




 
//这是有设定过期时间的使用示例： 
//s20是代表20秒 
//h是指小时，如12小时则是：h12 
//d是天数，30天则：d30 
 function getsec(str) {     
     var str1 = str.substring(1, str.length) * 1;
     var str2 = str.substring(0, 1);
     if (str2 == "s") {
         return str1 * 1000;
     }
     else if(str2=="m")
     {
         return str1 * 60  * 1000;
     }
     else if (str2 == "h") {
         return str1 * 60 * 60 * 1000;
     }
     else if (str2 == "d") {
         return str1 * 24 * 60 * 60 * 1000;
     }
 }
 //字节转换
 function bytesToSize(bytes) {
     if (bytes === 0) return '0 B';

     var k = 1024;

     sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

     i = Math.floor(Math.log(bytes) / Math.log(k));

     return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
     //toPrecision(3) 后面保留一位小数，如1.0GB                                                                                                                  //return (bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i];
 }

 //----------------------------------------------------------------------------------------------------url 相关  ----------------------------------------------------------------------------------------------------------------------------
//获取url参数
 function getQueryString(name) {
     var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
     var r = window.location.search.substr(1).match(reg);
     if (r != null) return unescape(r[2]); return null;
 }


//url 加密
 function encrypt(str, pwd) {
     if(pwd == null || pwd.length <= 0) {
         alert("Please enter a password with which to encrypt the message.");
         return null;
     }
     var prand = "";
     for(var i=0; i<pwd.length; i++) {
         prand += pwd.charCodeAt(i).toString();
     }
     var sPos = Math.floor(prand.length / 5);
     var mult = parseInt(prand.charAt(sPos) + prand.charAt(sPos*2) + prand.charAt(sPos*3) + prand.charAt(sPos*4) + prand.charAt(sPos*5));
     var incr = Math.ceil(pwd.length / 2);
     var modu = Math.pow(2, 31) - 1;
     if(mult < 2) {
         alert("Algorithm cannot find a suitable hash. Please choose a different password. \nPossible considerations are to choose a more complex or longer password.");
         return null;
     }
     var salt = Math.round(Math.random() * 1000000000) % 100000000;
     prand += salt;
     while(prand.length > 10) {
         prand = (parseInt(prand.substring(0, 10)) + parseInt(prand.substring(10, prand.length))).toString();
     }
     prand = (mult * prand + incr) % modu;
     var enc_chr = "";
     var enc_str = "";
     for(var i=0; i<str.length; i++) {
         enc_chr = parseInt(str.charCodeAt(i) ^ Math.floor((prand / modu) * 255));
         if(enc_chr < 16) {
             enc_str += "0" + enc_chr.toString(16);
         } else enc_str += enc_chr.toString(16);
         prand = (mult * prand + incr) % modu;
     }
     salt = salt.toString(16);
     while(salt.length < 8)salt = "0" + salt;
     enc_str += salt;
     return enc_str;
 }
//url 解密
 function decrypt(str, pwd) {
     if(str == null || str.length < 8) {
         alert("A salt value could not be extracted from the encrypted message because it's length is too short. The message cannot be decrypted.");
         return;
     }
     if(pwd == null || pwd.length <= 0) {
         alert("Please enter a password with which to decrypt the message.");
         return;
     }
     var prand = "";
     for(var i=0; i<pwd.length; i++) {
         prand += pwd.charCodeAt(i).toString();
     }
     var sPos = Math.floor(prand.length / 5);
     var mult = parseInt(prand.charAt(sPos) + prand.charAt(sPos*2) + prand.charAt(sPos*3) + prand.charAt(sPos*4) + prand.charAt(sPos*5));
     var incr = Math.round(pwd.length / 2);
     var modu = Math.pow(2, 31) - 1;
     var salt = parseInt(str.substring(str.length - 8, str.length), 16);
     str = str.substring(0, str.length - 8);
     prand += salt;
     while(prand.length > 10) {
         prand = (parseInt(prand.substring(0, 10)) + parseInt(prand.substring(10, prand.length))).toString();
     }
     prand = (mult * prand + incr) % modu;
     var enc_chr = "";
     var enc_str = "";
     for(var i=0; i<str.length; i+=2) {
         enc_chr = parseInt(parseInt(str.substring(i, i+2), 16) ^ Math.floor((prand / modu) * 255));
         enc_str += String.fromCharCode(enc_chr);
         prand = (mult * prand + incr) % modu;
     }
     return enc_str;
 }
//添加url 参数
 function addUrlPara(name, value) {
     var currentUrl = window.location.href.split('#')[0];
     if (/\?/g.test(currentUrl)) {
         if (/name=[-\w]{4,25}/g.test(currentUrl)) {
           //  alert(2)
             currentUrl = currentUrl.replace(/name=[-\w]{4,25}/g, name + "=" + value);
         } else {
            // currentUrl += "&" + name + "=" + value;
            // alert(window.location.href)
           //  currentUrl=  changeURLPar( window.location.href, name, value);
             setUrlParam(  name, value) ;
             return;
         }
     } else {
         currentUrl += "?" + name + "=" + value;
     }
     if (window.location.href.split('#')[1]) {
         window.location.href = currentUrl + '#' + window.location.href.split('#')[1];
     } else {
         window.location.href = currentUrl;
     }
 }
//修改url参数
 function setUrlParam(para_name, para_value) {
     var strNewUrl = new String();
     var strUrl = new String();
     var url = new String();
     url= window.location.href;
     strUrl = window.location.href;
     //alert(strUrl);
     if (strUrl.indexOf("?") != -1) {
         strUrl = strUrl.substr(strUrl.indexOf("?") + 1);
         //alert(strUrl);
         if (strUrl.toLowerCase().indexOf(para_name.toLowerCase()) == -1) {
             strNewUrl = url + "&" + para_name + "=" + para_value;
             window.location = strNewUrl;
             //return strNewUrl;
         } else {
             var aParam = strUrl.split("&");
             //alert(aParam.length);
             for (var i = 0; i < aParam.length; i++) {
                 if (aParam[i].substr(0, aParam[i].indexOf("=")).toLowerCase() == para_name.toLowerCase()) {
                     aParam[i] = aParam[i].substr(0, aParam[i].indexOf("=")) + "=" + para_value;
                 }
             }
             strNewUrl = url.substr(0, url.indexOf("?") + 1) + aParam.join("&");
             //alert(strNewUrl);
             window.location = strNewUrl;
             //return strNewUrl;
         }
     } else {
         strUrl += "?" + para_name + "=" + para_value;
         //alert(strUrl);
         window.location=strUrl;
     }
 }

 //----------------------------------------------------------------------------------------------------url 相关  ----------------------------------------------------------------------------------------------------------------------------

 $(function () {
     $('.pagination').css('margin-left', -$('.pagination').width() / 2);
 })

 function myBrowser(){
     var userAgent = navigator.userAgent; //取得浏览器的userAgent字符串
     var isIE = userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1; //判断是否IE浏览器
     var IE11 =  userAgent.indexOf("rv:11") > -1;  //
     var isFF = userAgent.indexOf("Firefox") > -1; //判断是否Firefox浏览器
     var isOpera = userAgent.indexOf("OPR") > -1; //判断是否Opera浏览器

     var isLieBao = userAgent.indexOf("LBBROWSER") > -1;  //猪豹
     var isQQ = userAgent.indexOf("QQBrowser") > -1;  //QQ
     var isBaiDu = userAgent.indexOf("BIDUBrowser") > -1;  //百度
     var isSafari = userAgent.indexOf("Safari") > -1; //判断是否Safari浏览器  BIDUBrowser
     var isChrome = userAgent.indexOf("Chrome") > -1; //chrome
     if (isIE) {
         var IE5 = IE55 = IE6 = IE7 = IE8 = IE9 = IE10 = IE11 = false;
         var reIE = new RegExp("MSIE (\\d+\\.\\d+);");
         reIE.test(userAgent);
         var fIEVersion = parseFloat(RegExp["$1"]);
         IE55 = fIEVersion == 5.5;
         IE6 = fIEVersion == 6.0;
         IE7 = fIEVersion == 7.0;
         IE8 = fIEVersion == 8.0;
         IE9 = fIEVersion == 9.0;
         IE10 = fIEVersion == 10.0;
         if (IE55) {
             return "IE55";
         }
         if (IE6) {
             return "IE6";
         }
         if (IE7) {
             return "IE7";
         }
         if (IE8) {
             return "IE8";
         }
         if (IE9) {
             return "IE9";
         }
         if (IE10) {
             return "IE10";
         }
     }//isIE end
     if (IE11) {
         return "IE11";
     }
     else if (isFF) {
         return "FF";
     }
     else if (isOpera) {
         return "Opera";
     }
     else if (isLieBao) {
         return "LieBao";
     }
     else if (isQQ) {
         return "QQ";
     }
     else if (isBaiDu) {
         return "BaiDu";
     }
     else if (isChrome) {
         return "Chrome";
     }
     else if (isSafari) {
         return "Safari";
     }
     else {
         return "NO";
     }
 }