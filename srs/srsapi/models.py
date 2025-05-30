from django.conf import settings
from django.db import models
from django.utils import timezone


class Word(models.Model):
    text = models.CharField(max_length=200)
    last_reviewed = models.DateTimeField(default=timezone.now)
    next_review = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=1)
    )
    repetitions = models.PositiveIntegerField(default=1)

    # Add the owner field
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # What happens when the user is deleted
    )

    class Meta:
        unique_together = ("owner", "text")

    def __str__(self):
        return f"{self.text} (last reviewed: {self.last_reviewed})"
