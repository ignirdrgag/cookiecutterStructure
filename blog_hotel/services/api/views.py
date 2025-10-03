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
from ..models import Reservation
from .serializers import ReservationSerializer
from content.models import Room

class ReservationViewSet(LoginRequiredMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    lookup_field = "id"
    template_name = 'services/reservation_list.html'

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'check_in')
            reservations = self.get_queryset()
            if search_query:
                reservations = reservations.filter(room__name__icontains=search_query)
            reservations = reservations.order_by(sort_by)
            reservations_json = list(reservations.values('id', 'room', 'check_in', 'check_out'))
            paginator = Paginator(reservations, 10)
            page_number = request.GET.get('page')
            reservations = paginator.get_page(page_number)
            context = {
                'title': _("Liste des réservations"),
                'reservations': reservations,
                'reservations_json': json.dumps(reservations_json, cls=DjangoJSONEncoder),
                'search_query': search_query,
                'total_reservations': paginator.count,
                'sort_by': sort_by,
                'rooms': Room.objects.all(),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            context = {
                'title': _("Liste des réservations"),
                'reservations': [],
                'reservations_json': json.dumps([]),
                'search_query': search_query,
                'total_reservations': 0,
                'sort_by': 'check_in',
                'rooms': [],
            }
            return render(request, self.template_name, context, status=500)

    @action(detail=False, methods=['post'])
    def create_reservation(self, request):
        try:
            serializer = ReservationSerializer(data=request.POST, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Réservation créée avec succès.')}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def edit_reservation(self, request, id=None):
        try:
            reservation = self.get_object()
            serializer = ReservationSerializer(reservation, data=request.POST, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': _('Réservation mise à jour avec succès.')}, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': _('Erreur de validation.'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Reservation.DoesNotExist:
            return Response({'success': False, 'message': _('Réservation introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def delete_reservation(self, request, id=None):
        try:
            reservation = self.get_object()
            reservation.delete()
            return Response({'success': True, 'message': _('Réservation supprimée avec succès.')}, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({'success': False, 'message': _('Réservation introuvable.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)