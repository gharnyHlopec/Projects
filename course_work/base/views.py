from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Headphones, Mouse, Keyboard, SharedID, Review, ProductImage, Cart, CartItem, User
from .forms import MouseForm, KeyboardForm, HeadphonesForm, ReviewForm, ProductImageForm, MyUserCreationForm, UserForm, GuestOrderForm, MyUserEditForm
from django.http import HttpResponse
import os
from django.db.models import Sum, Avg
from django.contrib.sessions.backends.db import SessionStore
from django.db import transaction
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def staff_is_allowed(user):
  return user.is_staff

def staff_not_allowed(user):
  return not user.is_staff

def main(request):
    return render(request, 'main.html')

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'Пользователь не существует')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, "Имя пользователя или пароль не существует")

    context = {'page':page}
    return render(request, 'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('main')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request,'Во время регистрации возникла ошибка')


    return render(request,'login_register.html', {'form' : form})


def catalog(request, page):
    q = request.GET.get('q', '')
    sort_param = request.GET.get('sort', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')
    availability = int(request.GET.get('availability', 0))
    context = {}
    if page == 'all':
        headphones = Headphones.objects.filter(name__icontains=q)
        mouses = Mouse.objects.filter(name__icontains=q)
        keyboards = Keyboard.objects.filter(name__icontains=q)

        if min_price:
            headphones = headphones.filter(price__gte=min_price)
            mouses = mouses.filter(price__gte=min_price)
            keyboards = keyboards.filter(price__gte=min_price)
            context['min_price'] = min_price
    
        if max_price:
            headphones = headphones.filter(price__lte=max_price)
            mouses = mouses.filter(price__lte=max_price)
            keyboards = keyboards.filter(price__lte=max_price)
            context['max_price'] = max_price

        if min_year:
            headphones = headphones.filter(date__gte=min_year)
            mouses = mouses.filter(date__gte=min_year)
            keyboards = keyboards.filtzr(date__gte=min_year)
            context['min_year'] = min_year

        if max_year:
            headphones = headphones.filter(date__lte=max_year)
            mouses = mouses.filter(date__lte=max_year)
            keyboards = keyboards.filter(date__lte=max_year)
            context['max_year'] = max_year
        
        if availability == 1:
            headphones = headphones.filter(amount__gt=0)
            mouses = mouses.filter(amount__gt=0)
            keyboards = keyboards.filter(amount__gt=0)

        if sort_param:
            headphones = headphones.order_by(sort_param)
            mouses = mouses.order_by(sort_param)
            keyboards = keyboards.order_by(sort_param)
        sum = len(headphones) + len(mouses) + len(keyboards)

        context = {
            'headphones': headphones,
            'mouses': mouses,
            'keyboards': keyboards,
            'page': page,
            'q': q,
            'sum': sum,
            'sort': sort_param,
            'min_price': min_price,
            'max_price': max_price,
            'min_year': min_year,
            'max_year': max_year,
            'availability':availability
        }

    elif page == 'headphone':
        obj = Headphones.objects.all()
        if min_price:
            obj = obj.filter(price__gte=min_price)
        if max_price:
            obj = obj.filter(price__lte=max_price)
        if min_year:
            obj = obj.filter(date__gte=min_year)
        if max_year:
            obj = obj.filter(date__lte=max_year)
        if availability == 1:
            obj = obj.filter(amount__gt=0)
    
        
        if sort_param:
            obj = obj.order_by(sort_param)
        context['obj'] = obj
        context['sort'] = sort_param 

    elif page == 'mouse':
        obj = Mouse.objects.all()

        if min_price:
            obj = obj.filter(price__gte=min_price)
        if max_price:
            obj = obj.filter(price__lte=max_price)
        if min_year:
            obj = obj.filter(date__gte=min_year)
        if max_year:
            obj = obj.filter(date__lte=max_year)
        if availability == 1:
            obj = obj.filter(amount__gt=0)
    
        
        if sort_param:
            obj = obj.order_by(sort_param)
        context['obj'] = obj
        context['sort'] = sort_param

    elif page == 'keyboard':
        obj = Keyboard.objects.all()

        if min_price:
            obj = obj.filter(price__gte=min_price)
        if max_price:
            obj = obj.filter(price__lte=max_price)
        if min_year:
            obj = obj.filter(date__gte=min_year)
        if max_year:
            obj = obj.filter(date__lte=max_year)
        if availability == 1:
            obj = obj.filter(amount__gt=0)

        if sort_param:
            obj = obj.order_by(sort_param)
        context['obj'] = obj 
        context['sort'] = sort_param

    context['page'] = page
    context['q'] = q
    context['min_price'] = min_price
    context['max_price'] = max_price
    context['min_year'] = min_year
    context['max_year'] = max_year    
    context['availability'] = availability    


    return render(request, 'catalog.html', context)


def info(request,pk):
    
    elem = SharedID.objects.get(id = pk)
    average_rating = Review.objects.filter(product=elem).aggregate(Avg('rating'))['rating__avg'] or 0
    
    review_count = Review.objects.filter(product=elem).count()

    if elem.type == 'Headphones':
        obj = Headphones.objects.get(shared_id = pk)
        info = ['Дата выхода на рынок','Тип','Беспроводной интерфейс','Пыле-, влаго-, ударопрочность','Материал корпуса','Цвет наушников','Цвет кабеля','Материал покрытия оголовья']
        data = [obj.date, obj.type, obj.wireless, obj.ruggedness, obj.body_material, obj.headphone_color, obj.cable_color, obj.earpad_material]

        
    elif elem.type == 'Mouse':
        obj = Mouse.objects.get(shared_id = pk)
        info = ['Дата выхода на рынок','Тип','Беспроводная', 'Тип сенсора', 'Модель сенсора', 'Максимальное разрешение сенсора', 'Максимальная частота опроса', 'материал корпуса', 'Подсветка']
        data = [obj.date, obj.type, obj.wireless, obj.sensor_type, obj.sensor_model, obj.max_sens_res, obj.max_pooling_rate, obj.body_material, obj.backlight]

    elif elem.type == 'Keyboard':
        obj = Keyboard.objects.get(shared_id = pk)
        info = ['Дата выхода на рынок','Тип','Технология переключателя', 'Наименование переключателей', 'Цвет', 'Кириллица', 'Беспроводная', 'Оплетка кабеля']
        data = [obj.date, obj.type, obj.switch_type, obj.switch_name, obj.color, obj.сyrillic, obj.wireless, obj.cable_sleeving]

    images = ProductImage.objects.filter(shared_id = elem)
    zipped_data = zip(info, data)
    context = {"obj": obj, "zipped_data": zipped_data, "images":images, "average_rating": average_rating, 'review_count':review_count}

    return render(request, 'info.html', context)

@user_passes_test(staff_not_allowed, login_url='/login')
def cart(request):
    cart = None
    cart_products = None
    cart_count = 0
    total_sum = 0

    if request.method == 'POST':    
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, status = '-')
            form = UserForm(request.POST, instance = request.user)
        else:
            cart = Cart.objects.get(session_key=request.session.session_key, status = '-')
            form = GuestOrderForm(request.POST)
        if form.is_valid():
            cart.first_name = form.cleaned_data['first_name']
            cart.last_name = form.cleaned_data['last_name']
            cart.phone_number = form.cleaned_data['phone_number']
            cart.email = form.cleaned_data['email']
            cart.status = "В обработке"
            cart.save()
            return redirect('main')

    if request.user.is_authenticated:
        cart,_ = Cart.objects.get_or_create(user=request.user, status = '-')
        form = UserForm(instance=request.user)
    else:
        if request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key, status = '-').last()
        form = GuestOrderForm()
    if cart:
        cart_products = CartItem.objects.filter(cart=cart)
        if cart_products.exists():
            cart_count = cart_products.aggregate(Sum('quantity'))['quantity__sum']
        else:
            cart_count = 0  
    else:
        context = {'cart_products':cart_products, 'cart_item_count': cart_count, 'form':form}
        return render(request, 'cart.html', context)

    items_with_details = []
    for item in cart_products:
        product_type = item.product.type
        
        if product_type == 'Headphones':
            details = Headphones.objects.get(shared_id=item.product)
        elif product_type == 'Mouse':
            details = Mouse.objects.get(shared_id=item.product)
        elif product_type == 'Keyboard':
            details = Keyboard.objects.get(shared_id=item.product)

        item_details = {
            'cart_item_id': item.id,
            'name': details.name,
            'price': details.price,
            'quantity': item.quantity,
            'result': (details.price * item.quantity),
        }

        if item.first_image is not None:
            item_details['image'] = item.first_image.image.url
        else:
            item_details['image'] = static('/images/placeholder.jpg')

        items_with_details.append(item_details) 

    for elem in items_with_details:
        total_sum +=elem['result']


    context = {'form':form,'cart_products':cart_products, 'cart_item_count': cart_count, 
                'items_with_details':items_with_details, 'total_sum':total_sum}

    return render(request, 'cart.html', context)


