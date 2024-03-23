from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils import timezone

from ..models import User, Order, Cart, CartItem, Product
from ..views import login_view

User = get_user_model()


class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpassword')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(email='admin@example.com', username='admin', password='adminpassword')
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertEqual(admin.username, 'admin')
        self.assertTrue(admin.check_password('adminpassword'))
        self.assertTrue(admin.is_admin)


class ProductModelTestCase(TestCase):
    def test_product_creation(self):
        current_time = timezone.now()
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100,
            quantity=10,
            at_data=current_time
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.price, 100)
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.at_data.replace(microsecond=0), current_time.replace(microsecond=0))


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=100, quantity=10)

    def test_order_creation(self):
        order = Order.objects.create(user=self.user, product=self.product, sum_orders=200, quantity=2)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.sum_orders, 200)
        self.assertEqual(order.quantity, 2)


class CartModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=100, quantity=10)

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)

    def test_cart_item_creation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, self.product)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='ivan@mail.ru', username='testuser', password='testpassword')

    def test_login_successful(self):
        request = self.factory.post(reverse('login'), {'email': 'test@example.com', 'password': 'testpassword'})
        request.session = {}
        response = login_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, reverse('index'))

    def test_login_invalid_credentials(self):
        # Simulate a POST request with invalid login credentials
        data = {'email': 'invalid@example.com', 'password': 'wrongpassword'}
        request = self.factory.post(reverse('login'), data=data)
        response = login_view(request)

        # Check if redirect occurred
        self.assertEqual(response.status_code, 200)
        # Check if redirected back to the login page (change to your expected redirect URL)
        self.assertEqual(response.url, reverse('login'))

    def test_login_get_request(self):
        # Simulate a GET request to the login page
        request = self.factory.get(reverse('login'))
        response = login_view(request)

        # Check if the view returns a successful response
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'mainapp/login.html')


class StoreViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='ivan@mail.ru', username='ivan', password='password')
        self.product1 = Product.objects.create(name='Product 1', description='Product 1', price=10, quantity=2)
        self.product2 = Product.objects.create(name='Product 2', description='Product 2', price=440, quantity=20)
        self.order1 = Order.objects.create(user=self.user, product=self.product1, sum_orders=200, quantity=2)
        self.order2 = Order.objects.create(user=self.user, product=self.product2, sum_orders=10, quantity=1)

    def test_store_view_authenticated(self):
        # Log in the user
        self.client.login(username='ivan@mail.ru', password='password')

        # Access the store view
        response = self.client.get(reverse('store'))

        # Check response status and template used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/store.html')

        # Check if products are in the response context
        self.assertTrue('products' in response.context)
        self.assertTrue('cart_products' in response.context)

        # Check the number of products in the context
        self.assertEqual(len(response.context['products']), 2)
        self.assertEqual(len(response.context['cart_products']), 2)

        # Check if product names are in the response content
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

    def test_store_view_unauthenticated(self):
        # Access the store view without logging in
        response = self.client.get(reverse('store'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'store')
