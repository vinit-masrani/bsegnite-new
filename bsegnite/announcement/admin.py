from django.contrib import admin

# Register your models here.
from .models import Announcement
from .models import Category
from .models import Company

class AnnouncementAdmin(admin.ModelAdmin):
	list_display=["ca_id","ca_head","ct","su","ca_datetime","get_c_name"]
	list_editable=["ct","su"]
	list_filter=["ct_id","ca_datetime"]
	search_fields=["ca_head","ca_datetime","ca_desc"]
	class Meta:
		model=Announcement
	def get_c_name(self,object):
		return object.c.c_name
	get_c_name.short_description='Compnay Name'
	# def get_ct_name(self,object):
	# 	return object.ct.ct_name
	# get_ct_name.short_description='Category Name'

class CompanyAdmin(admin.ModelAdmin):
	list_display=["c_id","c_acro","c_name","c_isin","c_indus"]
	list_filter=["c_indus"]
	search_fields=["c_id","c_acro","c_name","c_isin","c_indus"]
	class Meta:
		model=Company

class CategoryAdmin(admin.ModelAdmin):
	list_display=["ct_id","ct_name"]
	search_fields=["ct_id","ct_name"]
	class Meta:
		model=Category

admin.site.register(Announcement,AnnouncementAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Category,CategoryAdmin)