def reviews(request, pk):
    elem = SharedID.objects.get(id = pk)
    reviews = elem.review_set.all().order_by('-created')
    context = {'reviews':reviews, "pk":pk}
    return render(request, 'reviews.html', context)

@login_required(login_url='/login')
@user_passes_test(staff_not_allowed, login_url='/login')
def postReview(request, pk):
    if request.method == 'POST':
        review = Review.objects.create(
            user=request.user,
            product = SharedID.objects.get(id = pk),
            title=request.POST.get('title'),
            rating = request.POST.get('rating'),
            body=request.POST.get('body')
        )        
        return redirect('product-reviews',pk)
    else:
        context = {}
    if not request.user.is_authenticated:
        return redirect('login') 
    return render(request, 'review_form.html', context)


def deleteReview(request, prod_id, pk):
    review = Review.objects.get(id=pk)

    if request.user != review.user and request.user.is_staff !=  True:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        review.delete()
        return redirect('product-reviews', prod_id)
    return render(request, 'delete.html', {'obj':review.body[:50]})


@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def addProduct(request):
    if request.method == 'POST':
        product_type = request.POST.get('product_type')
        if product_type == 'mouse':
            form = MouseForm(request.POST, request.FILES)
        elif product_type == 'keyboard':
            form = KeyboardForm(request.POST, request.FILES)
        elif product_type == 'headphones':
            form = HeadphonesForm(request.POST, request.FILES)

        if form.is_valid():
            elem = form.save()
            related_data = SharedID.objects.get(pk=elem.shared_id.id)

          
            images = request.FILES.getlist('images')
            for pic in images:
                try:
                    
                    images = ProductImage.objects.create(
                        shared_id=related_data,
                        image=pic
                    )
                except Exception as e:
                    
                    print(f"Ошибка при сохранении изображения: {e}") 
                    messages.error(request, "Произошла ошибка при загрузке изображения.")

            return redirect('main')
        else:
            errors = form.errors
            messages.error(request, 'Error')
            context = {'form': form,'errors': errors}
            return render(request, 'object_form.html', context)
    else:
        form = MouseForm()
        context = {'form': form}
        return render(request, 'object_form.html', context)
    

