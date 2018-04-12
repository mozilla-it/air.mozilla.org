from django.db import models


class Event(models.Model):
    # max length comes from their docs
    event_key = models.PositiveIntegerField()
    title = models.CharField(max_length=355)
    description = models.TextField()
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    def __str__(self):
        return self.title
