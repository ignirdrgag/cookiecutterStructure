from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from ..forms import CategoryForm
from blog_hotel.content.models import Category
import json
from blog_hotel.content.models import Room, Status
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

class CategoryView(LoginRequiredMixin, View):
    template_name = 'pages/categorie/category_list.html'

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            sort_by = request.GET.get('sort_by', 'name')
            categories = Category.objects.all()
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

    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get('action')
            if action == 'create':
                return self._create_category(request)
            elif action == 'edit':
                return self._edit_category(request)
            elif action == 'delete':
                return self._delete_category(request)
            else:
                return JsonResponse({'success': False, 'message': _('Action non reconnue.')}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _create_category(self, request):
        try:
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                return JsonResponse({'success': True, 'message': _('Catégorie créée avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _edit_category(self, request):
        try:
            category_id = request.POST.get('category_id')
            category = Category.objects.get(pk=category_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': _('Catégorie mise à jour avec succès.')})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'message': _('Erreur de validation.'), 'errors': errors}, status=400)
        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Catégorie introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def _delete_category(self, request):
        try:
            category_id = request.POST.get('category_id')
            category = Category.objects.get(pk=category_id)
            if Room.objects.filter(category=category).exists():
                return JsonResponse({
                    'success': False,
                    'message': _('Cette catégorie est utilisée par des chambres.')
                }, status=400)
            category.delete()
            return JsonResponse({'success': True, 'message': _('Catégorie supprimée avec succès.')})
        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Catégorie introuvable.')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)