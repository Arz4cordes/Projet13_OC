from django.contrib import admin
from django.urls import path, include

from oc_lettings_site import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
    path('', include('lettings.urls')),
]
