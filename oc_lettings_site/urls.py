from django.contrib import admin
from django.urls import path, include

from oc_lettings_site import views


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


urlpatterns = [
    path('', views.index, name='index'),
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
    path('', include('lettings.urls')),
]
