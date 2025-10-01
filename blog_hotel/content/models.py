from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Nom"))  # ex: Disponible, Occupée, Maintenance

    class Meta:
        verbose_name = _("Statut")
        verbose_name_plural = _("Statuts")

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix par nuit"))
    photo = models.ImageField(upload_to='rooms/', blank=True, verbose_name=_("Photo"))  # Besoin de Pillow : déjà dans requirements
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_("Catégorie"))
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name=_("Statut"))

    class Meta:
        verbose_name = _("Chambre")
        verbose_name_plural = _("Chambres")

    def __str__(self):
        return self.name