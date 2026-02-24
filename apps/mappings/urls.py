from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PatientDoctorMappingViewSet

router = SimpleRouter()
router.register(r'', PatientDoctorMappingViewSet, basename='mappings')

urlpatterns = [
    path('', include(router.urls)),
]
