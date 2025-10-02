from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from blog_hotel.content.forms import StatusForm
from ..models import Status
from blog_hotel.content.models import Room
import json
from django.views import View

from django.core.serializers.json import DjangoJSONEncoder

class StatusView(LoginRequiredMixin, View):
    template_name = 'pages/statut/satuts_list.html'

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'name')
            statuses = Status.objects.all()
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

    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get('action')
            if action == 'create':
                return self._create_status(request)
            elif action == 'edit':
                return self._edit_status(request)
            elif action == 'delete':
                return self._delete_status(request)
            else:
                return JsonResponse({'success': False, 'message': _('Action non reconnue.')}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _create_status(self, request):
        try:
            form = StatusForm(request.POST)
            if form.is_valid():
                status = form.save()
                return JsonResponse({'success': True, 'message': _('Statut créé avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _edit_status(self, request):
        try:
            status_id = request.POST.get('status_id')
            status = Status.objects.get(pk=status_id)
            form = StatusForm(request.POST, instance=status)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': _('Statut mis à jour avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Status.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Statut introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _delete_status(self, request):
        try:
            status_id = request.POST.get('status_id')
            status = Status.objects.get(pk=status_id)
            if Room.objects.filter(status=status).exists():
                return JsonResponse({
                    'success': False,
                    'message': _('Ce statut est utilisé par des chambres.')
                }, status=400)
            status.delete()
            return JsonResponse({'success': True, 'message': _('Statut supprimé avec succès.')})
        except Status.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Statut introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)