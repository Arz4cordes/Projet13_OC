from django.contrib import admin
from django.urls import path, include

from oc_lettings_site import views, sentry_error_example


urlpatterns = [
    path('', views.index, name='index'),
    path('sentry-debug/', sentry_error_example.trigger_error),
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
    path('', include('lettings.urls')),
]
