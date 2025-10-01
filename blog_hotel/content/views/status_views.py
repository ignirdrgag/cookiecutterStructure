from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Status
from ..serializers import StatusSerializer

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'content/status_list.html'
    context_object_name = 'statuses'

class StatusDetailView(LoginRequiredMixin, DetailView):
    model = Status
    template_name = 'content/status_detail.html'

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'content/status_form.html'
    success_url = reverse_lazy('content:status_list')

class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'content/status_form.html'
    success_url = reverse_lazy('content:status_list')

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'content/status_confirm_delete.html'
    success_url = reverse_lazy('content:status_list')

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]