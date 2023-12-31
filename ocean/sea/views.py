from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UploadForm, UserCreationForm, CreateUserForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Image
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from PIL import Image as PILImage
from django.contrib.auth.models import Group

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    return HttpResponseRedirect('/image_list')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Basic')
            user.groups.add(group)

            return redirect('login')
    context = {'form': form}
    return render(request, 'sea/register.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("image_list"))
        else:
            return render(request, "sea/login.html", {"message": "Invalid credentials."})
    return render(request, "sea/login.html")

def logout_view(request):
    logout(request)
    return render(request, "sea/login.html", {"message": "Logged out."})


#@login_required
def upload_image(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the form data to create a new Image instance
            new_image = form.save(commit=False)
            new_image.uploaded_by = request.user  # Set the uploaded_by field to the current user
            new_image.save()
            # 200
            # Open the image using PIL
            use_image = PILImage.open(new_image.origin_image.path)

            # Resize the image with antialiasing (ANTIALIAS filter)
            thumbnail_200 = use_image.resize((200, 200), PILImage.ANTIALIAS)
            thumbnail_400 = use_image.resize((400, 400), PILImage.ANTIALIAS)
            # Save the resized image with a different name
            resized_image_filename_200 = f'{new_image.origin_image.name.split(".")[0]}_200.jpg'
            resized_image_path_200 = f'{settings.MEDIA_ROOT}/{resized_image_filename_200}'

            resized_image_filename_400 = f'{new_image.origin_image.name.split(".")[0]}_400.jpg'
            resized_image_path_400 = f'{settings.MEDIA_ROOT}/{resized_image_filename_400}'

            thumbnail_200.save(resized_image_path_200, format="JPEG")
            new_image.thumbnail_200 = resized_image_filename_200
            new_image.save()

            thumbnail_400.save(resized_image_path_400, format="JPEG")
            new_image.thumbnail_400 = resized_image_filename_400
            new_image.save()


            # Close the PIL image
            thumbnail_400.close()
            thumbnail_200.close()
            use_image.close()
            return redirect('image_list')
    else:
        form = UploadForm()
    return render(request, 'sea/upload_image.html', {'form': form})





#@login_required
def image_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    # Retrieve only the images uploaded by the current user
    image_list = Image.objects.filter(uploaded_by=request.user).all()
    thumbnail_200 = Image.objects.filter(
        Q(uploaded_by=request.user, uploaded_by__groups__name='Enterprise') |
        Q(uploaded_by=request.user, uploaded_by__groups__name='Basic') |
        Q(uploaded_by=request.user, uploaded_by__groups__name='Premium')
    ).values('thumbnail_200')


    thumbnail_400 = Image.objects.filter(
        Q(uploaded_by=request.user, uploaded_by__groups__name='Enterprise') |
        Q(uploaded_by=request.user, uploaded_by__groups__name='Premium')
    ).values('thumbnail_400')

    origin_image = Image.objects.filter(
        Q(uploaded_by=request.user, uploaded_by__groups__name='Enterprise') |
        Q(uploaded_by=request.user, uploaded_by__groups__name='Premium')
    ).values('origin_image')

    # Create an empty list to store the resized images

    context = {
        'image_list': image_list,
        'thumbnail_200': thumbnail_200,
        'thumbnail_400': thumbnail_400,
        'origin_image': origin_image

        }
    return render(request, 'sea/image_list.html', context)
