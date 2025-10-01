from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Room, Category, Status
from ..serializers import RoomSerializer, CategorySerializer, StatusSerializer  # Crée serializers.py

# Web views (CRUD)
class RoomListView(ListView):
    model = Room
    template_name = 'content/room_list.html'
    context_object_name = 'rooms'

class RoomDetailView(DetailView):
    model = Room
    template_name = 'content/room_detail.html'

class RoomCreateView(CreateView):
    model = Room
    fields = ['name', 'description', 'price', 'photo', 'category', 'status']
    template_name = 'content/room_form.html'
    success_url = reverse_lazy('content:room_list')

class RoomUpdateView(UpdateView):
    model = Room
    fields = ['name', 'description', 'price', 'photo', 'category', 'status']
    template_name = 'content/room_form.html'
    success_url = reverse_lazy('content:room_list')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'content/room_confirm_delete.html'
    success_url = reverse_lazy('content:room_list')

# API ViewSets (avec Spectacular auto-doc)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]  # Ou custom

# Similaire pour CategoryViewSet, StatusViewSet