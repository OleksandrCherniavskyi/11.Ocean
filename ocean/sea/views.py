from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UploadForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Image
from django.urls import reverse
from PIL import Image as PILImage
from io import BytesIO


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'origin_images.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render( request, "login.html", {"message": "Invalid credentials."})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})


def upload_origin_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UploadForm()
    return render(request, {'form': form})


def origin_images(request):

    # getting all the objects of hotel.
    #origin_images = Image.objects.all()
    ## Create a dictionary to store the thumbnail images
    #thumbnails = {}

    #for image in origin_images:
    #    # Open the original image using PIL (Pillow)
    #    img = PILImage.open(image.origin_image)

    #    # Resize the image to a height of 200px while maintaining aspect ratio
    #    img.thumbnail((img.width * 200 // img.height, 200))

    #    # Convert the image to BytesIO
    #    img_bytes = BytesIO()
    #    img.save(img_bytes, format='JPEG')

    #    # Store the thumbnail image in the dictionary
    #    thumbnails[image.id] = img_bytes.getvalue()
    context = {
        'origin_images': Image.objects.all()
    }
    return render(request, 'origin_images.html', context)

def success(request):
    return HttpResponse('successfully uploaded')
