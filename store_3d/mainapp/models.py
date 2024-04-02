from django.contrib.auth.models import AbstractBaseUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager


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
        """Creates and saves a new superuser"""
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    at_data = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='users')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """Returns the username"""
        return self.username

    def has_perm(self, perm, obj=None):
        """Determines if the user has a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """Determines if the user has permissions to view the app 'app_label'."""
        return True

    @property
    def is_staff(self):
        """Determines if the user is a staff member."""
        return self.is_admin


class Category(models.Model):
    """Model representing a category."""
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        """Returns the name of the Category ."""
        return self.name


class Product(models.Model):
    """Model representing a product."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=1)
    image = models.ImageField(upload_to='product_images/')
    at_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the name of the Product."""
        return self.name


class Article(models.Model):
    """Model representing an article."""
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        """Returns the title of the article."""
        return self.title


class Order(models.Model):
    """Order model"""
    PENDING = 'P'
    COMPLETED = 'C'
    CANCELLED = 'X'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    at_data = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    """Model representing a shopping cart."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)



class CartItem(models.Model):
    """Model representing an item in a shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=100)



    def save(self, *args, **kwargs):
        """Override the save method to update name, description, and price based on the linked product."""
        self.name = self.product.name
        self.description = self.product.description
        self.price = self.product.price
        super().save(*args, **kwargs)


class Image(models.Model):
    """Model representing an image."""
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img')

    def __str__(self):
        """String representation of the image object."""
        return self.title

