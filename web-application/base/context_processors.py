from .models import Cart, CartItem
from django.db.models import Sum
from django.contrib.sessions.backends.db import SessionStore

def cart_item_count(request):
    cart_count = 0

    if (not request.user.is_authenticated) and (not request.session.session_key):
        session = SessionStore()
        session.create()
        request.session = session
        
    cart, _ = Cart.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key if not request.user.is_authenticated else None, 
    )

    cart_products = CartItem.objects.filter(cart=cart)
    if cart_products.exists():
        cart_count = cart_products.aggregate(Sum('quantity'))['quantity__sum']
    else:
        cart_count = 0  

    return {'cart':cart,'cart_item_count': cart_count}