from django.contrib import admin
from .models import Broadcast

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "sent", "message")
