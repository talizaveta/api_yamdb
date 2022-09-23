from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    list_editable = ('name',)
    search_fields = ('name',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Genre)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    list_editable = ('name',)
    search_fields = ('name',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Title)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'rating',
        'genre',
        'category'
    )
    list_editable = ('name', 'description', 'rating',)
    search_fields = ('name',)
    list_filter = ('name', 'rating', 'genre', 'category',)
    empty_value_display = '-пусто-'
