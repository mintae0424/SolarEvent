from django.db import models

# Create your models here.
class EventTag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_date = models.DateField("event date")
    event_name = models.CharField(max_length=255)
    event_description = models.TextField()
    event_tags = models.ManyToManyField(EventTag, related_name="events")

    def __str__(self):
        return self.event_name
    
class Revision(models.Model):
    revision_id = models.IntegerField(unique=True)
    page_title = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    timestamp = models.DateTimeField("revision date")

    def __str__(self):
        return f'Revised {self.page_title} at {self.timestamp}'