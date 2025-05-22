from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import Avg

phone_regex = RegexValidator(
    regex=r'^\+?[0-9]+$', 
    message="Введите корректный номер телефона, содержащий только цифры и знак '+'"
)

class User(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    phone_number = models.CharField(
        max_length=20, 
        validators=[phone_regex], 
        null = True,
        blank=False  
    )
    username = models.CharField(max_length=100, blank = True, null = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Product(models.Model):
    product_types = [
        ('keyboard', 'Клавиатура'),
        ('mouse', 'Мышь'),
        ('headphones', 'Наушники'),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=40, choices=product_types,default='')
    name = models.CharField(max_length=200)
    price = models.DecimalField(validators=[MinValueValidator(0)],decimal_places=2, max_digits=10)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    year = models.IntegerField(validators=[MinValueValidator(1970),MaxValueValidator(2030)])
    
    description = models.JSONField(null=True,blank=True)

    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.id)
    
    @property
    def first_image(self):
        return self.images.first()
    
    def get_average_rating(self):
        average = self.review_set.aggregate(Avg('rating'))['rating__avg']
        return str(round(average, 1)) if average is not None else 0.0
        
    @property
    def get_review_count(self):
        return self.review_set.count() or 0  
    
    def delete(self, *args, **kwargs):
        for img in self.images.all():
            img.delete()
        super().delete(*args,**kwargs) 
    
    
class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True)
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE,null=True)
    title = models.CharField(max_length=350,null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    body = models.TextField(null = True, blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated','-created']


    def __str__(self):
        return str(self.id)
    

class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def first_image(self):
        if self.product.images.first():
            return self.product.images.first()

class Order(models.Model):

    statuses = [
        ('В обработке', 'В обработке'),
        ('Принят', 'Принят'),
        ('Отменен', 'Отменен'),
        ('Отменен системой (на складе недостаточно товара)', 'Отменен системой (на складе недостаточно товара)'),
        ('Завершен','Завершен')
    ]

    payment_statuses = [
        ('Оплата картой курьеру', 'Оплата картой курьеру'),
        ('Оплата наличными курьеру', 'Оплата наличными курьеру'),
        ('Оплата картой на сайте', 'Оплата картой на сайте'),
        ('Оплачен', 'Оплачен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, choices=statuses, default='-')
    payment_status = models.CharField(max_length=50, choices=payment_statuses, default='-')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    @property
    def get_total_cost(self):
        total_cost = 0
        for product in self.items.all():
            total_cost += product.price * product.quantity
        return total_cost

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=350,null=True)
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(validators=[MinValueValidator(0)],decimal_places=2, max_digits=10, null=True)