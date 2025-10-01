from django.db import models
from django.utils.translation import gettext_lazy as _
from blog_hotel.content.models import Room
from django.conf import settings

class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Utilisateur")
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name=_("Chambre")
    )
    check_in = models.DateField(verbose_name=_("Date d'arrivée"))
    check_out = models.DateField(verbose_name=_("Date de départ"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Créé le")
    )

    class Meta:
        verbose_name = _("Réservation")
        verbose_name_plural = _("Réservations")

    def __str__(self):
        return f"Réservation de {self.room} par {self.user} du {self.check_in} au {self.check_out}"