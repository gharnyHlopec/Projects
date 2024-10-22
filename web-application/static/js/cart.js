$(document).ready(function() {
    $(".quantity-control button").click(function() {
        var $button = $(this);
        var cartItemId = $button.attr('id').split('-')[1];
        var newQuantity = parseInt($("#quantity-" + cartItemId).text());
        if ($button.hasClass('plus')) {
            newQuantity++;
        } else if ($button.hasClass('minus') && newQuantity > 1) {
            newQuantity--;
        }
        $.ajax({
            url: '/update_cart_quantity/',
            type: 'POST',
            data: {
                'cart_item_id': cartItemId,
                'new_quantity': newQuantity
            },
            success: function(data) {
                $("#quantity-" + cartItemId).text(data.quantity);
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});