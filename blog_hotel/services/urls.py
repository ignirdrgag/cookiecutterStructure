from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.reservations_view import ReservationView, ReservationViewSet

app_name = 'services'

# Router DRF pour l'API
router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    # Vue principale pour le rendu HTML
    path('', ReservationView.as_view(), name='reservation_list'),
    
    # API REST
    path('api/', include(router.urls)),
]
