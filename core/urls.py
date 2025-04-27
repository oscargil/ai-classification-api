# core/urls.py
from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the URLs from the predictor app under the 'api/predictor/' namespace
    path('api/predictor/', include('predictor.urls')),
]
