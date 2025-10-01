from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Category
from ..serializers import CategorySerializer

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'content/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'content/category_detail.html'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'content/category_form.html'
    success_url = reverse_lazy('content:category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'content/category_form.html'
    success_url = reverse_lazy('content:category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'content/category_confirm_delete.html'
    success_url = reverse_lazy('content:category_list')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]