def get_form(request):
    product_type = request.GET.get('product_type')
    
    if product_type == 'mouse':
        form = MouseForm()
    elif product_type == 'keyboard':
        form = KeyboardForm()
    elif product_type == 'headphones':
        form = HeadphonesForm()
    
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def updateProduct(request,pk):
    elem = SharedID.objects.get(id = pk)
    images = ProductImage.objects.filter(shared_id = elem)
    if elem.type == 'Keyboard':
        obj = Keyboard.objects.get(shared_id=pk)
        form = KeyboardForm(instance=obj)

    elif elem.type == 'Mouse':
        obj = Mouse.objects.get(shared_id=pk) 
        form = MouseForm(instance=obj)
        
    elif elem.type =='Headphones':
        obj = Headphones.objects.get(shared_id=pk)
        form = HeadphonesForm(instance=obj)

    if request.method == 'POST':
        if elem.type == 'Keyboard':
            form = KeyboardForm(request.POST, instance = obj)
        elif elem.type == 'Mouse':
            form = MouseForm(request.POST, instance=obj)
        elif elem.type =='Headphones':
             form = HeadphonesForm(request.POST, instance=obj)

        form.save()
        pics = request.FILES.getlist('images')
        for pic in pics:
            images = ProductImage.objects.create(
            shared_id=elem,
            image=pic
        )  
        
        if form.is_valid():
            form.save()
            return redirect('info',pk)

    context = {'form':form, 'images':images, 'pk':pk}
    return render(request, 'edit_form.html', context)

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def deleteProduct(request,pk):
    elem = SharedID.objects.get(id = pk) 
    if elem.type == 'Keyboard':
        obj = Keyboard.objects.get(shared_id=pk)
        page = 'keyboard'
    elif elem.type == 'Mouse':
        obj = Mouse.objects.get(shared_id=pk)
        page = 'mouse'        
    elif elem.type =='Headphones':
        obj = Headphones.objects.get(shared_id=pk)
        page = 'headphone'

    if request.method == 'POST':
        obj.delete()
        return redirect('catalog', page)
    
    return render(request, 'delete.html', {'obj':obj})

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def deleteImage(request, pk, pk2): 
    elem = ProductImage.objects.get(id=pk2)
    if request.method == 'POST':
        elem.delete()
        return redirect('update-product', pk)
    return render(request, 'delete.html', {'obj':elem.image})

