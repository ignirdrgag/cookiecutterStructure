from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Reservation
from ..serializers import ReservationSerializer
from ..tasks import send_reservation_confirmation

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'services/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ['room', 'check_in', 'check_out']
    template_name = 'services/reservation_form.html'
    success_url = reverse_lazy('services:reservation_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # Lancer la tâche Celery pour envoyer l'email
        send_reservation_confirmation.delay(self.object.id)
        return response

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    fields = ['room', 'check_in', 'check_out']
    template_name = 'services/reservation_form.html'
    success_url = reverse_lazy('services:reservation_list')

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'services/reservation_confirm_delete.html'
    success_url = reverse_lazy('services:reservation_list')

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        reservation = serializer.save(user=self.request.user)
        # Lancer la tâche Celery pour l'API
        send_reservation_confirmation.delay(reservation.id)