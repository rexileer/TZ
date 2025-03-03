from newsletters.models import Broadcast
from asgiref.sync import sync_to_async


@sync_to_async
def get_broadcast():
    try:
        broadcast = Broadcast.objects.filter(sent=False).first()
        return broadcast
    except Broadcast.DoesNotExist:
        return None
