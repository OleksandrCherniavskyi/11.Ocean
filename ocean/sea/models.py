from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    name = models.CharField(max_length=64)
    origin_image = models.ImageField(upload_to='images/')
    #thumbnail_200 = models.ImageField(null=False, blank=True)
    #thumbnail_400 = models.ImageField(null=False, blank=True)
    #uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.name}"

