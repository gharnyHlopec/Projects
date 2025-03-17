from django.urls import path
from . import views

urlpatterns = [
    path('',views.main, name = 'main'),
    path('login/',views.loginPage, name = 'login'),
    path('logout/',views.logoutUser, name = 'logout'),
    path('register/',views.registerPage, name = 'register'),
    path('add_product/<str:product_type>', views.addProduct, name='add_product'),
    path('update-product/<str:pk>', views.updateProduct, name='update-product'),
    path('delete-product/<str:pk>', views.deleteProduct, name='delete-product'),
    path('delete-image/<str:pk>/<str:pk2>', views.deleteImage, name='delete-image'), # возможно нужно будет удалить
    path('reviews/<str:pk>', views.reviews, name='product-reviews'),
    path('post-review/<str:pk>', views.postReview, name='post-review'),
    path('delete-review/<str:prod_id>/<str:pk>', views.deleteReview, name='delete-review'),
    path('catalog/<str:page>/',views.catalog, name = 'catalog'),
    path('info/<str:pk>/', views.info, name = 'info'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.addToCart, name='add-to-cart'),
    path('admin-panel/',views.adminPanel, name = 'admin-panel'),
    path('person-panel/',views.personPanel, name = 'person-panel'),
    path('profile/',views.profile, name = 'profile'),
    path('update-profile/',views.updateProfile, name = 'update-profile'),
    path('user-orders/',views.userOrders, name = 'user-orders'),
    path('contact-information/', views.contactInformation, name='contact-information'),
    path('test/<str:product_type>',views.testView,name='test')      
]