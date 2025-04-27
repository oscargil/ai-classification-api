from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import numpy as np
import joblib
import os

class ModelTests(TestCase):
    """Tests for the ML model functionality"""
    
    def setUp(self):
        """Load the model and class names before running tests"""
        self.model = joblib.load('iris_model.joblib')
        self.class_names = joblib.load('iris_class_names.joblib')
        
    def test_model_exists(self):
        """Test that the model file exists and is loaded correctly"""
        self.assertIsNotNone(self.model, "Model should be loaded")
        self.assertIsNotNone(self.class_names, "Class names should be loaded")
        
    def test_model_prediction(self):
        """Test model predictions with known samples"""
        # Test case for Setosa
        setosa_sample = np.array([[5.1, 3.5, 1.4, 0.2]])  # Known Setosa measurements
        prediction = self.model.predict(setosa_sample)
        self.assertEqual(self.class_names[prediction[0]], 'setosa')
        
        # Test case for Versicolor
        versicolor_sample = np.array([[6.4, 3.2, 4.5, 1.5]])  # Known Versicolor measurements
        prediction = self.model.predict(versicolor_sample)
        self.assertEqual(self.class_names[prediction[0]], 'versicolor')
        
    def test_model_probability(self):
        """Test that probability predictions are valid"""
        sample = np.array([[5.1, 3.5, 1.4, 0.2]])
        probabilities = self.model.predict_proba(sample)[0]
        
        # Check probability sum to 1 (within floating point precision)
        self.assertAlmostEqual(sum(probabilities), 1.0)
        # Check probabilities are between 0 and 1
        self.assertTrue(all(0 <= p <= 1 for p in probabilities))

class APITests(APITestCase):
    """Tests for the API endpoints"""
    
    def setUp(self):
        """Set up data for the tests"""
        self.predict_url = reverse('predict')  # Make sure this matches your URL name
        self.valid_payload = {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        
    def test_valid_prediction_request(self):
        """Test prediction with valid data"""
        response = self.client.post(self.predict_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('prediction', response.data)
        self.assertIn('probability', response.data)
        
    def test_invalid_prediction_request(self):
        """Test prediction with invalid data"""
        invalid_payload = {
            "sepal_length": "invalid",
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        response = self.client.post(self.predict_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_missing_fields(self):
        """Test prediction with missing fields"""
        incomplete_payload = {
            "sepal_length": 5.1,
            "sepal_width": 3.5
        }
        response = self.client.post(self.predict_url, incomplete_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_prediction_bounds(self):
        """Test predictions with extreme values"""
        extreme_payload = {
            "sepal_length": 100.0,  # Unrealistic value
            "sepal_width": 100.0,
            "petal_length": 100.0,
            "petal_width": 100.0
        }
        response = self.client.post(self.predict_url, extreme_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Even with extreme values, we should get a valid prediction
        self.assertIn('prediction', response.data)
        self.assertIn('probability', response.data)

class SerializerTests(TestCase):
    """Tests for the serializers"""
    
    def test_input_serializer_validation(self):
        """Test input data validation"""
        from predictor.serializers import PredictionInputSerializer
        
        # Test valid data
        valid_data = {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        serializer = PredictionInputSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Test invalid data types
        invalid_data = {
            "sepal_length": "invalid",
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        serializer = PredictionInputSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        
        # Test missing fields
        incomplete_data = {
            "sepal_length": 5.1,
            "sepal_width": 3.5
        }
        serializer = PredictionInputSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
