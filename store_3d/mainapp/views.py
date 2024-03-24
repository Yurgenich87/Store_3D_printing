import json
import logging
import os
import random
from datetime import timedelta, datetime
from os.path import basename

from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Article, CartItem, Order, Cart, Product
from .forms import UserForm, LoginForm, UserProfileForm, OrderForm, ProductForm, ImageForm

logger = logging.getLogger(__name__)

COMMON_CONTENT = settings.COMMON_CONTENT


# ________________________________________________________General_____________________________________________________
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            logger.info(f' Валидация формы успешна')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            logger.debug(f"{user = }")
            if user is not None:
                login(request, user)
                logger.info(f'Пользователь успешно вошел: {user.email}')
                return redirect('index')
            else:
                logger.info(f'Неверная попытка входа с адресом электронной почты: {email}')
                return redirect('login')
    else:
        form = LoginForm()
    content = {
        'form': form,
        'title': 'Вход',
        **COMMON_CONTENT
    }
    logger.debug("Страница входа успешно загружена")
    return render(request, 'mainapp/login.html', content)


def register(request):
    """Registration form"""
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            logger.info(f' Валидация формы успешна')
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            username = form.cleaned_data.get('username')
            logger.info(f'Пользователь {username} успешно создан')
            return redirect('login')
        else:
            logger.info(f'Ошибка валидации формы: {form.errors}')
    content = {
        'form': form,
        'title': 'Регистрация',
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/register.html', content)


def logout_view(request):
    logout(request)
    logger.info('Пользователь успешно вышел из системы')
    return redirect('index')


@login_required
def profile(request):
    """"""
    user = request.user
    content = {
        'user': user,
        'title': 'Страница профиля',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/profile.html', content)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    content = {
        'form': form,
        'title': 'Страница профиля',
        **COMMON_CONTENT
    }
    return render(request, 'mainapp/profile.html', content)


@login_required
def delete_profile(request, user=None):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('index')
    content = {
        'user': user,
        'title': 'Страница профиля',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/profile.html', content)


# ________________________________________________________Menu_____________________________________________________
def index(request):
    """Main page"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('index')

    else:
        form = UserForm()

    content = {
        'form': form,
        'title': 'Главная',

        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/index.html', content)


def gallery(request):
    gallery_folder = r'E:\PYTHON\Store_3d_printing\store_3d\static\img\gallery'
    file_names = os.listdir(gallery_folder)
    gallery_range = range(1, len(file_names) + 1)
    content = {
        'title': 'Галерея',
        'gallery_range': gallery_range,
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/gallery.html', content)


def articles(request):

    articles = Article.objects.all()
    content = {
        'title': 'Статьи',
        'articles': articles,
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/articles.html', content)


def create_article(request):
    context = {
        'title': 'Создание статьи',
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {context['title']} успешно загружена!")
    return render(request, 'mainapp/create_article.html', context)


def contact(request):
    content = {
        'title': 'Контакты',
        **COMMON_CONTENT
    }

    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/contact.html', content, )


# Доработать
@csrf_exempt
def contact_form_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        content = {
            'title': 'Контакты',
            **COMMON_CONTENT
        }
        logger.debug(f'Выполняется отправка сообщения пользователем c email: {email}')
        send_mail(
            subject,
            message,
            email,
            ['store3dzepko'],
            fail_silently=False,
        )
        logger.debug('Сообщение отправлено')
        return JsonResponse({'success': True})


def about(request):
    logger.debug('About page accessed')
    content = {
        'title': 'О нас',
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/about.html', content)


@login_required
def store(request):
    user = request.user
    products = Product.objects.all()
    cart_sum = Cart.objects.filter(user=user).first()
    cart_products = CartItem.objects.filter(cart__user=user)
    context = {
        'cart_sum': cart_sum,
        'products': products,
        'cart_products': cart_products,
        'title': 'Магазин',
        **COMMON_CONTENT
    }

    logger.debug(f"Страница {context['title']} успешно загружена!, Вошел пользователь: {user.id}")
    return render(request, 'mainapp/store.html', context)


# ________________________________________________________Product_____________________________________________________
def manage_products(request):
    products = Product.objects.all()

    content = {
        'title': 'Мои товары',
        'products': products,
        **COMMON_CONTENT
    }

    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/manage_products.html', content)


@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        if request.headers.get('X-CSRFToken') != request.COOKIES.get('csrftoken'):
            return JsonResponse({'error': 'CSRF token mismatch'}, status=403)

        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.save()

            if 'image' in request.FILES:
                image = request.FILES['image']
                product.image.save(image.name, image)
                product.save()

            return JsonResponse({'success': 'Product created successfully'})
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def update_product(request, product_id):
    logger.info(f'Обновление данных продукта {product_id}')
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        text_form = ProductForm(request.POST, instance=product)

        if text_form.is_valid():
            text_form.save()

            if 'image' in request.FILES:
                image = request.FILES['image']
                product.image.save(image.name, image)
                product.save()

            logger.info(f'Продукт {product.name} успешно обновлен.')
            return JsonResponse({'message': 'Product updated successfully'}, status=200)
        else:
            errors = text_form.errors
            return JsonResponse({'error': errors}, status=400)

    else:
        return JsonResponse({'error': 'POST request expected'}, status=405)


def product_list(request):
    products = Product.objects.all()
    data = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
    } for product in products]
    return JsonResponse(data, safe=False)


def filter_products(request, days):
    """Filter products in products """
    try:
        days = int(days)
    except ValueError:
        logger.debug(f'Количечтво дней отсутствует')

    start_date = timezone.now() - timezone.timedelta(days=days)
    logger.debug(f'Фильтр: {start_date = }')

    filtered_products = Product.objects.filter(at_data__gte=start_date)
    products = filtered_products
    content = {
        'title': 'Фильтр товаров',
        'products': products,
        **COMMON_CONTENT
    }
    logger.debug(f"Фильтр в продукции применен успешно!")
    return render(request, 'mainapp/manage_products.html', content)


@require_http_methods(["POST", "PUT"])
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST' or request.method == 'PUT':
        product.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ________________________________________________________Orders_____________________________________________________
def orders(request, pk=None):
    if pk:
        order = get_object_or_404(Order, pk=pk)
        context = {
            'order': order,
            'title': f'Заказ #{order.pk}',
            **COMMON_CONTENT
        }
        template_name = 'mainapp/manage_orders.html'
    else:
        orders = Order.objects.all()
        context = {
            'orders': orders,
            'title': 'Список заказов',
            **COMMON_CONTENT
        }
        template_name = 'mainapp/manage_orders.html'

    return render(request, template_name, context)


def randomize_order_dates(request):
    start_date = timezone.make_aware(datetime(2022, 1, 1, 13, 4, 4))
    end_date = timezone.make_aware(datetime(2024, 3, 18, 13, 4, 4))

    orders = Order.objects.all()
    logger.debug(f"start_date {start_date} end_date: {end_date}")

    for order in orders:
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        order.at_data = random_date
        order.save()

    return HttpResponse("Order dates have been randomized successfully")


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            price_sum = product.price * quantity

            Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                price_sum=price_sum
            )
            return redirect('manage_orders')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'title': 'Создание заказа',
        **COMMON_CONTENT
    }
    return render(request, 'mainapp/create_order.html', context)


def update_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            order.sum_orders = order.product.price * form.cleaned_data['quantity']
            order.save()
            return redirect('manage_orders')

    else:
        form = OrderForm(instance=order)
    context = {
        'form': form,
        'title': 'Редактирование заказа',
        'order': order,
    }

    return render(request, 'mainapp/update_order.html', context)


def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('manage_orders')
    context = {
        'order': order,
        'title': 'Удаление заказа',
        **COMMON_CONTENT
    }
    return render(request, 'mainapp/delete_order.html', context)


@login_required
def filter_order(request, days):
    """Filter products in orders"""
    logger.debug(f'Фильтр: {request = } {days = }')
    try:
        days = int(days)
    except ValueError:
        logger.debug(f'Количество дней отсутствует')

    start_date = timezone.now() - timezone.timedelta(days=days)

    filtered_orders = Order.objects.filter(user=request.user, at_data__gte=start_date)

    unique_products = set()
    unique_orders = []
    for order in filtered_orders:
        if order.product not in unique_products:
            unique_products.add(order.product)
            unique_orders.append(order)

    content = {
        'title': 'Фильтр заказов',
        'orders': unique_orders,
        **COMMON_CONTENT
    }
    logger.debug(f"Фильтр в Ордерах применен успешно!")
    return render(request, 'mainapp/manage_orders.html', content)


def manage_orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'title': 'Мои заказы',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/manage_orders.html', context)


# ________________________________________________________Cart_____________________________________________________
@login_required
def view_cart(request):
    user = request.user
    cartitems = CartItem.objects.filter(cart__user=user)
    total_price = sum(item.product.price * item.quantity for item in cartitems)
    context = {
        'cartitems': cartitems,
        'total_price': total_price,
        'title': 'Корзина',
        **COMMON_CONTENT
    }

    logger.debug(f"Страница {context['title']} успешно загружена!")

    return render(request, 'mainapp/cart.html', context)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
            quantity = 1  # Устанавливаем количество товара равным 1
            sum_orders = product.price * quantity

            cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += quantity
                cart_item.save()
                cart.total_price += sum_orders
                cart.save()
            else:
                order = Order(user=request.user, product=product, quantity=quantity,
                              sum_orders=sum_orders, at_data=timezone.now())
                order.save()

            logger.debug(f"Товар {product.id} добавлен в корзину")

            # Получаем текущее количество записей в корзине и отправляем его в ответе
            cart_item_count = cart_item.quantity
            logger.debug(f"cart_item_count {cart_item_count = }, {cart_item.quantity = }")
            return JsonResponse({'success': True, 'cartItemCount': cart_item_count})

        except Exception as e:
            logger.debug(f"Товар {product.id} не добавлен в корзину: {e}")
            return JsonResponse({'success': False, 'error': str(e)})


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()

            if cart_item:
                cart_item.quantity -= 1

                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()

                logger.debug(f"Товар {product.id} удален из корзины")

                cart_item_count = CartItem.objects.filter(cart=cart).count()
                return JsonResponse({'success': True, 'cartItemCount': cart_item_count})
            else:
                logger.debug(f"Товар {product.id} не найден в корзине")
                return JsonResponse({'success': False, 'error': 'Товар не найден в корзине'})

        except Exception as e:
            logger.debug(f"Ошибка при удалении товара из корзины: {e}")
            return JsonResponse({'success': False, 'error': str(e)})


def filter_products_in_cart(request, days):
    """Filter the products in the shopping cart"""
    try:
        days = int(days)
    except ValueError:
        logger.debug(f'Количечтво дней отсутствует')

    start_date = timezone.now() - timezone.timedelta(days=days)
    logger.debug(f'Фильтр: {start_date = }')

    filtered_products = Product.objects.filter(user=request.user, at_data__gte=start_date)
    products = filtered_products
    content = {
        'title': 'Фильтр товаров',
        'products': products,
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")

    return render(request, 'mainapp/cart.html', content)
