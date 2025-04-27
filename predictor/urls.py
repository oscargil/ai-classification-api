# predictor/urls.py
from django.urls import path
from .views import PredictIrisView

urlpatterns = [
    # Define the URL pattern for the prediction view
    path('predict/', PredictIrisView.as_view(), name='predict_iris'),
]