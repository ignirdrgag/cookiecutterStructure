from celery import shared_task

@shared_task
def update_room_status(room_id):
    # Ex: Changer statut après réservation
    pass