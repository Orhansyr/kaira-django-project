from django.contrib import admin
from .models import Menu, PageComponent

# Register your models here to make them accessible in the admin panel.

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'url')

@admin.register(PageComponent)
class PageComponentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
