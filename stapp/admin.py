from django.contrib import admin
from .models import Prefecture, MstTestStation, TestGame, TestChoice

# django-import-exportsの設定
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats


# Register your models here.


class PrefectureResource(resources.ModelResource):
    class Meta:
        model = Prefecture

class MstTestStationResource(resources.ModelResource):
    class Meta:
        model = MstTestStation



class PrefectureAdmin(ImportExportModelAdmin):
    # django-import-exportsの設定
    resource_class = PrefectureResource
    formats = [base_formats.CSV] # formatsで指定できる
    
    # adminでの表示項目
    list_display = ('prf_no','prf_name')
    ordering = ['prf_no']
    search_fields = ['prf_name']


class MstTestStationAdmin(ImportExportModelAdmin):
    # django-import-exportsの設定
    resource_class = MstTestStationResource
    formats = [base_formats.CSV] # formatsで指定できる
    
    # adminでの表示項目
    list_display = ('no','name_kanji','name_hira','name_kata','first_letter','last_letter','is_ends_n','prf_no','city_name','jr_co_name','rail_name')
    ordering = ['first_letter']
    search_fields = ['first_letter']

class TestGameAdmin(admin.ModelAdmin):
    list_display = ('player','start_station','start_letter','goal_station','goal_letter','start_date','is_finished')

class TestChoiceAdmin(admin.ModelAdmin):
    list_display = ('game', 'station')

admin.site.register(Prefecture, PrefectureAdmin)
admin.site.register(MstTestStation, MstTestStationAdmin)
admin.site.register(TestGame, TestGameAdmin)
admin.site.register(TestChoice, TestChoiceAdmin)