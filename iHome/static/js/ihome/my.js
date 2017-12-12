function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// TOD: 点击退出按钮时执行的函数
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
    // 页面加载完毕,显示用户信息
    $.ajax({
        url: '/api/v1.0/user',
        type: 'get',
        headers: {
            'X_CSRFToken': getCookie('csrf_token')
        },
        success: function (resp) {
            $('#user-avatar').attr('src', resp.data.avatar_url);
            $('#user-name').html(resp.data.name);
            $('#user-mobile').html(resp.data.mobile)
        }
    })
});
