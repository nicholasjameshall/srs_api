from django.conf import settings
from django.db import models
from django.utils import timezone


class Word(models.Model):
    text = models.CharField(max_length=200)
    last_reviewed = models.DateTimeField(default=timezone.now)

    # Add the owner field
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # What happens when the user is deleted
    )

    def __str__(self):
        return f"{self.text} (last reviewed: {self.last_reviewed})"
