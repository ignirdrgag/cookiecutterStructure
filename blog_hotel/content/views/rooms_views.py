from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from ..forms import RoomForm
from blog_hotel.content.models import Room
import json
from blog_hotel.content.models import Category, Status
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

class RoomView(LoginRequiredMixin, View):
    template_name = 'pages/room/room_list.html'

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'name')
            rooms = Room.objects.all()
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

    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get('action')
            if action == 'create':
                return self._create_room(request)
            elif action == 'edit':
                return self._edit_room(request)
            elif action == 'delete':
                return self._delete_room(request)
            else:
                return JsonResponse({'success': False, 'message': _('Action non reconnue.')}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _create_room(self, request):
        try:
            form = RoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save()
                return JsonResponse({'success': True, 'message': _('Chambre créée avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _edit_room(self, request):
        try:
            room_id = request.POST.get('room_id')
            room = Room.objects.get(pk=room_id)
            form = RoomForm(request.POST, request.FILES, instance=room)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': _('Chambre mise à jour avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Chambre introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _delete_room(self, request):
        try:
            room_id = request.POST.get('room_id')
            room = Room.objects.get(pk=room_id)
            room.delete()
            return JsonResponse({'success': True, 'message': _('Chambre supprimée avec succès.')})
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Chambre introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)