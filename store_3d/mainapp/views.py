import logging
import os
import random
import time
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.mail import send_mail
from django.db.models import F
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest, \
    HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import floatformat
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from rest_framework import generics
from .models import Article, CartItem, Order, Cart, Product, User, Category
from .forms import UserForm, LoginForm, UserProfileForm, OrderForm, ProductForm, ImageForm
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, CategoriesSerializer

logger = logging.getLogger(__name__)

COMMON_CONTENT = settings.COMMON_CONTENT


# __________________________________________________________API_________________________________________________________
class UserListAPIView(generics.ListAPIView):
    """API view to list users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductListAPIView(generics.ListAPIView):
    """API view to list products."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListAPIView(generics.ListAPIView):
    """API view to list orders."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CategoriesListAPIView(generics.ListAPIView):
    """API view to list categories."""
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


# ________________________________________________________General_____________________________________________________
def login_view(request):
    """View function for user login."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User '{user.email}' logged in successfully.")
                return redirect('index')
            else:
                logger.error("Login failed for email: %s", email)
                messages.add_message(request, messages.ERROR, 'Invalid email or password.')
                return redirect('login')
    else:
        form = LoginForm()
    content = {
        'form': form,
        'title': 'Вход',
        **COMMON_CONTENT
    }
    logger.debug(f"Page '{content['title']}' loaded successfully.")
    return render(request, 'mainapp/login.html', content)


def register(request):
    """View function for user registration."""
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            logger.info('Form validation successful')
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            username = form.cleaned_data.get('username')
            logger.info(f'User "{username}" successfully created')
            return redirect('login')
        else:
            logger.info(f'Form validation error: {form.errors}')
    content = {
        'form': form,
        'title': 'Регистрация',
        **COMMON_CONTENT
    }
    logger.debug(f'Page "{content["title"]}" loaded successfully')
    return render(request, 'mainapp/register.html', content)


def logout_view(request):
    """View function for logging out the user."""
    logout(request)
    logger.debug('User successfully logged out')
    return redirect('index')


@login_required
def profile(request):
    """View function for user profile edit menu."""
    user = request.user
    content = {
        'user': user,
        'title': 'Профиль',
        **COMMON_CONTENT
    }

    logger.debug(f"User profile page for {user} loaded successfully.")
    return render(request, 'mainapp/profile.html', content)


@login_required
def edit_profile(request):
    """View function for editing user profile."""
    user = request.user
    logger.debug(f'User {user} is editing their profile.')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
            form.save()
            logger.debug(f'Profile data for {user} updated successfully.')
            return redirect('profile')
        else:
            logger.error(f'Invalid data in the form: {form.errors}')
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = UserProfileForm(instance=user)

    content = {
        'form': form,
        'title': 'Редактирование профиля',
        **COMMON_CONTENT
    }
    return render(request, 'mainapp/profile.html', content)


