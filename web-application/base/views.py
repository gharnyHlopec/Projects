from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Headphones, Mouse, Keyboard, SharedID, Review, ProductImage, Cart, CartItem, User, Product
from .forms import MouseForm, KeyboardForm, HeadphonesForm, ReviewForm, ProductImageForm, MyUserCreationForm, UserForm, GuestOrderForm, MyUserEditForm,ProductForm
from django.http import HttpResponse, JsonResponse,HttpResponseNotFound
import json
from django.urls import reverse
from django.db.models import Avg
from django.contrib.sessions.backends.db import SessionStore
from django.db import transaction
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator

def only_for_staff(user):
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
    min_price = request.GET.get('min_price') or '-1'
    max_price = request.GET.get('max_price') or '9999999'
    min_year = request.GET.get('min_year') or '-1'
    max_year = request.GET.get('max_year') or '9999999'

    availability = int(request.GET.get('availability', -1))

    if page == 'all':
        products = Product.objects.filter(name__icontains=q,
                                            price__gte=min_price,
                                            price__lte=max_price,
                                            year__gte=min_year,
                                            year__lte=max_year,
                                            amount__gt=availability)

    else:
        products = Product.objects.filter(type=page,
                                        price__gte=min_price,
                                        price__lte=max_price,
                                        year__gte=min_year,
                                        year__lte=max_year,
                                        amount__gt=availability)
    if sort_param:
        products = products.order_by(sort_param)
    amount_of_products = len(products)

    context = {
        'products': products,
        'page':page,
        'q':q,
        'min_price':min_price,
        'max_price':max_price,
        'min_year':min_year,
        'max_year':max_year,
        'availability':availability,
        'sort':sort_param,
        'amount_of_products': amount_of_products
    }   

    # paginator = Paginator(obj,2)
    # print(list(paginator.get_elided_page_range()))
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render(request,'catalog_grid_innerHTML.html',context)
        return JsonResponse({'html':html.content.decode('utf-8')})
    else:
        return render(request, 'catalog.html', context)


def info(request,pk):
    
    product = Product.objects.get(id=pk)
    description = json.loads(product.description)

    if product.type == 'keyboard':
        info = ['Дата выхода на рынок','Тип','Технология переключателя', 'Наименование переключателей', 'Цвет', 'Кириллица', 'Беспроводная', 'Оплетка кабеля']
        data = [product.year,product.type,description["switch_type"],description["switch_name"],description["color"],description["cyrillic"],description["wireless"],description["cable_braid"]]

    elif product.type == 'mouse':
        info = ['Дата выхода на рынок','Тип','Беспроводная', 'Тип сенсора', 'Модель сенсора', 'Максимальное разрешение сенсора', 'Максимальная частота опроса', 'материал корпуса', 'Подсветка']
        data = [product.year,product.type,description["wireless"],description["sensor_type"],description["sensor_model"],description["sensor_resolution"],description["sensor_polling_rate"],description["case_material"],description["lighting"]]

    elif product.type == 'headphones':
        info = ['Дата выхода на рынок','Тип','Беспроводной интерфейс','Пыле-, влаго-, ударопрочность','Материал корпуса','Цвет наушников','Цвет кабеля','Материал покрытия оголовья']
        data = [product.year,product.type,description["wireless"],description["protection"],description["case_material"],description["headphones_color"],description["cable_color"],description["ear_cushion_material"]]
        
    images = ProductImage.objects.filter(product_id = product)
    image_amount = len(images)
    zipped_data = zip(info, data)
    context = {"product": product, "zipped_data": zipped_data, "images":images, "image_amount":image_amount}

    return render(request, 'info.html', context)

