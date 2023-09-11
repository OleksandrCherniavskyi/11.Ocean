from django.shortcuts import render, redirect
from .forms import UploadForm
from django.http import HttpResponse

def origin_image_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UploadForm()
    return render(request, {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')
