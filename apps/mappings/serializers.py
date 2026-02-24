from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """Serializer for PatientDoctorMapping model."""
    
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']
    
    def validate(self, data):
        """Validate patient ownership and check for duplicate mappings."""
        patient = data.get('patient')
        doctor = data.get('doctor')
        request = self.context.get('request')
        
        # Validate patient ownership
        if request and patient:
            if patient.created_by != request.user:
                raise PermissionDenied("You don't have permission to assign doctors to this patient.")
        
        # Check for duplicate mapping (only on create, not update)
        if not self.instance and patient and doctor:
            if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
                raise serializers.ValidationError(
                    "This doctor is already assigned to this patient."
                )
        
        return data
    
    def to_representation(self, instance):
        """Add nested patient and doctor details for better readability."""
        representation = super().to_representation(instance)
        representation['patient_details'] = {
            'id': instance.patient.id,
            'name': instance.patient.name,
            'age': instance.patient.age,
            'gender': instance.patient.gender
        }
        representation['doctor_details'] = {
            'id': instance.doctor.id,
            'name': instance.doctor.name,
            'specialization': instance.doctor.specialization,
            'experience': instance.doctor.experience
        }
        return representation
