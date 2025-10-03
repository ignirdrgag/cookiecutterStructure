import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import Client
from blog_hotel.services.models import Reservation
from blog_hotel.content.models import Room

@pytest.mark.django_db
def test_get_reservations_list(client):
    # Création d’un utilisateur + login
    user = User.objects.create_user(username="kruger", password="123456")
    client.login(username="kruger", password="123456")

    # Création de Room + Reservation
    room = Room.objects.create(name="Chambre VIP", capacity=2)
    Reservation.objects.create(room=room, check_in=timezone.now(), check_out=timezone.now())

    url = reverse("reservation_list")  # Vérifie que ton urlpattern a bien ce name
    response = client.get(url)

    assert response.status_code == 200
    assert b"Liste des r\xc3\xa9servations" in response.content  # Vérifie titre dans le template
    assert "reservations_json" in response.context


@pytest.mark.django_db
def test_create_reservation(client):
    user = User.objects.create_user(username="kruger", password="123456")
    client.login(username="kruger", password="123456")

    room = Room.objects.create(name="Suite présidentielle", capacity=2)

    url = reverse("reservation_list")  # même vue ReservationView
    response = client.post(url, {
        "action": "create",
        "room": room.id,
        "check_in": timezone.now(),
        "check_out": timezone.now(),
    })

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Réservation créée avec succès" in data["message"]


@pytest.mark.django_db
def test_edit_reservation(client):
    user = User.objects.create_user(username="kruger", password="123456")
    client.login(username="kruger", password="123456")

    room = Room.objects.create(name="Chambre Luxe", capacity=2)
    reservation = Reservation.objects.create(room=room, check_in=timezone.now(), check_out=timezone.now())

    url = reverse("reservation_list")
    response = client.post(url, {
        "action": "edit",
        "reservation_id": reservation.id,
        "room": room.id,
        "check_in": timezone.now(),
        "check_out": timezone.now(),
    })

    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.django_db
def test_delete_reservation(client):
    user = User.objects.create_user(username="kruger", password="123456")
    client.login(username="kruger", password="123456")

    room = Room.objects.create(name="Chambre Standard", capacity=2)
    reservation = Reservation.objects.create(room=room, check_in=timezone.now(), check_out=timezone.now())

    url = reverse("reservation_list")
    response = client.post(url, {"action": "delete", "reservation_id": reservation.id})

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert Reservation.objects.count() == 0
