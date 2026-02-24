from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Doctor CRUD operations.
    
    Requires authentication for all operations.
    Provides full CRUD operations for doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Create doctor with error handling."""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": e.detail if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Failed to create doctor. Please check your input."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        """Update doctor with error handling."""
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": e.detail if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to update doctor. Please check your input."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        """Delete doctor with error handling."""
        try:
            return super().destroy(request, *args, **kwargs)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to delete doctor."},
                status=status.HTTP_400_BAD_REQUEST
            )
