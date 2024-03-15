from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import index, about, contact, register, gallery, login_view, \
    logout_view, profile, edit_profile, delete_profile, manage_products, update_order, delete_order, \
    create_order, orders, manage_orders, update_product, delete_product, articles

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('gallery/', gallery, name='gallery'),
    path('articles/', articles, name='articles'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('products/', manage_products, name='manage_products'),
    path('update_product/<int:product_id>/', update_product, name='update_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('orders/', manage_orders, name='manage_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('update_order/<int:order_id>/', update_order, name='update_order'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

