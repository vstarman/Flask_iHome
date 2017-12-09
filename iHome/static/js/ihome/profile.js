function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // TOD: 在页面加载完毕向后端查询用户的信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0'){
            // 将数据填充到页面
            $('#user-avatar').attr("src", resp.data.avatar_url)
            $('#user-name').val(resp.data.name)
        }
    })


    // TOD: 管理上传用户头像表单的行为
    $("#form-avatar").submit(function (e) {
        e.preventDefault()

        // 进行上传
        $(this).ajaxSubmit({
            url: "/api/v1.0/user/avatar",
            type: "post",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "0") {
                    // 代表上传成功
                    $("#user-avatar").attr("src", resp.data.avatar_url)
                }else {
                    alert(resp.errmsg)
                }
            }
        })
    })

    // TOD: 管理用户名修改的逻辑
    $("#form-name").submit(function (e) {
        e.preventDefault()

        var name = $("#user-name").val()
        if (!name) {
            alert("请输入昵称")
            return
        }

        $.ajax({
            url: "/api/v1.0/user/name",
            type: "post",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            contentType: "application/json",
            data: JSON.stringify({"name": name}),
            success: function (resp) {
                if (resp.errno == "0") {
                    $(".error-msg").hide()
                    showSuccessMsg()
                }else {
                    $(".error-msg").show()
                }
            }
        })
    })

})

