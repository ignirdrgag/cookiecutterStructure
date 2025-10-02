from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Reservation
from django.utils import timezone

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'check_in', 'check_out']
        labels = {
            'room': _("Chambre"),
            'check_in': _("Date d'arrivée"),
            'check_out': _("Date de départ"),
        }
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in < timezone.now().date():
                raise forms.ValidationError(_("La date d'arrivée ne peut pas être dans le passé."))
            if check_out <= check_in:
                raise forms.ValidationError(_("La date de départ doit être après la date d'arrivée."))
        return cleaned_data