function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TOD: 在页面加载完毕之后获取区域信息
    $.get("/api/v1.0/areas", function (resp) {
        if (resp.errno == "0") {
            // 取出数据，遍历添加选项
            // for(var i=0;i<resp.data.areas.length;i++){
            //     var areaId = resp.data.areas[i].aid;
            //     var areaName = resp.data.areas[i].aname;
            //     // 将选项添加到 select 中
            //     $("#area-id").append('<option value="'+ areaId +'">' + areaName + '</option>')
            // }
            // render_template('index.html', data=data)
            var html = template('areas-tmpl', {'areas': resp.data.areas});
            $('#area-id').html(html)
        }
    });

    // TODO: 处理房屋基本信息提交的表单数据



    // TODO: 处理图片表单的数据

})