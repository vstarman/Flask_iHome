//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// $(document).ready(function(){
//     $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
//     $(window).on('resize', centerModals);
//     // TOD: 查询房东的订单
//     $.get('/api/v1.0/user/orders?role=landlord', function (resp) {
//         if (resp.errno == '0'){
//             $('.orders-list').html(template('orders-list-tmpl', {'orders': resp.data.orders}))
//             $(".order-accept").on("click", function(){
//                 // 点击接单按钮
//                 var order_id = $(this).parents("li").attr("order-id");
//                 $(".modal-accept").attr("order-id", order_id);
//                 });
//             $('.modal-accept').on('click', function () {
//                 var order_id = $(this).attr("order-id");
//                 $.ajax({
//                         url: '/api/v1.0/order/' + order_id + '/status',
//                         type: 'put',
//                         contentType: 'application/json',
//                         headers: {
//                             'X-CSRFToken': getCookie('csrf_token')
//                         },
//                         success: function (resp) {
//                             if (resp.errno == '0'){
//                                 // 1.设置订单状态的html
//                                 $('.order-text>span').html('已接单');
//                                 // 2.隐藏接单拒单按钮
//                                 $('.order-operate').hide();
//                                 // 隐藏弹出的框
//                                 $('#accept-modal').hide()
//                             }
//                         }
//                     })
//                 });
//             $(".order-reject").on("click", function(){
//                 // 拒单
//                 var order_id = $(this).parents("li").attr("order-id");
//                 $(".modal-reject").attr("order-id", order_id);
//             });
//         }
//     });
//     // TODO: 查询成功之后需要设置接单和拒单的处理
//     // TODO: order-id标签设置不上
//
// });

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    // 查询房东的订单
    $.get("/api/v1.0/user/orders?role=landlord", function (resp) {
        if (resp.errno == "0") {
            $(".orders-list").html(template("orders-list-tmpl", {"orders": resp.data.orders}))
            // 查询成功之后需要设置接单和拒单的处理
            $(".order-accept").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });
            $(".modal-accept").on("click", function () {
                var orderId = $(this).attr("order-id");
                // 接单
                $.ajax({
                    url: "/api/v1.0/order/" + orderId + "/status",
                    type: "put",
                    contentType: "application/json",
                    headers: {
                        "X-CSRFToken": getCookie("csrf_token")
                    },
                    success: function (resp) {
                        if (resp.errno == "0") {
                            // 1. 设置订单状态的html
                            $(".orders-list>li[order-id=" + orderId + "]>div.order-content>div.order-text>ul li:eq(4)>span").html("已接单");
                            // 2. 隐藏接单和拒单操作
                            $("ul.orders-list>li[order-id=" + orderId + "]>div.order-title>div.order-operate").hide();
                            // 3. 隐藏弹出的框
                            $("#accept-modal").modal("hide");
                        }
                    }
                })
            });
            $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });
        }
    })
});