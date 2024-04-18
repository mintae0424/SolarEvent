import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandParser
from pages.models import Event, EventTag

class Command(BaseCommand):
    help = "Load events from a CSV file to the databse"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to event file")

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.stdout.write(self.style.SUCCESS("Importing data from file"))

        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    event_date = datetime.strptime(row['Event date'], '%B %d, %Y').date()
                    event_name = row['Event name']
                    event_description = row['Event description']
                    event_tags = [tag.strip() for tag in row['Tags'].split(",")]

                    

                    event, created = Event.objects.update_or_create(
                        event_date = event_date,
                        event_name = event_name,
                        defaults = {
                            'event_description': event_description,
                        }
                    )

                    for tag in event_tags:
                        event_tag, tag_created = EventTag.objects.get_or_create(name=tag)
                        event.event_tags.add(event_tag)

                    event.save()
            self.stdout.write(self.style.SUCCESS("Successfully imported data from file"))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to import due to: {e}'))