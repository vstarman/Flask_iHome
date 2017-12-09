function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// TODO: 点击退出按钮时执行的函数
function logout() {
    $.ajax({
        url: '/api/v1.0/session',
        type: 'delete',
        headers: {
            'X_CSRFToken': getCookie('csrf_token')
        },
        success: function (resp) {
            location.href = '/index.html'
        }
    })
}

$(document).ready(function(){

    // TODO: 在页面加载完毕之后去加载个人信息

});
