from django.contrib import admin
from .models import Company, Copier, DriverFile

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Copier)
class CopierAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'color_mono', 'bit', 'model_name', 'driver_file')
    list_filter = ('color_mono', 'bit')


@admin.register(DriverFile)
class DriverFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')
