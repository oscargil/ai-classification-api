# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Simplified API path
    path('api/', include('predictor.urls')),
]
