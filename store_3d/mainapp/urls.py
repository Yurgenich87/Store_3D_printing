from django.urls import path

from .views import index, about, contact, register, gallery, login_view, \
    logout_view, profile, edit_profile, delete_profile, manage_products, manage_orders

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('gallery/', gallery, name='gallery'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('products/', manage_products, name='manage_products'),
    path('orders/', manage_orders, name='manage_orders'),
    path('orders/', manage_orders, name='manage_orders'),
]