@user_passes_test(staff_not_allowed, login_url='/login')
def addToCart(request):
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = 1
        product = get_object_or_404(SharedID, id=product_id)

        if (not request.user.is_authenticated) and (not request.session.session_key):
            session = SessionStore()
            session.create()
            session_key = session.session_key
            request.session = session
            
        cart, _ = Cart.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if not request.user.is_authenticated else None, 
            status = '-'
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        print(10*'\n', request.build_absolute_uri())
        return redirect(previous_url)  
    
def deleteFromCart(request):
    item_id = request.POST.get('cart_item_id')
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
        return redirect('cart') 
    return redirect('cart')  


def minus(request):
    item_id = request.POST.get('cart_item_id')
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        cart_item.quantity -= 1
        cart_item.save()
        if cart_item.quantity == 0:
            deleteFromCart(request)  
        return redirect('cart')  
    return redirect('cart')  


def plus(request):
    item_id = request.POST.get('cart_item_id')
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        cart_item.quantity += 1 
        cart_item.save()
    return redirect('cart') 

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def adminPanel(request):
    carts = Cart.objects.exclude(status = '-').order_by('status')
    cart_items = {}  

    for cart in carts:
        items = CartItem.objects.filter(cart=cart)
        cart_items[cart] = items  

    context = {
        'carts': carts,
        'cart_items': cart_items, 
        }

    return render(request, 'admin_panel.html', context)

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def acceptOrder(request, pk):
    with transaction.atomic():
        cart = Cart.objects.get(id=pk)
        cartItems = CartItem.objects.filter(cart=cart)

        for item in cartItems:
            if item.product.type == 'Headphones':
                details = Headphones.objects.get(shared_id=item.product)
            elif item.product.type == 'Mouse':
                details = Mouse.objects.get(shared_id=item.product)
            elif item.product.type == 'Keyboard':
                details = Keyboard.objects.get(shared_id=item.product)

            if item.quantity > details.amount:
                cart.status = 'Отменен системой (на складе недостаточно товара)'
                cart.save()
                return redirect('admin-panel') 
            else:
                details.amount -= item.quantity
                details.save()

        cart.status = 'Принят'
        cart.save()
        return redirect('admin-panel')

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def declineOrder(request, pk):
    cart = Cart.objects.get(id = pk)
    if cart.status == 'Принят':
        cartItems = CartItem.objects.filter(cart=cart)
        for item in cartItems:
            if item.product.type == 'Headphones':
                details = Headphones.objects.get(shared_id=item.product)
            elif item.product.type == 'Mouse':
                details = Mouse.objects.get(shared_id=item.product)
            elif item.product.type == 'Keyboard':
                details = Keyboard.objects.get(shared_id=item.product)

            details.amount += item.quantity
            details.save()
    cart.status = 'Отменен'
    cart.save()
    return redirect('admin-panel')

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def finishOrder(request, pk):
    cart = Cart.objects.get(id = pk)
    cart.status = 'Завершен'
    cart.save()
    return redirect('admin-panel')

@login_required(login_url='/login')
@user_passes_test(staff_is_allowed, login_url='/login')
def personPanel(request):
    users = User.objects.all
    context = {'users':users}
    return render(request, 'person-panel.html', context)

@login_required(login_url='/login')
def profile(request):
    user=request.user
    context = {'user':user}
    return render(request,'profile.html',context)

@login_required(login_url='/login')
def updateProfile(request):
    if request.method == 'POST':
        form = MyUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = MyUserEditForm(instance=request.user)

    context = {'form': form} 
    return render(request, 'edit-profile.html', context)

@login_required(login_url='/login')
@user_passes_test(staff_not_allowed, login_url='/login')
def userOrders(request):
    carts = Cart.objects.exclude(status='-').filter(user=request.user).order_by('status')
    cart_items = {} 

    for cart in carts:
        items = CartItem.objects.filter(cart=cart)
        cart_items[cart] = items  

    context = {
        'carts': carts,
        'cart_items': cart_items, 
        }
    return render(request, 'user-orders.html', context)