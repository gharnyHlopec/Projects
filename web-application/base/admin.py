from django.contrib import admin
from .models import Review,Review, ProductImage, Cart, CartItem, Order, OrderItem, User, Product

# Register your models here.

admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)
admin.site.register(Product)