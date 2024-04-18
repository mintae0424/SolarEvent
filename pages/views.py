from django.shortcuts import render
from .models import Event, EventTag, Revision
from collections import defaultdict


def home(request):
    return render(request, 'pages/home.html')


def random_number(request):
    return render(request, 'pages/random_number.html')

def display_graph(request):
    titles = Revision.objects.order_by().values('page_title').distinct()

    revisions_by_title = {}
    months = set()

    for title in titles:
        page_title = title.get("page_title")
        revision_data = get_revision_data(page_title)
        revisions_by_title[page_title] = revision_data
        months.update(revision_data['x'])

    months = sorted(months)
    events = Event.objects.all()

    events_data = [{
        'month': event.event_date.strftime('%Y-%m'),
        'name': event.event_name,
        'tags': [tag.name for tag in event.event_tags.all()]
    } for event in events]

    tags_data = EventTag.objects.all().values_list('name', flat=True)

    return render(request, 'pages/graph.html', {
        "months_data": months,
        "revisions_data": revisions_by_title,
        "events_data": events_data,
        "tags_data": tags_data
    })

def get_revision_data(page_title):
    revisions = Revision.objects.filter(
        page_title=page_title
    ).order_by('timestamp')

    revisions_by_month = defaultdict(int)
    total_revisions = 0
    for revision in revisions:
        month = revision.timestamp.strftime('%Y-%m')
        total_revisions += 1
        revisions_by_month[month] = total_revisions

    months = sorted(set(revisions_by_month.keys()))
    revisions_data = [revisions_by_month[month] for month in months]
    

    return {
        'x': months,
        'y': revisions_data,
    }