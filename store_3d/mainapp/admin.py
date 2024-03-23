from django.contrib import admin
from .models import User, Product, Order, Cart, CartItem

# Регистрация модели User
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'address', 'is_active', 'is_admin', 'at_data')
    search_fields = ('username', 'email', 'phone', 'address')
    list_filter = ('is_active', 'is_admin', 'at_data')
    readonly_fields = ('at_data',)
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)

# Регистрация модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity', 'at_data')
    search_fields = ('name', 'description')
    list_filter = ('at_data',)
    readonly_fields = ('at_data',)
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Product, ProductAdmin)

# Регистрация модели Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'sum_orders', 'quantity', 'at_data')
    search_fields = ('user__username', 'product__name')
    list_filter = ('at_data',)
    readonly_fields = ('at_data',)
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Order, OrderAdmin)

# Регистрация модели Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price')
    search_fields = ('user__username',)
    readonly_fields = ()
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Cart, CartAdmin)

# Регистрация модели CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'name', 'price', 'quantity', 'description')
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ()
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(CartItem, CartItemAdmin)
