from django.contrib import admin

from models import Generation


class GenerationAdmin(admin.ModelAdmin):
    list_display = ['app_name','index','created','last_updated','active']
    list_filter = ['app_name',]
    ordering = ['app_name','index']
admin.site.register(Generation, GenerationAdmin)