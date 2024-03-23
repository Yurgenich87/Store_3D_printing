from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from .views import index, about, contact, register, gallery, login_view, \
    logout_view, profile, edit_profile, delete_profile, manage_products, update_order, delete_order, \
    create_order, orders, manage_orders, update_product, delete_product, articles, product_list, create_product, \
    filter_products, add_to_cart, remove_from_cart, view_cart, store, filter_products_in_cart, randomize_order_dates, \
    filter_order, create_article, contact_form_submit, upload_image

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('contact_form_submit/', contact_form_submit, name='contact_form_submit'),

    path('gallery/', gallery, name='gallery'),
    path('articles/', articles, name='articles'),
    path('create_article/', create_article, name='create_article'),

    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),

    path('products/', manage_products, name='manage_products'),
    path('upload/', upload_image, name='upload_image'),
    path('products_list/', product_list, name='product_list'),
    path('update_product/<int:product_id>/', update_product, name='update_product'),
    path('create_product/', create_product, name='create_product'),
    path('filter_products/<int:days>/', filter_products, name='filter_products'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),

    path('orders/', manage_orders, name='manage_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('update_order/<int:order_id>/', update_order, name='update_order'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('filter_order/<int:days>/', filter_order, name='filter_order'),
    path('randomize_order_dates/', randomize_order_dates, name='randomize_order_dates'),

    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('filter_products_in_cart/<int:days>/', filter_products_in_cart, name='filter_products_in_cart'),
    path('store/', store, name='store'),

    path('', RedirectView.as_view(url='/media/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



