# predictor/urls.py
from django.urls import path
from .views import predict_iris

urlpatterns = [
    # Simplified prediction endpoint
    path('predict/', predict_iris, name='predict'),
]