from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
import json
from django.core.serializers.json import DjangoJSONEncoder
from ..models import Room, Category, Status
from .serializers import RoomSerializer, CategorySerializer, StatusSerializer

class RoomViewSet(LoginRequiredMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    lookup_field = "id"
    template_name = 'content/room_list.html'

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'name')
            rooms = self.get_queryset()
            if search_query:
                rooms = rooms.filter(name__icontains=search_query)
            rooms = rooms.order_by(sort_by)
            rooms_json = list(rooms.values('id', 'name', 'description', 'price', 'category', 'status'))
            paginator = Paginator(rooms, 10)
            page_number = request.GET.get('page')
            rooms = paginator.get_page(page_number)
            context = {
                'title': _("Liste des chambres"),
                'rooms': rooms,
                'rooms_json': json.dumps(rooms_json, cls=DjangoJSONEncoder),
                'search_query': search_query,
                'total_rooms': paginator.count,
                'sort_by': sort_by,
                'categories': Category.objects.all(),
                'statuses': Status.objects.all(),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            context = {
                'title': _("Liste des chambres"),
                'rooms': [],
                'rooms_json': json.dumps([]),
                'search_query': search_query,
                'total_rooms': 0,
                'sort_by': 'name',
                'categories': [],
                'statuses': [],
            }
            return render(request, self.template_name, context, status=500)

    @action(detail=False, methods=['post'])
    def create_room(self, request):
        try:
            serializer = RoomSerializer(data=request.POST, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Chambre créée avec succès.')}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def edit_room(self, request, id=None):
        try:
            room = self.get_object()
            serializer = RoomSerializer(room, data=request.POST, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Chambre mise à jour avec succès.')}, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Room.DoesNotExist:
            return Response({'success': False, 'message': _('Chambre introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def delete_room(self, request, id=None):
        try:
            room = self.get_object()
            room.delete()
            return Response({'success': True, 'message': _('Chambre supprimée avec succès.')}, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({'success': False, 'message': _('Chambre introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryViewSet(LoginRequiredMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"
    template_name = 'content/category_list.html'

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'name')
            categories = self.get_queryset()
            if search_query:
                categories = categories.filter(name__icontains=search_query)
            categories = categories.order_by(sort_by)
            categories_json = list(categories.values('id', 'name', 'description'))
            paginator = Paginator(categories, 10)
            page_number = request.GET.get('page')
            categories = paginator.get_page(page_number)
            context = {
                'title': _("Liste des catégories"),
                'categories': categories,
                'categories_json': json.dumps(categories_json, cls=DjangoJSONEncoder),
                'search_query': search_query,
                'total_categories': paginator.count,
                'sort_by': sort_by,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            context = {
                'title': _("Liste des catégories"),
                'categories': [],
                'categories_json': json.dumps([]),
                'search_query': search_query,
                'total_categories': 0,
                'sort_by': 'name',
            }
            return render(request, self.template_name, context, status=500)

    @action(detail=False, methods=['post'])
    def create_category(self, request):
        try:
            serializer = CategorySerializer(data=request.POST, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Catégorie créée avec succès.')}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def edit_category(self, request, id=None):
        try:
            category = self.get_object()
            serializer = CategorySerializer(category, data=request.POST, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Catégorie mise à jour avec succès.')}, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'success': False, 'message': _('Catégorie introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def delete_category(self, request, id=None):
        try:
            category = self.get_object()
            if Room.objects.filter(category=category).exists():
                return Response({
                    'success': False,
                    'message': _('Cette catégorie est utilisée par des chambres.')
                }, status=status.HTTP_400_BAD_REQUEST)
            category.delete()
            return Response({'success': True, 'message': _('Catégorie supprimée avec succès.')}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'success': False, 'message': _('Catégorie introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StatusViewSet(LoginRequiredMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    lookup_field = "id"
    template_name = 'content/status_list.html'

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'name')
            statuses = self.get_queryset()
            if search_query:
                statuses = statuses.filter(name__icontains=search_query)
            statuses = statuses.order_by(sort_by)
            statuses_json = list(statuses.values('id', 'name'))
            paginator = Paginator(statuses, 10)
            page_number = request.GET.get('page')
            statuses = paginator.get_page(page_number)
            context = {
                'title': _("Liste des statuts"),
                'statuses': statuses,
                'statuses_json': json.dumps(statuses_json, cls=DjangoJSONEncoder),
                'search_query': search_query,
                'total_statuses': paginator.count,
                'sort_by': sort_by,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            context = {
                'title': _("Liste des statuts"),
                'statuses': [],
                'statuses_json': json.dumps([]),
                'search_query': search_query,
                'total_statuses': 0,
                'sort_by': 'name',
            }
            return render(request, self.template_name, context, status=500)

    @action(detail=False, methods=['post'])
    def create_status(self, request):
        try:
            serializer = StatusSerializer(data=request.POST, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Statut créé avec succès.')}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def edit_status(self, request, id=None):
        try:
            status = self.get_object()
            serializer = StatusSerializer(status, data=request.POST, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Statut mis à jour avec succès.')}, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Status.DoesNotExist:
            return Response({'success': False, 'message': _('Statut introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def delete_status(self, request, id=None):
        try:
            status = self.get_object()
            if Room.objects.filter(status=status).exists():
                return Response({
                    'success': False,
                    'message': _('Ce statut est utilisé par des chambres.')
                }, status=status.HTTP_400_BAD_REQUEST)
            status.delete()
            return Response({'success': True, 'message': _('Statut supprimé avec succès.')}, status=status.HTTP_200_OK)
        except Status.DoesNotExist:
            return Response({'success': False, 'message': _('Statut introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)