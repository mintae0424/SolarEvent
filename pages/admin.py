from django.contrib import admin
from .models import Event, EventTag, Revision

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_date', 'event_name', 'event_description', 'list_event_tags')

    def list_event_tags(self, obj):
        return ", ".join([tag.name for tag in obj.event_tags.all()])
    
    list_event_tags.short_description = "Event Tags"

admin.site.register(Event, EventAdmin)
admin.site.register(EventTag)
admin.site.register(Revision)