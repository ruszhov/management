from django.contrib import admin
from .models import *
# Register your models here.

class FileAdmin(admin.ModelAdmin):
	list_display = [field.name for field in File._meta.fields]
	search_fields = ['title', 'file']

	class Meta:
		model = File
admin.site.register(File, FileAdmin)