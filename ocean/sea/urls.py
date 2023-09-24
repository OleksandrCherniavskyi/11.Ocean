from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_image, image_list,  registerPage, login_view, logout_view, index


urlpatterns = [

    path('', index, name='index'),
    path('login', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registerPage, name='register'),

    path('upload_image', upload_image, name='upload_image'),
    path('image_list', image_list, name='image_list'),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)