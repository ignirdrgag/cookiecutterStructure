from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from ..forms import ReservationForm
from ..models import Reservation
from blog_hotel.content.models import Room
from rest_framework import viewsets
from blog_hotel.services.models import Reservation
from ..serializers import ReservationSerializer
import json
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

class ReservationView(LoginRequiredMixin, View):
    template_name = 'pages/reservation/reservation_list.html'

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'check_in')
            reservations = Reservation.objects.all()
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

    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get('action')
            if action == 'create':
                return self._create_reservation(request)
            elif action == 'edit':
                return self._edit_reservation(request)
            elif action == 'delete':
                return self._delete_reservation(request)
            else:
                return JsonResponse({'success': False, 'message': _('Action non reconnue.')}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _create_reservation(self, request):
        try:
            form = ReservationForm(request.POST)
            if form.is_valid():
                reservation = form.save()
                return JsonResponse({'success': True, 'message': _('Réservation créée avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _edit_reservation(self, request):
        try:
            reservation_id = request.POST.get('reservation_id')
            reservation = Reservation.objects.get(pk=reservation_id)
            form = ReservationForm(request.POST, instance=reservation)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': _('Réservation mise à jour avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Réservation introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _delete_reservation(self, request):
        try:
            reservation_id = request.POST.get('reservation_id')
            reservation = Reservation.objects.get(pk=reservation_id)
            reservation.delete()
            return JsonResponse({'success': True, 'message': _('Réservation supprimée avec succès.')})
        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Réservation introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)



class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer