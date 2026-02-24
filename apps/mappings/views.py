from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from apps.patients.models import Patient
from apps.doctors.models import Doctor


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing patient-doctor mappings."""
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only mappings for patients created by the current user."""
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        )

    def perform_create(self, serializer):
        """Validate patient ownership before creating mapping."""
        patient = serializer.validated_data.get('patient')
        
        # Check if patient belongs to current user
        if patient.created_by != self.request.user:
            raise PermissionDenied("You can only assign doctors to your own patients.")
        
        serializer.save()
    
    def perform_update(self, serializer):
        """Verify ownership before updating mapping."""
        if serializer.instance.patient.created_by != self.request.user:
            raise PermissionDenied("You can only update mappings for your own patients.")
        serializer.save()

    def perform_destroy(self, instance):
        """Verify ownership before deleting mapping."""
        if instance.patient.created_by != self.request.user:
            raise PermissionDenied("You can only delete mappings for your own patients.")
        
        instance.delete()
    
    def create(self, request, *args, **kwargs):
        """Create mapping with comprehensive error handling."""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": e.detail if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        except IntegrityError:
            return Response(
                {"error": "This doctor is already assigned to this patient."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to create mapping. Please check your input."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        """Update mapping with error handling."""
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": e.detail if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {"error": "Mapping not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to update mapping. Please check your input."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        """Delete mapping with error handling."""
        try:
            return super().destroy(request, *args, **kwargs)
        except PermissionDenied as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {"error": "Mapping not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to delete mapping."},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def patient_mappings(self, request, patient_id=None):
        """Get all doctor mappings for a specific patient."""
        try:
            patient = Patient.objects.get(id=patient_id, created_by=request.user)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found or you don't have permission to access it."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        mappings = self.get_queryset().filter(patient=patient)
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)
