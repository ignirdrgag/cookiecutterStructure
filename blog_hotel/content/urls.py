from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.rooms_views import RoomListView, RoomDetailView, RoomCreateView, RoomUpdateView, RoomDeleteView, RoomViewSet
from .views.category_views import (
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, CategoryViewSet
)
from .views.status_views import (
    StatusListView, StatusDetailView, StatusCreateView, StatusUpdateView, StatusDeleteView, StatusViewSet
)

app_name = 'content'

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'statuses', StatusViewSet)

urlpatterns = [
    # Chambres
    path('', RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('room/create/', RoomCreateView.as_view(), name='room_create'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room_update'),
    path('room/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    # Catégories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    # Statuts
    path('status/', StatusListView.as_view(), name='status_list'),
    path('status/<int:pk>/', StatusDetailView.as_view(), name='status_detail'),
    path('status/create/', StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
    # APIs
    path('api/', include(router.urls)),
]