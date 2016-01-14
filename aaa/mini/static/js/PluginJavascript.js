
 
    function Mychang() {

        var window_w = $(window).width();
        var window_h = $(window).height();
        var footH = $('.footOpertion').height();
        //外主框定高 
        $(".thumbItems").css("height", window_h - 190 - footH + "px");
        $(".rtgy-cont").css("height", window_h - 280 - footH + "px");
        $(".treelist").css("height", window_h - 340 + "px");
        $(".main-left").css("height", window_h - 81 + "px");
        $(".main-right").css("height", window_h - 81 + "px");
        $(".smain").css('height', window_h + 'px');
        $(".left-panel").css("height", window_h - 204 + "px");
        $(".systemRt-cont").css("height", window_h - 90 + "px");
        $(".systemRt-cont2").css("height", window_h - 150 + "px");
        $(".systemRt-cont3").css("height", window_h - 180 + "px");
        $(".systemRt-cont4").css("height", window_h - 164 + "px");
        $(".systemRt-cont5").css("height", window_h - 100 + "px");
        $(".systemRt-cont6").css("height", window_h - 221 + "px");
    };
$(function () {

    Mychang();
    
    window.onresize = Mychang;

    window.onload =  Mychang;

    // window.onload=function(){    // 
    //         alert('window');
    //     }
   //上一页
    $(".to-Forward").click(function () {
        history.go(-1);
    })
    //下一页
    $(".to-Backward").click(function () {
        window.history.forward();
    })


    // $("#logininfo").click(function () {
    //     var sta = $(".logininfo .fldiv").css("display");
    //     if (sta == "none")
    //         $(".logininfo .fldiv").css("display", "block");
    //     else
    //         $(".logininfo .fldiv").css("display", "none");
    // });


    $("#logininfo").toggle(function() {
        $(".logininfo .fldiv").css("display", "block");
    }, function() {
        $(".logininfo .fldiv").css("display", "none");
    });

    document.onclick = function (event) {
        isMousOut(event, "logininfo", ".logininfo .fldiv");
    }


    $("#chpwd").click(function () {                
        Popup.init('closePopupLayer', 'popupLayer', 'popupLayerBox');
        Popup.popup();
    });
    $("#chabout").click(function () {
        $.post("/default/system/checkversion", function(data) {
            if(data.returncode == '100100000'){
                $("#viewAbout").text(data.data.version);
            }else{
                $("#viewAbout").text("获取版本出错!");
            }
        })
        Popup.init('closePopupLayer_about', 'popupLayer_about', 'popupLayerBox_about');
        Popup.popup();
    });

// 注销
    $("#chout").click(function () {
        if (confirm("您确认注销登录吗？")) {
           $.post("/default/logout/", function (data, status) {
               if (status == "success")
                   window.location = "/";
           });
            // window.location = "/";
        }
    });

    //$("#UploadPhoto").click(function () {
    //    Popup.init('closePopupLayer_Upload', 'popupLayer_Upload', 'popupLayerBox_Upload');
    //    Popup.popup();
    //});

// 密码修改
    $("#submitPwd").click(function () {
        $(".errorMessage").text("");
        var oldpwd = $.trim($("#OldPassword").val());
        var newpwd = $.trim($("#NewPassword").val());
        var Conpwd = $.trim($("#ConfirmPassword").val());
        if (oldpwd.trim().length < 5){
                $(".errorMessage").text("旧密码格式不正确");
                return false;
        }
        if (newpwd.trim().length < 5) {
                $(".errorMessage").text("新密码不能小于6位字符");
                return false;
            }
        if (newpwd != Conpwd) {
                $(".errorMessage").text("新密码和确认密码不匹配");
                return false;
            }
        if (newpwd === oldpwd.trim()) {
                $(".errorMessage").text("新密码和旧密码不能相同");
                return false;
            }
        
        var datas = { oldpwd: oldpwd, newpwd: newpwd };
        //$.post("/Home/ChangePassword", datas, function (result, status) {
        $.post("/default/accountc/manage/", datas, function (data, status) {
            alert(data.message);
            if (data.returncode == "100100000"){
                Popup.closepopup();
                window.location = "/";
            }else
                $(".errorMessage").text("操作失败!请联系管理员!");
        },"json");
        return false;
    }) 

// 关闭弹层清空填写项
    $('#closePopupLayer').on('click',function(){
            $("#OldPassword").val('');
            $("#NewPassword").val('');
            $("#ConfirmPassword").val('');
            $(".errorMessage").text('');
     });


            // 解决ie8支持string trim
            String.prototype.trim = function(){ return Trim(this);};
            function LTrim(str)
            {
                var i;
                for(i=0;i<str.length;i++)
                {
                    if(str.charAt(i)!=" "&&str.charAt(i)!=" ")break;
                }
                str=str.substring(i,str.length);
                return str;
            }
            function RTrim(str)
            {
                var i;
                for(i=str.length-1;i>=0;i--)
                {
                    if(str.charAt(i)!=" "&&str.charAt(i)!=" ")break;
                }
                str=str.substring(0,i+1);
                return str;
            }
            function Trim(str)
            {
                return LTrim(RTrim(str));
            }



})
 
function ReSet()
{
   // alert(1);
}

Mychang();