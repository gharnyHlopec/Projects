from django.contrib import admin
from .models import Headphones, Mouse, Keyboard, Review,SharedID, Review, ProductImage, Cart, CartItem, User, Product

# Register your models here.

admin.site.register(Headphones)
admin.site.register(Mouse)
admin.site.register(Keyboard)
admin.site.register(Review)
admin.site.register(SharedID)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(User)
admin.site.register(Product)