@user_passes_test(staff_not_allowed, login_url='/login')
def cart(request):
    cart = None
    cart_products = None
    total_sum = 0
    #Если запрос пришел с AJAX, то добавляем/убавляем количество товара в корзине
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        cart_id = data.get('product_id')
        value = data.get('value')
        cart_item = get_object_or_404(CartItem, id=cart_id)

        if value:
            cart_item.quantity += int(value)
            cart_item.save()
        else:
            cart_item.delete()  

    #Получаем или создаем корзину
    if request.user.is_authenticated:
        cart,_ = Cart.objects.get_or_create(user=request.user, status = '-')
    else:
        if request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key, status = '-').last()

    #Если корзина есть, то получаем её содержимое 
    if cart:
        cart_products = CartItem.objects.filter(cart=cart)
    else:
        context = {'cart_products':cart_products}
        return render(request, 'cart.html', context)

    #Расписываем подробнее её содержимое
    products_with_details = []
    for item in cart_products:
        details = Product.objects.get(id=item.product.id)
        item_details = {
            'cart_item_id': item.id,
            'name': details.name,
            'price': details.price,
            'quantity': item.quantity,
            'result': details.price * item.quantity,
        }

        if item.first_image is not None:
            item_details['image'] = item.first_image.image.url
        else:
            item_details['image'] = static('/images/placeholder.jpg')

        products_with_details.append(item_details) 

    for product_with_details in products_with_details:
        total_sum += product_with_details['result']

    context = {'products_with_details':products_with_details, 'total_sum':total_sum}
    #Если AJAX-запрос, то просто меняем внутренности корзины
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
        navbar_html = render(request,'navbar.html')
        cart_product_wrapper_html = render(request,'cart_product_wrapper.html',context)
        return JsonResponse({'navbar_html':navbar_html.content.decode('utf-8'),
                             'cart_product_wrapper_html':cart_product_wrapper_html.content.decode('utf-8')})
    else: # Если нет то полностью отрисовываем страницу
        return render(request, 'cart.html', context)

def contactInformation(request):
    if request.user.is_authenticated:
        cart,_ = Cart.objects.get_or_create(user=request.user, status = '-')
        form = UserForm(instance=request.user)
    else:
        if request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key, status = '-').last()
        form = GuestOrderForm()

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

    context = {"form":form,"cart":cart}
    return render(request, 'contact-information.html', context)


def reviews(request, pk):
    product = Product.objects.get(id = pk)
    reviews = product.review_set.all().order_by('-created')
    context = {'reviews':reviews, "product":product}
    return render(request, 'reviews.html', context)

@login_required(login_url='/login')
@user_passes_test(staff_not_allowed, login_url='/login')
def postReview(request, pk):
    if request.method == 'POST':
        Review.objects.create(
            user=request.user,
            product = Product.objects.get(id = pk),
            title=request.POST.get('title'),
            rating = request.POST.get('rating'),
            body=request.POST.get('body')
        )        
        return redirect('product-reviews',pk)
    else:
        context = {'pk':pk}
    if not request.user.is_authenticated:
        return redirect('login') 
    return render(request, 'review_form.html', context)


def deleteReview(request, prod_id, pk):
    review = Review.objects.get(id=pk)

    if request.user != review.user and request.user.is_staff != True:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        review.delete()
        return redirect('product-reviews', prod_id)
    return render(request, 'delete.html')

@login_required(login_url='/login')
@user_passes_test(only_for_staff, login_url='/login')
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

        # form.save()
        pics = request.FILES.getlist('images')
        for pic in pics:
            ProductImage.objects.create(
            shared_id=elem,
            image=pic
        )  
        
        if form.is_valid():
            form.save()
            return redirect('info',pk)

    context = {'form':form, 'images':images, 'pk':pk}
    return render(request, 'edit_product.html', context)

@login_required(login_url='/login')
@user_passes_test(only_for_staff, login_url='/login')
def deleteProduct(request,pk):
    product = Product.objects.get(id = pk) 
    if request.method == 'POST':
        product.delete()
        return redirect('catalog',product.type)
    return render(request, 'delete.html', {'pruduct':product})

