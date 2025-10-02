from django.urls import path
from .views.rooms_views import RoomView
from .views.status_views import StatusView
from .views.category_views import CategoryView  # supposons que tu aies cette view

app_name = 'content'

urlpatterns = [
    path('room/', RoomView.as_view(), name='room_list'),
    path('statut/', StatusView.as_view(), name='status_list'),
    path('categorie/', CategoryView.as_view(), name='category_list'),  # ajout des catégories
]
