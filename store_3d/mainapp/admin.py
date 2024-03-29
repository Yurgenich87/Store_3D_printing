from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Order, Cart, CartItem, Category


@admin.action(description="Сбросить количество в ноль")
def reset_quantity(modeladmin, request, queryset):
    """Admin action to reset the quantity of selected items to zero"""
    queryset.update(quantity=0)


class CustomUserAdmin(UserAdmin):
    """User model registration"""
    list_display = ('username', 'email', 'phone', 'is_active', 'is_admin', 'at_data')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'is_admin', 'at_data')
    readonly_fields = ('at_data',)
    filter_horizontal = ('groups',)
    fieldsets = (
        ('Пользователь', {
            'fields': ('username', 'email', 'password', 'is_admin', 'is_active')
        }),
        ('Группа', {
            'fields': ('groups',)
        }),
        ('Адресная информация', {
            'fields': ('city', 'region', 'street', 'postal_code', 'phone')
        }),
        ('ФИО', {
            'fields': ('first_name', 'last_name', 'patronymic_name')
        }),
    )


admin.site.register(User, CustomUserAdmin)


class ProductAdmin(admin.ModelAdmin):
    """Product model registration"""
    list_display = ('name', 'description', 'price', 'quantity', 'at_data')
    search_fields = ('name', 'description')
    filter_horizontal = ()
    actions = [reset_quantity]
    fieldsets = (
        ('Товар', {
            'fields': ('name', 'price',)
        }),
        ('Категория', {
            'fields': ('category',)
        }),
        ('Описание', {
            'fields': ('description', 'at_data')
        }),
        ('Количество', {
            'fields': ('quantity',)
        }),
    )


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    """Model Order Registration"""
    list_display = ('user', 'product', 'at_data')
    search_fields = ('user__username', 'product__name')
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Order, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    """Cart model registration"""
    list_display = ('user', 'total_price')
    search_fields = ('user__username',)

    def get_readonly_fields(self, request, obj=None):
        """Gets a list of read-only fields"""
        if obj:
            return self.readonly_fields + tuple([field.name for field in obj._meta.fields])
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        """Checks to see if there is authorization to change the facility"""
        if obj:
            return False
        return True


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    """Registering a CartItem model"""
    list_display = ('product', 'name', 'price', 'quantity', 'description')
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ()
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(CartItem, CartItemAdmin)


class CategoryAdmin(admin.ModelAdmin):
    """Product model registration"""
    list_display = ('name', )
    search_fields = ('name', )
    filter_horizontal = ()
    fieldsets = (
        ('Наименование категории', {
            'fields': ('name', )
        }),
    )


admin.site.register(Category, CategoryAdmin)
