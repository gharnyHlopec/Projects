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

class SharedID(models.Model):

    type_choice = [
        ('Keyboard', 'Keyboard'),
        ('Mouse', 'Mouse'),
        ('Headphones', 'Headphones'),
    ]
        
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20,choices=type_choice,default='')
    
    def __str__(self):
        return str(self.id)
    


#----------------------------------------------------------------------------------------------
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
    
    @property
    def get_average_rating(self):
        average = self.review_set.aggregate(Avg('rating'))['rating__avg'] #обратное отношение с именем <имя_модели>_set
        return round(average, 1) if average is not None else 0.0 # считаем avg(rating) и получаем подключеваое значения словаря
    
    @property
    def get_review_count(self):
        return self.review_set.count() or 0  # считаем сколько отзывов соответствует этому продукту
#----------------------------------------------------------------------------------------------
    



    
class Headphones(models.Model):
        
    available_choices = [
        ('-', '-'),
        ('Без микрофона', 'Без микрофона'),
        ('С микрофоном', 'С микрофоном'),
        ('Игровые', 'Игровые'),
    ]
    
    boolean_choices = [
        ('Yes','Да'),
        ('No','Нет'),
    ]

    shared_id = models.OneToOneField(SharedID, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    
    date = models.IntegerField(validators=[MinValueValidator(1970), MaxValueValidator(2030)])
    type = models.CharField(max_length=20,choices=available_choices,default='')
    wireless = models.BooleanField(null = True, blank = True, choices=boolean_choices)
    ruggedness = models.BooleanField(null = True, blank = True, choices=boolean_choices)
    body_material = models.CharField(max_length=200, null = True, blank = True)
    headphone_color = models.CharField(max_length=200, null = True, blank = True)
    cable_color = models.CharField(max_length=200, null = True, blank = True)
    earpad_material = models.CharField(max_length=200, null = True, blank = True)
    
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        if not self.shared_id:
            shared_id = SharedID.objects.create(type='Headphones')  
            self.shared_id = shared_id
        else:
            self.shared_id.type = 'Headphones'
            self.shared_id.save() 
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.shared_id.delete()  
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    

class Mouse(models.Model):
        
    mouse_choices = [
        ('-', '-'),
        ('Мышь', 'Мышь'),
        ('Игровая мышь', 'Игровая мышь'),
        ('Трекбол', 'Трекбол'),
    ]

    sensor_choices = [
        ('-', '-'),
        ('Лазерный', 'Лазерный'),
        ('Оптический', 'Оптический'),
        ('BlueTrack', 'BlueTrack'),
    ]

    boolean_choices = [
        ('Yes','Да'),
        ('No','Нет'),
    ]

    shared_id = models.OneToOneField(SharedID, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    
    date = models.IntegerField(validators=[MinValueValidator(1970), MaxValueValidator(2030)])
    type = models.CharField(max_length=20,choices=mouse_choices,default='')
    wireless = models.BooleanField(null = True, blank = True, choices=boolean_choices)
    sensor_type = models.CharField(max_length=20,choices=sensor_choices,default='')
    sensor_model = models.CharField(max_length=50, null = True, blank = True)
    max_sens_res = models.IntegerField(validators=[MinValueValidator(1)],null = True, blank = True)
    max_pooling_rate = models.IntegerField(validators=[MinValueValidator(1)],null = True, blank = True)
    body_material = models.CharField(max_length=200, null = True, blank = True)
    backlight = models.BooleanField(null = True, blank = True, choices=boolean_choices)
    
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)


    def save(self, *args, **kwargs):
        if not self.shared_id:
            shared_id = SharedID.objects.create(type='Mouse')  
            self.shared_id = shared_id
        else:
            self.shared_id.type = 'Mouse'  
            self.shared_id.save()  
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.shared_id.delete()  
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    

class Keyboard(models.Model):
        
    keyboard_choices = [
        ('-', '-'),
        ('Игровая', 'Игровая'),
        ('Офисная', 'Офисная'),
        ('Стандартная', 'Стандартная'),
        ('Офисная', 'Офисная'),
    ]

    switch_choices = [
        ('-', '-'),
        ('Механическая', 'Механическая'),
        ('Мембранная', 'Мембранная'),
        ('Оптическая', 'Оптическая'),
    ]

    boolean_choices = [
        ('Yes','Да'),
        ('No','Нет'),
    ]

    shared_id = models.OneToOneField(SharedID, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    
    date = models.IntegerField(validators=[MinValueValidator(1970), MaxValueValidator(2030)])
    type = models.CharField(max_length=20,choices=keyboard_choices,default='')
    switch_type = models.CharField(max_length=30,choices=switch_choices,default='')
    switch_name = models.CharField(max_length=200, null = True, blank = True)
    color = models.CharField(max_length=200, null = True, blank = True)
    сyrillic = models.BooleanField(null = True, blank = True, choices=boolean_choices)
    wireless = models.BooleanField(null = True, blank = True, choices=boolean_choices)
    cable_sleeving = models.BooleanField(null = True, blank = True, choices=boolean_choices)
    
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)


    def save(self, *args, **kwargs):
        if not self.shared_id:
            shared_id = SharedID.objects.create(type='Keyboard') 
            self.shared_id = shared_id
        else:
            self.shared_id.type = 'Keyboard'  
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.shared_id.delete()  
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    

class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True)
    # shared_id = models.ForeignKey(SharedID, on_delete=models.CASCADE, related_name="images")
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

    statuses = [
        ('-', '-'),
        ('В обработке', 'В обработке'),
        ('Принят', 'Принят'),
        ('Отменен', 'Отменен'),
        ('Отменен системой (на складе недостаточно товара)', 'Отменен системой (на складе недостаточно товара)'),
        ('Завершен','Завершен')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=statuses, default='-')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    updated = models.DateTimeField(auto_now = True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def first_image(self):
        if self.product.images.first():
            return self.product.images.first()
        