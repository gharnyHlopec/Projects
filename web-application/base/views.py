from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Headphones, Mouse, Keyboard, SharedID, Review, ProductImage, Cart, CartItem, User
from .forms import MouseForm, KeyboardForm, HeadphonesForm, ReviewForm, ProductImageForm, MyUserCreationForm, UserForm, GuestOrderForm, MyUserEditForm
from django.http import HttpResponse, JsonResponse
import json
from django.urls import reverse
from django.db.models import Avg
from django.contrib.sessions.backends.db import SessionStore
from django.db import transaction
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


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


    context = {}
    if page == 'all':
        headphones = Headphones.objects.filter(name__icontains=q,
                                       price__gte=min_price,
                                       price__lte=max_price,
                                       date__gte=min_year,
                                       date__lte=max_year,
                                       amount__gt=availability)
        mouses = Mouse.objects.filter(name__icontains=q,
                               price__gte=min_price,
                               price__lte=max_price,
                               date__gte=min_year,
                               date__lte=max_year,
                               amount__gt=availability)
        keyboards = Keyboard.objects.filter(name__icontains=q,
                                     price__gte=min_price,
                                     price__lte=max_price,
                                     date__gte=min_year,
                                     date__lte=max_year,
                                     amount__gt=availability)
 
        if sort_param:
            headphones = headphones.order_by(sort_param)
            mouses = mouses.order_by(sort_param)
            keyboards = keyboards.order_by(sort_param)
        sum = len(headphones) + len(mouses) + len(keyboards)

        context = {
            'headphones': headphones,
            'mouses': mouses,
            'keyboards': keyboards,
            'sum': sum
        } 

    elif page == 'headphones':
        obj = Headphones.objects.all()

        obj = obj.filter(price__gte=min_price,
                            price__lte=max_price,
                            date__gte=min_year,
                            date__lte=max_year,
                            amount__gt=availability)
    
        if sort_param:
            obj = obj.order_by(sort_param)
        context['obj'] = obj

    elif page == 'mouse':
        obj = Mouse.objects.all()

        obj = obj.filter(price__gte=min_price,
                            price__lte=max_price,
                            date__gte=min_year,
                            date__lte=max_year,
                            amount__gt=availability)
    
        if sort_param:
            obj = obj.order_by(sort_param)
        context['obj'] = obj

    elif page == 'keyboard':
        obj = Keyboard.objects.all()


        obj = obj.filter(price__gte=min_price,
                            price__lte=max_price,
                            date__gte=min_year,
                            date__lte=max_year,
                            amount__gt=availability)
    
        if sort_param:
            obj = obj.order_by(sort_param)
        context['obj'] = obj

    context['page'] = page
    context['q'] = q
    context['min_price'] = min_price
    context['max_price'] = max_price
    context['min_year'] = min_year
    context['max_year'] = max_year    
    context['availability'] = availability
    context['sort'] = sort_param     
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render(request,'product-grid.html',context)
        return JsonResponse({'html':html.content.decode('utf-8')})
    else:
        return render(request, 'catalog.html', context)


def info(request,pk):
    
    elem = SharedID.objects.get(id = pk)
    average_rating = Review.objects.filter(product=elem).aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating,1)
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
    total_sum = 0
    #Если запрос пришел с AJAX, то добавляем/убавляем количество товара в корзине
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        item_id = data.get('product_id')
        value = data.get('value')
        cart_item = get_object_or_404(CartItem, id=item_id)

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
            'price': round(details.price,2),
            'quantity': item.quantity,
            'result': round(details.price * item.quantity,2),
        }

        if item.first_image is not None:
            item_details['image'] = item.first_image.image.url
        else:
            item_details['image'] = static('/images/placeholder.jpg')

        items_with_details.append(item_details) 

    for elem in items_with_details:
        total_sum +=elem['result']

    total_sum = round(total_sum,2)

    context = {'cart_products':cart_products, 
                'items_with_details':items_with_details, 'total_sum':total_sum}
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
    elem = SharedID.objects.get(id = pk)
    reviews = elem.review_set.all().order_by('-created')
    context = {'reviews':reviews, "pk":pk}
    return render(request, 'reviews.html', context)

@login_required(login_url='/login')
@user_passes_test(staff_not_allowed, login_url='/login')
def postReview(request, pk):
    if request.method == 'POST':
        Review.objects.create(
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
@user_passes_test(only_for_staff, login_url='/login')
def addProduct(request,product_type):
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
                    ProductImage.objects.create(
                        shared_id=related_data,
                        image=pic
                    )
                except Exception as e:
                    messages.error(request, "Произошла ошибка при загрузке изображения.")
            return JsonResponse({'redirect':reverse('catalog',kwargs={'page':product_type}) })
        else:
            errors = form.errors
            messages.error(request, 'Error')
            context = {'form': form,'errors': errors, 'product_type':product_type}
            html = render(request, 'add_product_form_innerHTML.html',context)
            return JsonResponse({'html':html.content.decode('utf-8')})
    else:
        if product_type == 'mouse':
            form = MouseForm()
        elif product_type == 'keyboard':
            form = KeyboardForm()
        else:
            form = HeadphonesForm()
        context = {'form': form, 'product_type':product_type}

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render(request, 'add_product_form_innerHTML.html', context) 
            return JsonResponse({'html':html.content.decode('utf-8')})
        return render(request, 'add_product.html', context)

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

        form.save()
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
    return render(request, 'edit_form.html', context)

@login_required(login_url='/login')
@user_passes_test(only_for_staff, login_url='/login')
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
        page = 'headphones'

    if request.method == 'POST':
        obj.delete()
        return redirect('catalog', page)
    
    return render(request, 'delete.html', {'obj':obj})

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
        elif data.get('action') == 'decline':
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