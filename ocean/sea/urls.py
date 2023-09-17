from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_origin_image, origin_images, success, index, login_view, logout_view


urlpatterns = [
    path('', index, name="index"),
    path('login', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('register/', registerPage, name='register'),

    path('upload_origin_image', upload_origin_image, name='image_upload'),
    path('origin_images', origin_images, name='origin_images'),
    path('success', success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)