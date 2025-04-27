# predictor/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
import os
import numpy as np
from .serializers import IrisFeaturesSerializer

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


class PredictIrisView(APIView):
    """
    API View to predict Iris species using the trained model.
    Accepts POST requests with flower features.
    """
    def post(self, request, *args, **kwargs):
        if model is None or class_names is None:
             return Response(
                {"error": "Model not loaded correctly. Check server logs."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = IrisFeaturesSerializer(data=request.data)
        if serializer.is_valid():
            # Get validated data
            features = serializer.validated_data
            # Convert to numpy array format expected by the model (2D array)
            input_data = np.array([[
                features['sepal_length'],
                features['sepal_width'],
                features['petal_length'],
                features['petal_width']
            ]])

            try:
                # Make prediction
                prediction_index = model.predict(input_data) # Returns array [index]
                predicted_class_name = class_names[prediction_index[0]]

                # Optional: Get probabilities if the model supports it
                try:
                   probabilities = model.predict_proba(input_data)
                   # Create a dictionary mapping class names to probabilities
                   probability_dict = {name: prob for name, prob in zip(class_names, probabilities[0])}
                except AttributeError:
                    # Handle models that don't have predict_proba (like some SVMs)
                    probability_dict = "Probabilities not available for this model type"


                # Return result
                return Response(
                    {
                        "predicted_species_index": int(prediction_index[0]), # Ensure index is int
                        "predicted_species_name": predicted_class_name,
                        "prediction_probabilities": probability_dict
                    },
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                 # Handle potential errors during prediction
                 return Response(
                    {"error": f"Prediction error: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)