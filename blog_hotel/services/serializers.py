from rest_framework import serializers
from .models import Reservation
from blog_hotel.content.models import Room
from blog_hotel.content.serializers import RoomSerializer

class ReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True
    )

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room', 'room_id', 'check_in', 'check_out', 'created_at']
        read_only_fields = ['user', 'created_at']