from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Room, Category, Status

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'price', 'photo', 'category', 'status']
        labels = {
            'name': _("Nom"),
            'description': _("Description"),
            'price': _("Prix par nuit"),
            'photo': _("Photo"),
            'category': _("Catégorie"),
            'status': _("Statut"),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError(_("Le nom est requis."))
        return name

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': _("Nom"),
            'description': _("Description"),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError(_("Le nom est requis."))
        return name
    


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'  # ou les champs que tu veux
