from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'check_in', 'check_out', 'created_at')
    list_filter = ('check_in', 'check_out')
    search_fields = ('room__name', 'user__username')