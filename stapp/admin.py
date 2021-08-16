from django.contrib import admin
from .models import Prefecture

# django-import-exportsの設定
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats


# Register your models here.


class PrefectureResource(resources.ModelResource):
    class Meta:
        model = Prefecture


class PrefectureAdmin(ImportExportModelAdmin):
    # django-import-exportsの設定
    resource_class = PrefectureResource
    formats = [base_formats.CSV] # formatsで指定できる
    
    # adminでの表示項目
    list_display = ('id','prf_no','prf_name')
    list_filter = ['prf_no']
    search_fields = ['prf_name']

admin.site.register(Prefecture, PrefectureAdmin)