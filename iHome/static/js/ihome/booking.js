function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    // TOD: 判断用户是否登录
    $.get('/api/v1.0/session', function(resp){
       if (resp.errno == '0'){
            if (!(resp.data.user_name && resp.data.user_id)){
                location.href = '/login.html'
            }
       }
    });

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate >= endDate) {
            showErrorMsg("日期有误，请重新选择!");
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24);
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var queryData = decodeQuery();
    var houseId = queryData["hid"];

    // TOD: 获取房屋的基本信息
    $.get('/api/v1.0/house/' + houseId, function (resp) {
       if (resp.errno == '0'){
           // 图片,金额,总金额
           $('.house-info>img').attr('src',resp.data.house.img_urls[0]);
           $('.house-info>.house-text>h3').html(resp.data.house.title);
           $('.house-info>.house-text>p>span').html(resp.data.house.price/100).toFixed(0);
       }
    });

    // TOD: 订单提交
    $('.submit-btn').on('click', function () {
        var start_day = $('#start-date').val();
        var end_day = $('#end-date').val();
        if (!(start_day && end_day)){
            return '请输入时间信息'
        }
        var params = {
            'start_day': start_day,
            'end_day': end_day,
            'house_id': houseId
        };
        $.ajax({
            url: '/api/v1.0/order',
            type: 'post',
            data: JSON.stringify(params),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0'){
                    // 下单成功
                    location.href = '/orders.html'
                }else if (resp.errno == '4101'){
                    location.href = '/login.html'
                }else {
                    alert(resp.errmsg)
                }
            }
        })
    })
});