@login_required
def delete_profile(request, user=None):
    """View function for deleting user profile."""
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        logger.info(f"User '{user}' profile deleted successfully.")
        return redirect('index')

    content = {
        'user': user,
        'title': 'Удаление профиля',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/profile.html', content)


# ________________________________________________________Menu_____________________________________________________
def index(request):
    """View function for the main page."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("New user registered successfully.")
            return redirect('index')

    else:
        form = UserForm()

    content = {
        'form': form,
        'title': 'Главная',
        **COMMON_CONTENT
    }
    logger.debug(f"Page '{content['title']}' loaded successfully.")
    return render(request, 'mainapp/index.html', content)


def gallery(request):
    """View function for the gallery page."""
    gallery_folder = os.path.join(settings.STATIC_ROOT, 'img', 'gallery')
    file_names = os.listdir(gallery_folder)
    gallery_range = range(1, len(file_names) + 1)
    content = {
        'title': 'Галерея',
        'gallery_range': gallery_range,
        **COMMON_CONTENT
    }
    logger.debug(f"Page '{content['title']}' loaded successfully.")
    return render(request, 'mainapp/gallery.html', content)


def articles(request):
    """View function for displaying articles."""
    articles = Article.objects.all()
    content = {
        'title': 'Статьи',
        'articles': articles,
        **COMMON_CONTENT
    }
    logger.debug(f"Page '{content['title']}' loaded successfully.")
    return render(request, 'mainapp/articles.html', content)


def create_article(request):
    """View function for creating an article."""
    context = {
        'title': 'Добавление статьи',
        **COMMON_CONTENT
    }
    logger.debug(f"Page '{context['title']}' loaded successfully.")
    return render(request, 'mainapp/create_article.html', context)


def contact(request):
    """View function for displaying contact page."""
    content = {
        'title': 'Контакты',
        **COMMON_CONTENT
    }

    logger.debug(f"Page '{content['title']}' loaded successfully!")
    return render(request, 'mainapp/contact.html', content)


@csrf_exempt
def contact_form_submit(request):
    """View function for submitting contact form."""
    if request.method == 'POST':
        email = "store3dzepko@mail.ru"
        email_user = request.POST.get('email')
        subject = f"{request.POST.get('name')}, ({email_user})"
        message = request.POST.get('message')

        logger.debug(f'Sending message from user with email: {email_user}')
        send_mail(
            subject,
            message,
            email,
            ['store3dzepko@mail.ru'],
            fail_silently=False,
        )
        logger.debug('Message sent successfully')
        return JsonResponse({'success': True, 'message': 'Message sent successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def about(request):
    """View function for the about page."""
    logger.debug('About page accessed')
    content = {
        'title': 'О нас',
        **COMMON_CONTENT
    }
    logger.debug(f"Page {content['title']} loaded successfully!")
    return render(request, 'mainapp/about.html', content)


@login_required
def store(request):
    """View function for the store page."""
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

    logger.debug(f"Page {context['title']} loaded successfully!, User logged in: {user.id}")
    return render(request, 'mainapp/store.html', context)


# ________________________________________________________Product_____________________________________________________
@login_required
def manage_products(request):
    """View function for managing products."""
    products = Product.objects.all()

    content = {
        'title': 'Мои товары',
        'products': products,
        **COMMON_CONTENT
    }

    logger.debug(f"Page {content['title']} loaded successfully!")
    return render(request, 'mainapp/manage_products.html', content)


@login_required
@csrf_exempt
def create_product(request):
    """View function for creating a new product."""
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


@login_required
@csrf_exempt
def update_product(request, product_id):
    logger.info(f'Updating product data: {product_id}')
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            if 'image' in request.FILES:
                image = request.FILES['image']
                product.image.save(image.name, image)
                product.save()

            logger.info(f'Product {product.name} successfully updated.')
            return JsonResponse({'message': 'Product updated successfully'}, status=200)
        else:
            errors = form.errors
            logger.error(f'Error updating product {product_id}: {errors}')
            return JsonResponse({'error': errors}, status=400)

    else:
        logger.warning(f'Invalid request method for updating product {product_id}: {request.method}')
        return JsonResponse({'error': 'POST request expected'}, status=405)


@require_http_methods(["POST", "PUT"])
def delete_product(request, product_id):
    """View function for deleting a product."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST' or request.method == 'PUT':
        product.delete()
        logger.info(f"Product with ID {product_id} deleted successfully.")
        return JsonResponse({'success': True})
    logger.error("Invalid HTTP method used for delete_product view.")
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def filter_products(request, days):
    """View function to filter products based on a specified number of days."""
    try:
        days = int(days)
        if days > 0:
            start_date = timezone.now() - timezone.timedelta(days=days)
            filtered_products = Product.objects.filter(at_data__gte=start_date)
            products = filtered_products
            content = {
                'title': 'Filter Products',
                'products': products,
                **COMMON_CONTENT
            }
            logger.debug("Filter applied successfully to products!")
            return render(request, 'mainapp/manage_products.html', content)
        else:
            return redirect('manage_products')
    except ValueError:
        logger.error("Invalid number of days provided: %s", days)
        return redirect('manage_products')


# ________________________________________________________Orders_____________________________________________________
@login_required
@csrf_exempt
def manage_orders(request):
    """View function to manage orders."""
    orders = Order.objects.all()

    context = {
        'orders': orders,
        'title': 'My Orders',
        **COMMON_CONTENT
    }

    logger.debug(f"Page {context['title']} loaded successfully.")
    return render(request, 'mainapp/manage_orders.html', context)


def orders(request, pk=None):
    """View function to display orders."""
    if pk:
        order = get_object_or_404(Order, pk=pk)
        context = {
            'order': order,
            'title': f'Order #{order.pk}',
            **COMMON_CONTENT
        }
        template_name = 'mainapp/manage_orders.html'
    else:
        orders = Order.objects.all()
        context = {
            'orders': orders,
            'title': 'Order List',
            **COMMON_CONTENT
        }
        template_name = 'mainapp/manage_orders.html'

    logger.debug(f"Page {context['title']} loaded successfully.")
    return render(request, template_name, context)


def randomize_order_dates(request):
    """View function to randomize order dates."""
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
    """View function for creating an order."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            product = form.cleaned_data['product']

            Order.objects.create(
                user=user,
                product=product,
            )
            logger.info("Order created successfully.")
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
    """View function for updating order data."""
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
    """View function for deleting an order."""
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.delete()
        logger.info(f"Order {order_id} deleted successfully.")
        return redirect('manage_orders')
    context = {
        'order': order,
        'title': 'Удаление заказа',
        **COMMON_CONTENT
    }
    return render(request, 'mainapp/delete_order.html', context)


@login_required
def filter_order(request, days):
    """View function to filter orders based on a specified number of days."""
    try:
        days = int(days)
        if days > 0:
            start_date = timezone.now() - timezone.timedelta(days=days)
            filtered_orders = Order.objects.filter(user=request.user, at_data__gte=start_date)

            unique_products = set()
            unique_orders = []
            for order in filtered_orders:
                if order.product not in unique_products:
                    unique_products.add(order.product)
                    unique_orders.append(order)

            content = {
                'title': 'Filter Orders',
                'orders': unique_orders,
                **COMMON_CONTENT
            }
            logger.debug("Filter applied successfully to orders!")
            return render(request, 'mainapp/manage_orders.html', content)
        else:
            logger.debug("Invalid number of days provided: %s", days)
            return render(request, 'mainapp/manage_orders.html', {'title': 'Filter Orders', **COMMON_CONTENT})
    except ValueError:
        logger.error("Invalid number of days provided: %s", days)
        return render(request, 'mainapp/manage_orders.html', {'title': 'Filter Orders', **COMMON_CONTENT})


# ________________________________________________________Cart_____________________________________________________
@login_required
def view_cart(request):
    """View function for displaying the user's cart."""
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
        'title': 'Cart',
        **COMMON_CONTENT
    }

    logger.debug(f"Page {context['title']} loaded successfully!")
    return render(request, 'mainapp/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """View function for adding a product to the user's cart."""
    if request.method == 'POST':
        try:
            user = request.user
            product = Product.objects.get(pk=product_id)
            quantity = 1  # Set the quantity of the product to 1

            cart, created = Cart.objects.get_or_create(user=user)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            # Regardless of creating a new cart item, create an order
            order = Order(user=user, product=product, at_data=timezone.now())
            order.save()

            # Recalculate the total price of the cart after adding the product
            cart.total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
            cart.save()

            logger.debug(f"Product {product.id} added to the cart")

            # Get the current number of items in the cart and send it in the response
            cart_item_count = cart_item.quantity
            logger.debug(f"cart_item_count {cart_item_count = }, {cart_item.quantity = }")
            return JsonResponse({'success': True, 'cartItemCount': cart_item_count})

        except Exception as e:
            logger.debug(f"Product {product_id} not added to the cart: {e}")
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def remove_from_cart(request, product_id):
    """View function for removing a product from the user's cart."""
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

                logger.debug(f"Product {product.id} removed from the cart")

                cart.total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
                cart.save()

                order = Order.objects.filter(user=user, status='P').last()

                if order:
                    order.status = 'X'
                    order.save()

                cart_item_count = CartItem.objects.filter(cart=cart).count()
                return JsonResponse({'success': True, 'cartItemCount': cart_item_count})

        except Exception as e:
            logger.debug(f"Error removing product from the cart: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


def filter_products_in_cart(request, days):
    """View function to filter products in the shopping cart."""
    try:
        days = int(days)
    except ValueError:
        logger.debug(f'Number of days is missing')

    start_date = timezone.now() - timezone.timedelta(days=days)
    logger.debug(f'Filter: {start_date = }')

    filtered_products = Product.objects.filter(user=request.user, at_data__gte=start_date)
    products = filtered_products
    content = {
        'title': 'Filter Products',
        'products': products,
        **COMMON_CONTENT
    }
    logger.debug(f"Page {content['title']} loaded successfully!")

    return render(request, 'mainapp/cart.html', content)


@login_required
def purchase(request):
    """View function for processing the purchase of items in the user's cart."""
    user = request.user

    products = Product.objects.filter(cart__user=user).annotate(formatted_price=F('price'))
    cart_products = CartItem.objects.filter(cart__user=user)
    total_price = sum(item.product.price * item.quantity for item in cart_products)
    total_price = intcomma(floatformat(total_price, -2))
    cart_products_length = sum(item.quantity for item in cart_products)

    if request.method == 'POST':
        try:
            payment_method = request.POST.get('payment_method')

            order = Order.objects.filter(user=request.user, status='Pending').last()
            if order:
                order.status = 'Completed'
                order.save()

            return redirect('order_confirmation')
        except Exception as e:
            logger.error(f"Error processing purchase: {e}")

    context = {
        'user': user,
        'products': products,
        'cart_products': cart_products,
        'total_price': total_price,
        'cart_products_length': cart_products_length,
        'title': 'Корзина',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/purchase.html', context)


@csrf_exempt
@login_required
def process_payment(request):
    user = request.user
    logger.info(f'{user =}')
    cart = Cart.objects.get(user=user)

    cart_items = cart.cartitem_set.all()
    cart_items.delete()
    logger.debug(f'Корзина успешно очищена, после покупки')

    Order.objects.filter(user=user).update(status=Order.COMPLETED)
    logger.debug(f'Статус ордера изменен на: COMPLETED')

    response_data = {'redirect_url': '/store/'}
    return JsonResponse(response_data)
