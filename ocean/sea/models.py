
from django.db import models
from django.contrib.auth.models import User




class Image(models.Model):

    origin_image = models.ImageField(blank=True)
    thumbnail_200 = models.ImageField(blank=True)
    thumbnail_400 = models.ImageField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.origin_image)


class ResizeImage(models.Model):
    image_resize = models.ImageField(blank=True, upload_to='resized/')
    origin_image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.image_resize)