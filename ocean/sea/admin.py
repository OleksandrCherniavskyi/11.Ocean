from django.contrib import admin
from .models import Image
# Register your models here.

#admin.site.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('origin_image', 'uploaded_by')
    list_filter = ('uploaded_by','uploaded_by__groups__name')  # Add any filters you need

admin.site.register(Image, ImageAdmin)
