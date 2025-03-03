from django.db import models

class Broadcast(models.Model):
    message = models.TextField("Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка #{self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
