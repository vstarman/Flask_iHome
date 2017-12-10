function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // TOD: 获取该房屋的详细信息
    $.get('/api/v1.0/house/'+houseId, function (resp) {
        if (resp.errno == '0'){
            // 填充房屋里的图片数据
            $('.swiper-container').html(template('house-detail-tmpl',
                {'img_urls': resp.data.house.images, 'price': resp.data.house.price}));
            // 填充房屋里的详情数据
            $('.detail-con').html(template('house-detail-tmpl', {'house': resp.data.house}));
            // 判断是否是房东
            if (resp.data.house.user_id != resp.data.user_id){
                // 显示预定按钮
                $('.book-house').show();
                // 设置点击预定的url
                $('.book-house').attr('href', '/booking.html?hid='+resp.data.house.hid)
            }
            // 数据加载完毕,需显示幻灯片效果
            // TOD: 数据加载完毕后,需要设置幻灯片对象，开启幻灯片滚动
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
        }
    });
})