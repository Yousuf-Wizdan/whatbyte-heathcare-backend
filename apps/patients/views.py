from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients.
    Only returns patients created by the authenticated user.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only patients created by the current user."""
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically assign the logged-in user as created_by."""
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Verify ownership before updating patient."""
        if serializer.instance.created_by != self.request.user:
            raise PermissionDenied("You don't have permission to update this patient.")
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """Create patient with error handling."""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": e.detail if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Failed to create patient. Please check your input."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        """Update patient with error handling."""
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
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to update patient. Please check your input."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        """Delete patient with error handling."""
        try:
            return super().destroy(request, *args, **kwargs)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to delete patient."},
                status=status.HTTP_400_BAD_REQUEST
            )

