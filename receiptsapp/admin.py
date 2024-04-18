from django.contrib import admin
from .models import Receipt, Category


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'time_to_cook')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)