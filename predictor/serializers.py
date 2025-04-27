# predictor/serializers.py
from rest_framework import serializers

class IrisFeaturesSerializer(serializers.Serializer):
    """ Serializer to validate input Iris features """
    sepal_length = serializers.FloatField()
    sepal_width = serializers.FloatField()
    petal_length = serializers.FloatField()
    petal_width = serializers.FloatField()

    def validate(self, data):
        for key, value in data.items():
            if value < 0:
                raise serializers.ValidationError(f"{key} must be non-negative.")
        return data