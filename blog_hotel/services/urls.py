from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.reservations_view import (
    ReservationListView,
    ReservationCreateView,
    ReservationUpdateView,
    ReservationDeleteView,
    ReservationViewSet
)

app_name = 'services'

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation_list'),
    path('create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation_update'),
    path('<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),
    path('api/', include(router.urls)),  # APIs à /services/api/reservations/
]