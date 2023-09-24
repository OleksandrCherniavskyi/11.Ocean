from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Image, User
from django.contrib.auth.forms import UserCreationForm
from PIL import Image as PILImage
from django.core.validators import FileExtensionValidator


class UploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['origin_image']
        validators = [
            FileExtensionValidator(allowed_extensions=['png', 'jpg']),
        ]

    def clean_origin_image(self):
        origin_image = self.cleaned_data.get('origin_image')
        if origin_image is None:
            raise ValidationError(_('No chose file.'))
        # Check if the file size is greater than 50 MB (50 * 1024 * 1024 bytes)
        max_size = 10 * 1024 * 1024
        min_size = 0.1  # Minimum file size in bytes
        min_width = 200
        min_height = 200

        if origin_image and origin_image.size > max_size:
            raise ValidationError(_('The file size exceeds the maximum allowed size of 10 MB.'))

        # Check the image dimensions
        img = PILImage.open(origin_image)

        width, height = img.size
        if width < min_width or height < min_height:
            raise ValidationError(_('The image dimensions must be at least 200x200 pixels.'))

        # Check the file size is greater than the minimum (300 bytes)
        if origin_image.size < min_size:
            raise ValidationError(_('The file size is less than the minimum allowed size of 300 bytes.'))

        return origin_image


class ImageSizeForm(forms.Form):
    width = forms.IntegerField(label='Width', required=True)
    height = forms.IntegerField(label='Height', required=True)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']