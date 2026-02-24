from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model."""
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'experience', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
