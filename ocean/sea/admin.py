from django.contrib import admin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import path
from django.shortcuts import render, redirect
from .models import Image, ResizeImage
from .forms import ImageSizeForm
from PIL import Image as PILImage
from io import BytesIO

class ImageAdmin(admin.ModelAdmin):
    list_display = ('origin_image', 'uploaded_by')
    list_filter = ('uploaded_by', 'uploaded_by__groups__name')

    actions = ['resize_images']

    def resize_images(self, request, queryset):
        selected_ids = ','.join([str(image.id) for image in queryset])
        return redirect(f'/admin/sea/image/resize/?ids={selected_ids}')

    resize_images.short_description = 'Resize selected images'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('resize/', self.process_resize_form),
        ]
        return custom_urls + urls



    def process_resize_form(self, request):
        if 'ids' in request.GET:
            image_ids = request.GET['ids'].split(',')
            images = Image.objects.filter(id__in=image_ids)

            if request.method == 'POST':
                form = ImageSizeForm(request.POST)
                if form.is_valid():
                    width = form.cleaned_data['width']
                    height = form.cleaned_data['height']

                    for image in images:
                        # Open the original image using PIL
                        img = PILImage.open(image.origin_image.path)

                        # Resize the image
                        img.thumbnail((width, height))

                        # Save the resized image to an in-memory buffer
                        img_io = BytesIO()
                        img.save(img_io, 'JPEG')

                        # Create an InMemoryUploadedFile to save to the ImageField
                        img_file = InMemoryUploadedFile(
                            img_io, None, f'{image.origin_image.name.split(".")[0]}_resized.jpg',
                            'image/jpeg', img_io.tell, None
                        )

                        # Save the resized image to the ResizeImage model
                        resize_image = ResizeImage(
                            origin_image=image,
                            image_resize=img_file
                        )
                        resize_image.save()

                    self.message_user(request, f'Successfully resized {len(images)} image(s).')
                    return redirect('/admin/sea/resizeimage/')
            else:
                form = ImageSizeForm()

            context = {
                'form': form,
                'images': images,
            }
            return render(request, 'admin/resize_images.html', context)


admin.site.register(Image, ImageAdmin)


class ResizeImageAdmin(admin.ModelAdmin):
    list_display = ('image_resize', 'get_origin_image_id')

    def get_origin_image_id(self, obj):
        return obj.origin_image.id

    get_origin_image_id.short_description = 'Origin Image ID'

admin.site.register(ResizeImage, ResizeImageAdmin)

