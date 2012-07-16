"""Hooks django-genia models into the Django admin"""

from django.contrib import admin

from genia.models import Generation


class GenerationAdmin(admin.ModelAdmin):
    """Admin for our Generation model"""
    list_display = ['app_name', 'index', 'created', 'last_updated', 'active']
    list_filter = ['app_name',]
    ordering = ['app_name', 'index']
admin.site.register(Generation, GenerationAdmin)