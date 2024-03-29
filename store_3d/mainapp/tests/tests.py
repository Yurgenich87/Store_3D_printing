import io
import json
import os

from django.core import mail
from django.db.models import Sum
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model
from ..forms import UserForm
from ..models import User, Order, Cart, CartItem, Product, Article, Category
import logging

logger = logging.getLogger(__name__)


# class TestLoginView(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.login_url = reverse('login')
#         self.index_url = reverse('index')
#         self.user = User.objects.create(email='test@test.com', username='testuser', password=make_password('testpassword'))
#
#     def test_login_view_get(self):
#         """
#         Test GET request to login view.
#         """
#         response = self.client.get(self.login_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/login.html')
#
#     def test_login_view_post_valid(self):
#         """
#         Test POST request to login view with valid credentials.
#         """
#         response = self.client.post(self.login_url, {'email': 'test@test.com', 'password': 'testpassword'})
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.index_url)
#
#     def test_login_view_post_invalid(self):
#         """
#         Test POST request to login view with invalid credentials.
#         """
#         response = self.client.post(self.login_url, {'email': 'test@test.com', 'password': 'wrongpassword'})
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.login_url)
#         messages = list(response.wsgi_request._messages)
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Invalid email or password.')
#
#
# class TestRegisterView(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.register_url = reverse('register')
#         self.login_url = reverse('login')
#         self.user_data = {
#             'username': 'testuser',
#             'password': 'testpassword',
#             'email': 'test@test.com',
#             'phone': '1234567890'
#         }
#
#     def test_register_view_get(self):
#         """
#         Test GET request to register view.
#         """
#         response = self.client.get(self.register_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/register.html')
#
#     def test_register_view_post_valid(self):
#         """
#         Test POST request to register view with valid form data.
#         """
#         form_data = {
#             'username': 'testuser',
#             'password': 'testpassword',
#             'email': 'test@test.com',
#             'phone': '1234567890'
#         }
#         response = self.client.post(self.register_url, form_data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.login_url)
#
#     def test_register_view_post_invalid(self):
#         """
#         Test POST request to register view with invalid data.
#         """
#         invalid_data = self.user_data.copy()
#         invalid_data['username'] = ''
#         response = self.client.post(self.register_url, invalid_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required.', html=True)
#         self.assertFalse(User.objects.filter(username='testuser').exists())
#
#
#     class Meta:
#         verbose_name = "Test Register View"
#
#
# class TestLogoutView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.logout_url = reverse('logout')
#         self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(username='testuser', password='12345')
#
#     def test_logout_view(self):
#         """
#         Test logging out the user.
#         """
#         response = self.client.get(self.logout_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('index'))
#         self.assertNotIn('_auth_user_id', self.client.session)
#
#
# class TestProfileView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.profile_url = reverse('profile')
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#
#     def test_profile_view_authenticated(self):
#         """
#         Test loading the profile page for authenticated user.
#         """
#         response = self.client.get(self.profile_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Профиль')
#         self.assertTemplateUsed(response, 'mainapp/profile.html')
#
#
# class TestEditProfileView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.edit_profile_url = reverse('edit_profile')
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#
#     def test_edit_profile_view_get(self):
#         """
#         Test loading the edit profile page with GET request.
#         """
#         response = self.client.get(self.edit_profile_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Редактирование профиля')
#         self.assertTemplateUsed(response, 'mainapp/profile.html')
#
#
# class TestDeleteProfileView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.delete_profile_url = reverse('delete_profile')
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#
#     def test_delete_profile_view_get(self):
#         """
#         Test loading the delete profile page with GET request.
#         """
#         response = self.client.get(self.delete_profile_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Удаление профиля')
#
#     def test_delete_profile_view_post(self):
#         """
#         Test deleting the user profile with POST request.
#         """
#         response = self.client.post(self.delete_profile_url)
#         self.assertRedirects(response, reverse('index'))
#         self.assertFalse(User.objects.filter(username='testuser').exists())
#
#
# class TestIndexView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.index_url = reverse('index')
#
#     def test_index_view_get(self):
#         """
#         Test loading the index page with a GET request.
#         """
#         response = self.client.get(self.index_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/index.html')
#         self.assertIn('form', response.context)
#         self.assertIsInstance(response.context['form'], UserForm)
#
#     def test_index_view_post_valid_form(self):
#         """
#         Test submitting a valid form to the index page.
#         """
#         form_data = {
#             'username': 'testuser',
#             'password': 'testpassword',
#             'email': 'test@test.com',
#             'phone': '1234567890'
#         }
#         response = self.client.post(self.index_url, form_data)
#         self.assertRedirects(response, self.index_url)
#
#     def test_index_view_post_invalid_form(self):
#         """
#         Test submitting an invalid form to the index page.
#         """
#         invalid_form_data = {
#             'username': 'testuser',
#             'password': 'testpassword'
#         }
#         response = self.client.post(self.index_url, invalid_form_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/index.html')
#         self.assertIn('form', response.context)
#         form = response.context['form']
#         self.assertIsInstance(form, UserForm)
#         self.assertTrue(form.errors)
#
#
# class TestCreateArticleView(TestCase):
#     def test_create_article_view_get(self):
#         """Test loading the create article page with a GET request."""
#         response = self.client.get(reverse('create_article'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/create_article.html')
#         self.assertIn('title', response.context)
#         self.assertEqual(response.context['title'], 'Добавление статьи')
#
#     # You can add more tests here for POST requests, form submission, etc.
#
#
# class TestStoreView(TestCase):
#     def setUp(self):
#         # Create a user
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
#         # Create a category
#         category = Category.objects.create(name='Category')
#
#         # Create some products
#         self.product1 = Product.objects.create(name='Product 1', price=10)
#         self.product2 = Product.objects.create(name='Product 2', price=20)
#
#         # Create a cart for the user
#         self.cart = Cart.objects.create(user=self.user)
#
#         # Add products to the cart
#         self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
#         self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)
#
#         # Create a request factory
#         self.factory = RequestFactory()
#
#     def test_store_view_authenticated_user(self):
#         """Test loading the store page for authenticated user."""
#         # Set the user as authenticated
#         self.client.force_login(self.user)
#
#         # Send a GET request to the store page
#         response = self.client.get(reverse('store'))
#
#         # Check if the response is successful
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/store.html')
#
#
# class TestManageProductsView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#
#         # Create a category with id=1
#         self.category = Category.objects.create(id=1, name='Category')
#
#         # Create some products for testing
#         self.product1 = Product.objects.create(name='Product 1', price=10, category=self.category)
#         self.product2 = Product.objects.create(name='Product 2', price=20, category=self.category)
#
#     def test_manage_products_view_authenticated_user(self):
#         """Test loading the manage products page for an authenticated user."""
#         response = self.client.get(reverse('manage_products'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/manage_products.html')
#         # Check if products are in the context
#         self.assertIn('products', response.context)
#         # Check if the correct products are in the context
#         products_in_context = response.context['products']
#         self.assertIn(self.product1, products_in_context)
#         self.assertIn(self.product2, products_in_context)
#
#     def test_manage_products_view_unauthenticated_user(self):
#         """Test loading the manage products page for an unauthenticated user."""
#         # Logout the user
#         self.client.logout()
#         response = self.client.get(reverse('manage_products'))
#         self.assertEqual(response.status_code, 302)
#         # Check if the redirection URL contains '/login/' without 'next' parameter
#         self.assertRedirects(response, '/login/?next=/products/')
#
#
# class TestUpdateProductView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#         self.category = Category.objects.create(id=1, name='Category')
#
#     def test_update_product_valid_data(self):
#         """Test updating product with valid data."""
#         product = Product.objects.create(
#             name='Test Product',
#             description='Test Description',
#             price=10,
#             quantity=5,
#             category=self.category,
#             image='path/to/image.jpg'
#         )
#
#         post_data = {
#             'name': 'Updated Product',
#             'description': 'Updated Description',
#             'price': 20,
#             'quantity': 10,
#             'category': self.category.id,
#         }
#         response = self.client.post(reverse('update_product', kwargs={'product_id': product.id}), post_data)
#         response_json = json.dumps(response.json(), indent=4)
#         logger.debug(f'Response JSON: {response_json}')
#
#         self.assertEqual(response.status_code, 200)
#
#         product.refresh_from_db()
#         self.assertEqual(product.name, 'Updated Product')
#         self.assertEqual(product.description, 'Updated Description')
#         self.assertEqual(product.price, 20)
#         self.assertEqual(product.quantity, 10)
#         self.assertEqual(product.category, self.category)
#
#
#     def test_update_product_invalid_data(self):
#         """Test updating product with invalid data."""
#         product = Product.objects.create(name='Test Product', price=10, category=self.category)
#
#         post_data = {
#             'price': 20,
#         }
#         response = self.client.post(reverse('update_product', kwargs={'product_id': product.id}), post_data)
#
#         self.assertEqual(response.status_code, 400)
#
#         # Check if product data remains unchanged
#         product.refresh_from_db()
#         self.assertEqual(product.name, 'Test Product')
#         self.assertEqual(product.price, 10)
#
#     def test_update_product_nonexistent_id(self):
#         """Test updating non-existent product."""
#         response = self.client.post(reverse('update_product', kwargs={'product_id': 999}))
#
#         self.assertEqual(response.status_code, 404)
#
#
# class CreateOrderViewTest(TestCase):
#     def setUp(self):
#         """Set up the test environment."""
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#
#     def test_create_order_view_get(self):
#         """Test GET request to the create order view."""
#         response = self.client.get(reverse('create_order'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/create_order.html')
#         self.assertIn('form', response.context)
#         self.assertIn('title', response.context)
#         self.assertEqual(response.context['title'], 'Создание заказа')
#
#     def test_create_order_view_post_valid_data(self):
#         # Prepare form data to be sent
#         form_data = {
#             'user': self.user.pk,
#             'product': 'some_product_id'
#         }
#
#         # Send a POST request with form data
#         response = self.client.post(reverse('create_order'), form_data)
#
#         # Check the response status code
#         self.assertEqual(response.status_code, 200)
#
#     def test_create_order_view_post_invalid_data(self):
#         """Test POST request with invalid data to the create order view."""
#         form_data = {
#             'user': '',
#             'product': '',
#         }
#         response = self.client.post(reverse('create_order'), data=form_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mainapp/create_order.html')
#         self.assertIn('form', response.context)
#         self.assertIn('title', response.context)
#         self.assertEqual(response.context['title'], 'Создание заказа')
#
#         # Optionally, assert that no order was created in the database
#         self.assertFalse(Order.objects.exists())
#
#
# class AddToCartViewTestCase(TestCase):
#     def setUp(self):
#         """Set up the test environment."""
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#         self.product = Product.objects.create(name='Test Product', price=10)
#
#     def test_add_to_cart_success(self):
#         """Test adding a product to the cart successfully."""
#         response = self.client.post(reverse('add_to_cart', kwargs={'product_id': self.product.pk}))
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content.decode('utf-8'))
#         self.assertTrue(data['success'])
#         self.assertEqual(data['cartItemCount'], 1)
#
#         # Check if the order is created
#         self.assertTrue(Order.objects.filter(user=self.user, product=self.product).exists())
#
#         # Check if the cart and cart item are created or updated
#         cart = Cart.objects.get(user=self.user)
#         self.assertTrue(CartItem.objects.filter(cart=cart, product=self.product, quantity=1).exists())
#
#     def test_add_to_cart_error(self):
#         """Test error handling when adding a product to the cart."""
#         # Ensure that an invalid product ID is used to trigger an exception
#         invalid_product_id = 9999999
#         response = self.client.post(reverse('add_to_cart', kwargs={'product_id': invalid_product_id}))
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content.decode('utf-8'))
#         self.assertFalse(data['success'])
#         self.assertIn('error', data)
#
#     def tearDown(self):
#         """Clean up after the test."""
#         User.objects.all().delete()
#         Product.objects.all().delete()
#         Cart.objects.all().delete()
#         Order.objects.all().delete()
#
#
# class RemoveFromCartViewTestCase(TestCase):
#     def setUp(self):
#         """Set up the test environment."""
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#         self.client.login(email='test@example.com', password='12345')
#         self.product = Product.objects.create(name='Test Product', price=10)
#         self.cart = Cart.objects.create(user=self.user)
#         self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
#
#     def test_remove_from_cart_success(self):
#         """Test removing a product from the cart successfully."""
#         response = self.client.post(reverse('remove_from_cart', kwargs={'product_id': self.product.pk}))
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content.decode('utf-8'))
#         self.assertTrue(data['success'])
#         self.assertEqual(data['cartItemCount'], 0)
#         self.assertFalse(CartItem.objects.filter(cart=self.cart, product=self.product).exists())
#
#     def test_remove_from_cart_product_not_found(self):
#         """Test removing a product that is not found in the cart."""
#         invalid_product_id = 9999999
#         response = self.client.post(reverse('remove_from_cart', kwargs={'product_id': invalid_product_id}))
#         self.assertEqual(response.status_code, 500)
#         data = json.loads(response.content.decode('utf-8'))
#         self.assertFalse(data['success'])
#         self.assertIn('error', data)
#
#     def tearDown(self):
#         """Clean up after the test."""
#         User.objects.all().delete()
#         Product.objects.all().delete()
#         Cart.objects.all().delete()
#         Order.objects.all().delete()


class ContactFormSubmitTest(TestCase):

    def test_contact_form_submit_success(self):
        # Create a client to send requests
        client = Client()

        # Send a POST request
        response = client.post(reverse('contact_form_submit'), {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'John Doe, (johndoe@example.com)',
            'message': 'Test Message'
        })

        # Check if JSON response indicates successful submission
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'success': True, 'message': 'Message sent successfully'}
        )

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'John Doe, (johndoe@example.com)')  # <-- Check subject value
        self.assertEqual(mail.outbox[0].body, 'Test Message')
        self.assertEqual(mail.outbox[0].from_email, 'store3dzepko@mail.ru')
        self.assertEqual(mail.outbox[0].to, ['store3dzepko@mail.ru'])

    def test_contact_form_submit_invalid_method(self):
        # Make a GET request to the view
        response = self.client.get(reverse('contact_form_submit'))

        # Assert that the response status code is 405 (Method Not Allowed)
        self.assertEqual(response.status_code, 405)

        # Assert that the response contains the expected error message
        expected_data = {'success': False, 'message': 'Invalid request method'}
        self.assertJSONEqual(response.content, expected_data)
        # Check if no email was sent
        self.assertEqual(len(mail.outbox), 0)


