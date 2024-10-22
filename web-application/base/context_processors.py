from .models import Cart, CartItem
from django.db.models import Sum


def cart_item_count(request):
    cart_count = 0
    cart = None
    if request.user.is_authenticated:
        cart,_ = Cart.objects.get_or_create(user=request.user, status = '-')
    elif request.session.session_key != None:
        cart,_ = Cart.objects.get_or_create(session_key=request.session.session_key,status = '-')
    if cart:
        cart_products = CartItem.objects.filter(cart=cart)
        if cart_products.exists():
            cart_count = cart_products.aggregate(Sum('quantity'))['quantity__sum']
        else:
            cart_count = 0  

    return {'cart_item_count': cart_count}