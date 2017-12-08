function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
var imageCodeId = ""
var preimageCodeId = ""
// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    // 1.生成图片验证码
    imageCodeId = generateUUID();
    // 2.设置验证码标签的src
    var url = '/api/v1.0/imagecode?cur=' + imageCodeId + '&pre=' + preimageCodeId
    // 3.置换验证码图片src链接
    $('.image-code>img').attr('src', url)
    preimageCodeId = imageCodeId
}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // TODO: 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    // 1.组织后端需求的参数
    var params = {
        'mobile': mobile,
        'image_code': imageCode,
        'image_code_id': imageCodeId
    };
    // 2.通过ajax方式向后端发送请求,让后端发送短信验证码
    $.ajax({
        url: "/api/v1.0/sms",
        type: "post",
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        data: JSON.stringify(params),
        success: function (resp) {
            if (resp.errno == "0") {
                // 代表发送成功
                // 倒计时
                var num = 60;
                var t = setInterval(function () {
                    if (num == 1) {
                        // 倒计时完成
                        clearInterval(t);
                        $(".phonecode-a").html("获取验证码")
                    }else {
                        num -= 1;
                        // 更新按钮上的文字内容
                        $(".phonecode-a").html(num + "秒")
                    }
                }, 1000, 60)
            }else {
                $("#phone-code-err span").html(resp.errmsg);
                $("#phone-code-err").show();
                // 将点击按钮的onclick事件函数恢复回去
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
                // 如果错误码是4004，代表验证码错误，重新生成验证码
                if (resp.errno == "4004") {
                    generateImageCode()
                }
            }
        }
    })
}

$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // TODO: 注册的提交(判断参数是否为空)
});
