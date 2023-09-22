from django import forms

from .models import Image



class UploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['origin_image']

class ImageSizeForm(forms.Form):
    width = forms.IntegerField(label='Width', required=True)
    height = forms.IntegerField(label='Height', required=True)

