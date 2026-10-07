"""URL routing for the enrollments app (trampa E02: DefaultRouter genera las rutas).

Rutas generadas:
  GET    /api/enrollments/                  -> list
  POST   /api/enrollments/                  -> create
  GET    /api/enrollments/{id}/            -> retrieve
  PUT    /api/enrollments/{id}/            -> update
  PATCH  /api/enrollments/{id}/            -> partial_update
  DELETE /api/enrollments/{id}/            -> destroy
"""
from rest_framework.routers import DefaultRouter

from .views import EnrollmentViewSet

router = DefaultRouter()
router.register(r"", EnrollmentViewSet, basename="enrollment")

urlpatterns = router.urls