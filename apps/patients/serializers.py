from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()


class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def validate_age(self, value):
        """Validate that age is within acceptable range."""
        if value < 0 or value > 150:
            raise serializers.ValidationError("Age must be between 0 and 150.")
        return value
