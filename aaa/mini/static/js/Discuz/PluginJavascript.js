$(function () { 
    function Mychang() {
        var window_w = $(window).width();
        var window_h = $(window).height();
        //外主框定高
        $(".rtgy-box").css("width", window_w - 306 + "px");
        $(".rtgy-box").css("height", window_h - 75 + "px");
        $(".rtgy-box-center").css("width", window_w - 306 + "px");
        $(".rtgy-box-center").css("height", window_h - 116 + "px");
        // left height
        $(".left-panel").css("height", window_h - 94 + "px");
        $(".treelist").css("height", window_h - 127 + "px");  
    };
    Mychang();
    window.onresize = Mychang;
   //上一页
    $(".to-Forward").click(function () {
        history.go(-1);
    })
    //下一页
    $(".to-Backward").click(function () {
        window.history.forward();
    })
    $("#logininfo").click(function () {
        var sta = $(".logininfo .fldiv").css("display");
        if (sta == "none")
            $(".logininfo .fldiv").css("display", "block");
        else
            $(".logininfo .fldiv").css("display", "none");
    });

    //document.onclick = function (event) {
    //    isMousOut(event, "logininfo", ".logininfo .fldiv");
    //}


    $("#chpwd").click(function () {                
        Popup.init('closePopupLayer', 'popupLayer', 'popupLayerBox');
        Popup.popup();
    });
    $("#chabout").click(function () {
        Popup.init('closePopupLayer_about', 'popupLayer_about', 'popupLayerBox_about');
        Popup.popup();
    });

    $("#chout").click(function () {
        if (confirm("您确认注销登录吗？")) {
            $.post("/", function (data, status) {
                if (status == "success")
                    window.location = "/Home/Login";
            });
        }               
    });

    $("#UploadPhoto").click(function () {
        Popup.init('closePopupLayer_Upload', 'popupLayer_Upload', 'popupLayerBox_Upload');
        Popup.popup();
    });

            
             
    $("#submitPwd").click(function () {
        $(".errorMessage").text("");
        var oldpwd = $("#OldPassword").val();
        var newpwd = $("#NewPassword").val();
        var Conpwd = $("#ConfirmPassword").val();
        if (oldpwd.trim().length < 5) {
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

        var datas = { oldpwd: oldpwd, newpwd: newpwd };
        $.post("/Home/ChangePassword", datas, function (result, status) {

            if (status == "success")
                if (result.status == "success") {
                    alert("操作成功!");
                    Popup.closepopup();

                    //成功后重新登录 
                    $.post("/Home/LoginOut", function (data, status) {
                        if (status == "success")
                            window.location = "/Home/Login";
                    });
                }
                else
                    $(".errorMessage").text(result.result);
            else
                $(".errorMessage").text("操作失败!请联系管理员!");
        });
        return false;
    });
});