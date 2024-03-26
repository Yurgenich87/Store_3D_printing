import json
import logging
import os
import random
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.mail import send_mail
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import floatformat
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from rest_framework import generics

from .models import Article, CartItem, Order, Cart, Product, User, Category
from .forms import UserForm, LoginForm, UserProfileForm, OrderForm, ProductForm, ImageForm
from .serializers import UserSerializer, ProductSerializer, OrderSerializer,  CategoriesSerializer

logger = logging.getLogger(__name__)

COMMON_CONTENT = settings.COMMON_CONTENT


# __________________________________________________________API_________________________________________________________
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CategoriesListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


# ________________________________________________________General_____________________________________________________
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Неверный логин или пароль.')
                return redirect('login')
    else:
        form = LoginForm()
    content = {
        'form': form,
        'title': 'Вход',
        **COMMON_CONTENT
    }
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
    """User profile edit menu"""
    user = request.user
    content = {
        'user': user,
        'title': 'Профиль',
        **COMMON_CONTENT
    }

    logger.debug(f"Страница профиля пользователя: {user} успешно загружена!")
    return render(request, 'mainapp/profile.html', content)


def edit_profile(request):
    user = request.user
    logger.debug(f'Пользователь {user} редактирует свой профиль')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
            form.save()
            logger.debug(f'Успешное обновление данных профиля {user}')

            return redirect('profile')
        else:
            logger.error(f'Неверные данные в форме: {form.errors}')
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

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
    cart_products = CartItem.objects.filter(cart__user=user)
    total_price = sum(item.product.price * item.quantity for item in cart_products)
    context = {
        'total_price': total_price,
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


@require_http_methods(["POST", "PUT"])
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST' or request.method == 'PUT':
        product.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


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


# ________________________________________________________Orders_____________________________________________________
def manage_orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'title': 'Мои заказы',
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {context['title']} успешно загружена")
    return render(request, 'mainapp/manage_orders.html', context)


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

            Order.objects.create(
                user=user,
                product=product,
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


@csrf_exempt
@require_POST
def update_order(request, order_id):
    logger.info(f'Updating order data for order {order_id}')
    order = get_object_or_404(Order, pk=order_id)

    order_form = OrderForm(request.POST, instance=order)

    if order_form.is_valid():
        order_form.save()
        logger.info(f'Order {order.id} successfully updated.')
        return JsonResponse({'message': 'Order updated successfully'}, status=200)
    else:
        errors = order_form.errors
        return JsonResponse({'error': errors}, status=400)


@csrf_exempt
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


# ________________________________________________________Cart_____________________________________________________
@login_required
def view_cart(request):
    user = request.user
    products = Product.objects.filter(cart__user=user).annotate(formatted_price=F('price'))
    cart_products = CartItem.objects.filter(cart__user=user)
    total_price = sum(item.product.price * item.quantity for item in cart_products)
    total_price = intcomma(floatformat(total_price, -2))
    cart_products_length = sum(item.quantity for item in cart_products)
    logger.debug(f" {cart_products_length = } ")
    context = {
        'products': products,
        'cart_products': cart_products,
        'total_price': total_price,
        'cart_products_length': cart_products_length,
        'title': 'Корзина',
        **COMMON_CONTENT
    }

    logger.debug(f"Страница {context['title']} успешно загружена!")

    return render(request, 'mainapp/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            user = request.user
            product = Product.objects.get(pk=product_id)
            quantity = 1  # Устанавливаем количество товара равным 1

            cart, created = Cart.objects.get_or_create(user=user)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            # Вне зависимости от создания нового элемента корзины, создаем заказ
            order = Order(user=user, product=product, at_data=timezone.now())
            order.save()

            # Пересчитываем сумму заказа после добавления товара в корзину
            cart.total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
            cart.save()

            logger.debug(f"Товар {product.id} добавлен в корзину")

            # Получаем текущее количество записей в корзине и отправляем его в ответе
            cart_item_count = cart_item.quantity
            logger.debug(f"cart_item_count {cart_item_count = }, {cart_item.quantity = }")
            return JsonResponse({'success': True, 'cartItemCount': cart_item_count})

        except Exception as e:
            logger.debug(f"Товар {product.id} не добавлен в корзину: {e}")
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        try:
            user = request.user
            product = Product.objects.get(pk=product_id)
            cart = Cart.objects.get(user=user)
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()

            if cart_item:
                cart_item.quantity -= 1

                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()

                logger.debug(f"Товар {product.id} удален из корзины")

                cart.total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
                cart.save()

                order = Order.objects.filter(user=user, status='P').last()

                if order:
                    order.status = 'X'
                    order.save()

                cart_item_count = CartItem.objects.filter(cart=cart).count()
                return JsonResponse({'success': True, 'cartItemCount': cart_item_count})
            else:
                logger.debug(f"Товар {product.id} не найден в корзине")
                return JsonResponse({'success': False, 'error': 'Товар не найден в корзине'})

        except Exception as e:
            logger.debug(f"Ошибка при удалении товара из корзины: {e}")
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def purchase(request):
    user = request.user

    products = Product.objects.filter(cart__user=user).annotate(formatted_price=F('price'))
    cart_products = CartItem.objects.filter(cart__user=user)
    total_price = sum(item.product.price * item.quantity for item in cart_products)
    total_price = intcomma(floatformat(total_price, -2))
    cart_products_length = sum(item.quantity for item in cart_products)

    if request.method == 'POST':
        # Обработка данных формы и выбранного способа оплаты
        payment_method = request.POST.get('payment_method')
        # Дополнительная логика, например, сохранение заказа в базе данных

        # Изменение статуса заказа на "Completed"
        order = Order.objects.filter(user=request.user, status='Pending').last()
        if order:
            order.status = 'Completed'
            order.save()

        # Перенаправление на другую страницу (например, страницу подтверждения заказа)
        return redirect('order_confirmation')
    context = {
        'user': user,
        'products': products,
        'cart_products': cart_products,
        'total_price': total_price,
        'cart_products_length': cart_products_length,
        'title': 'Корзина',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/purchase.html')


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