@login_required(login_url='/login')
@user_passes_test(only_for_staff, login_url='/login')
def deleteImage(request, pk, pk2): 
    elem = ProductImage.objects.get(id=pk2)
    if request.method == 'POST':
        elem.delete()
        return redirect('update-product', pk)
    return render(request, 'delete.html', {'obj':elem.image})

@user_passes_test(staff_not_allowed, login_url='/login')
def addToCart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = 1
        product = get_object_or_404(Product, id=product_id)

        if (not request.user.is_authenticated) and (not request.session.session_key):
            session = SessionStore()
            session.create()
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
        html = render(request,'navbar.html')
        
        return JsonResponse({'html':html.content.decode('utf-8')})
    else:
        redirect('main')

@login_required(login_url='/login')
@user_passes_test(only_for_staff, login_url='/login')
def adminPanel(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = Cart.objects.get(id = data.get('pk'))
        if data.get('action') == 'accept':
            with transaction.atomic():
                cartItems = CartItem.objects.filter(cart=cart)
                for item in cartItems:
                    details = Product.objects.get(id=item.product.id)
                    if item.quantity > details.amount:
                        cart.status = 'Отменен системой (на складе недостаточно товара)'
                        cart.save()
                        return redirect('admin-panel') 
                    else:
                        details.amount -= item.quantity
                        details.save()
                cart.status = 'Принят'
        elif data.get('action') == 'decline':
            if cart.status == 'Принят':
                cartItems = CartItem.objects.filter(cart=cart)
                for item in cartItems:
                    details = Product.objects.get(id=item.product.id)
                    details.amount += item.quantity
                    details.save()
            cart.status = 'Отменен'
        elif data.get('action') == 'finish':
            cart.status = 'Завершен'
        cart.save()

    carts = Cart.objects.exclude(status = '-').order_by('status')
    cart_items = {}  

    for cart in carts:
        items = CartItem.objects.filter(cart=cart)
        cart_items[cart] = items  

    context = {
        'carts': carts,
        'cart_items': cart_items, 
        }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render(request, 'admin_panel_innerHTML.html',context)
        return JsonResponse({'html':html.content.decode('utf-8')})
    else:
        return render(request, 'admin_panel.html', context)

@login_required(login_url='/login')
@user_passes_test(only_for_staff, login_url='/login')
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
    carts = Cart.objects.exclude(status='-').filter(user=request.user).order_by('-updated')
    cart_items = {} 

    for cart in carts:
        items = CartItem.objects.filter(cart=cart)
        cart_items[cart] = items  

    context = {
        'carts': carts,
        'cart_items': cart_items, 
        }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render(request,'user-orders-innerHTML.html',context)
        return JsonResponse({'html':html.content.decode('utf-8')}) 

    return render(request, 'user-orders.html', context)

def addProduct(request,product_type,allowed_types):
    if product_type not in allowed_types.split('|'):
        return HttpResponseNotFound('Invalid product type')
    else:
        form = ProductForm()
        if request.method == 'POST':
            data = request.POST.get('json_data')
            
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.type = product_type
                product.description = data
                product.save()
                product_id = Product.objects.get(pk=product.id)
                images = request.FILES.getlist('images')
                for pic in images:
                    try:
                        ProductImage.objects.create(
                            product_id=product_id,
                            image=pic
                        )
                    except Exception as e:
                        messages.error(request, "Произошла ошибка при загрузке изображения.")
                return JsonResponse({'redirect':reverse('catalog',kwargs={'page':product_type}) })
            else:
                context = {'form': form, 'product_type':product_type}
                html = render(request, 'add_product_form_innerHTML.html',context)
                return JsonResponse({'html':html.content.decode('utf-8')})

        context = {'form': form, 'product_type':product_type}
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render(request, 'add_product_form_innerHTML.html',context)
            return JsonResponse({'html':html.content.decode('utf-8')})
        else:
            return render(request, 'add_product.html', context)