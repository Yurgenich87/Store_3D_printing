from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.html import escape

class UserManager(BaseUserManager):
    """Manager for user model"""

    def create_user(self, email, username, password=None):
        """Creates a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a new super user"""
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """ Class for users in the system"""
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    at_data = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Product(models.Model):
    """Product model"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    at_data = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)


class Order(models.Model):
    """Order model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_sum = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    at_data = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    """Article model"""
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_html_content(self):
        """Return the content as HTML"""
        return escape(self.content)  # Обработка специальных символов HTML
