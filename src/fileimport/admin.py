from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Warehouse

# Register your models here.
@admin.register(Warehouse)
class WarehouseAdmin(ImportExportModelAdmin):
    list_display = ('id','loan_num','slug','upload_date','submitted')
