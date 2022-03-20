from .models import *
from django.contrib import admin


@admin.register(File)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["file"]

