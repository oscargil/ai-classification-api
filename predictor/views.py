# predictor/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import joblib
import os
import numpy as np
from .serializers import PredictionInputSerializer, PredictionOutputSerializer

# Build paths to the model files dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models_trained', 'iris_model.joblib')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'models_trained', 'iris_class_names.joblib')

# Load model and class names when the app starts
try:
    model = joblib.load(MODEL_PATH)
    class_names = joblib.load(CLASS_NAMES_PATH)
    print("Model and class names loaded successfully.")
except FileNotFoundError:
    model = None
    class_names = None
    print(f"Error: Model files not found at {MODEL_PATH} or {CLASS_NAMES_PATH}")
except Exception as e:
    model = None
    class_names = None
    print(f"Error loading model or class names: {e}")

@api_view(['POST'])
def predict_iris(request):
    """
    Predict iris species from sepal and petal measurements
    """
    # Validate input
    serializer = PredictionInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Prepare input data
    features = np.array([[
        serializer.validated_data['sepal_length'],
        serializer.validated_data['sepal_width'],
        serializer.validated_data['petal_length'],
        serializer.validated_data['petal_width']
    ]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    max_probability = max(probabilities)
    
    # Prepare response
    output_data = {
        'prediction': class_names[prediction],
        'probability': float(max_probability)
    }
    
    output_serializer = PredictionOutputSerializer(data=output_data)
    if output_serializer.is_valid():
        return Response(output_serializer.data)
    return Response(output_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)