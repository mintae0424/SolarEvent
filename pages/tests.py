import os
import tempfile
import csv
from django.test import TestCase
from django.core.management import call_command
from datetime import datetime
from pages.models import Event, EventTag, Revision

# Create your tests here.
class EventModelTest(TestCase):
    def setUp(self):
        EventTag.objects.create(name="A")
        EventTag.objects.create(name="B")

    def test_event_creation(self):
        """Test Event model can be created as expected"""
        event = Event.objects.create(
            event_date=datetime.now().date(),
            event_name="ABC",
            event_description="ABC"
        )
        tag1 = EventTag.objects.get(name="A")
        tag2 = EventTag.objects.get(name="B")
        event.event_tags.add(tag1, tag2)
        event.save()

        retrieved = Event.objects.get(event_name="ABC")
        self.assertEqual(retrieved.event_description, "ABC")
        self.assertTrue(retrieved.event_tags.filter(name="A").exists())
        self.assertTrue(retrieved.event_tags.filter(name="B").exists())

class EventTagModelTest(TestCase):
    def test_event_tag_creation(self):
        """Test EventTag model can be created as expected"""
        tag = EventTag.objects.create(
            name="A"
        )
        tag.save()

        retrieved = EventTag.objects.get(name="A")
        self.assertEqual(retrieved.name, tag.name)
        self.assertEqual(EventTag.objects.count(), 1)

class RevisionModelTest(TestCase):
    def test_revision_creation(self):
        """Test Revision model can be created as expected"""
        revision = Revision.objects.create(
            revision_id = 1,
            page_title= "ABC",
            user="A",
            timestamp=datetime.now().date(),
        )

        revision.save()

        retrieved = Revision.objects.get(revision_id=1)
        self.assertEqual(retrieved.page_title, "ABC")
        self.assertEqual(Revision.objects.count(), 1)



class LoadEventsTest(TestCase):
    def test_load_success(self):
        """Test to check if a CSV file with correct format will load successfully"""
        data = [
            ['Event date', 'Event name', 'Event description', 'Tags'],
            ['April 01, 2024', 'Event A', 'Description A', 'TagA'],
            ['April 02, 2024', 'Event B', 'Description B', 'TagB']
        ]
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', suffix='.csv') as temp:
            writer = csv.writer(temp)  # Specify the delimiter here
            for row in data:
                writer.writerow(row)
            temp.flush()
            temp.seek(0)
            call_command('load_events', temp.name)
            temp.close()
        
        
        os.unlink(temp.name)

        self.assertEqual(Event.objects.count(), 2)
        self.assertTrue(Event.objects.filter(event_name="Event A").exists())
        self.assertTrue(Event.objects.filter(event_name="Event B").exists())

    def test_load_failure(self):
        """Test to check if a CSV file with incorrect format will not load"""
        data = [
            ['Event date', 'Event name', 'Event description', 'Tags'],
            ['2024-04-01', 'Event A', 'Description A', 'TagA'],
            ['2024-04-02', 'Event B', 'Description B', 'TagB']
        ]
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', suffix='.csv') as temp:
            writer = csv.writer(temp)  # Specify the delimiter here
            for row in data:
                writer.writerow(row)
            temp.flush()
            temp.seek(0)
            call_command('load_events', temp.name)
            temp.close()
        
        
        os.unlink(temp.name)

        self.assertEqual(Event.objects.count(), 0)

    def test_upload_with_duplicate_tags(self):
        """Test to check that when duplicate tags exist, it does not create duplicates"""
        data = [
            ['Event date', 'Event name', 'Event description', 'Tags'],
            ['April 01, 2024', 'Event A', 'Description A', 'TagA'],
            ['April 02, 2024', 'Event B', 'Description B', 'TagB'],
            ['April 02, 2024', 'Event C', 'Description B', 'TagB']
        ]

        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', suffix='.csv') as temp:
            writer = csv.writer(temp)  # Specify the delimiter here
            for row in data:
                writer.writerow(row)
            temp.flush()
            temp.seek(0)
            call_command('load_events', temp.name)
            temp.close()
        
        
        os.unlink(temp.name)

        self.assertEqual(Event.objects.count(), 3)
        self.assertTrue(EventTag.objects.count(), 2)

    
    def test_upload_with_duplicate_events(self):
        """Test to check that when duplicate events exist, it does not create duplicates"""
        data = [
            ['Event date', 'Event name', 'Event description', 'Tags'],
            ['April 01, 2024', 'Event A', 'Description A', 'TagA'],
            ['April 02, 2024', 'Event B', 'Description B', 'TagB'],
            ['April 02, 2024', 'Event B', 'Description B', 'TagB']
        ]

        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', suffix='.csv') as temp:
            writer = csv.writer(temp)  # Specify the delimiter here
            for row in data:
                writer.writerow(row)
            temp.flush()
            temp.seek(0)
            call_command('load_events', temp.name)
            temp.close()
        
        
        os.unlink(temp.name)

        self.assertEqual(Event.objects.count(), 2)
        self.assertTrue(EventTag.objects.count(), 3)

    def test_upload_with_list_of_tags(self):
        """Test to check that upload works with multiple tags for a single event"""
        data = [
            ['Event date', 'Event name', 'Event description', 'Tags'],
            ['April 01, 2024', 'Event A', 'Description A', 'TagA, TagB, TagC'],
            ['April 02, 2024', 'Event B', 'Description B', 'TagD'],
        ]

        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', suffix='.csv') as temp:
            writer = csv.writer(temp)  # Specify the delimiter here
            for row in data:
                writer.writerow(row)
            temp.flush()
            temp.seek(0)
            call_command('load_events', temp.name)
            temp.close()
        
        
        os.unlink(temp.name)

        self.assertEqual(Event.objects.count(), 2)
        self.assertTrue(EventTag.objects.count(), 4)
