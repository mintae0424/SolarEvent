import requests
from datetime import datetime
from django.core.management.base import BaseCommand, CommandParser
from pages.models import Revision

class Command(BaseCommand):
    help = "Fetch Wikipedia revision histories of selected title using MediaWiki"

    def add_arguments(self, parser):
        parser.add_argument('page_title', type=str, help="Page title of WikiPedia Page (ex: 'Solar cell')")
    
    def handle(self, *args, **options):
        page_title = options['page_title']
        self.stdout.write(self.style.SUCCESS(f'Fetching revision history for: {page_title}'))
        self.fetch_revisions(page_title)

    def fetch_revisions(self, page_title):
        session = requests.Session()
        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "prop": "revisions",
            "titles": page_title,
            "rvlimit": "100",
            "rvprop": "timestamp|user|ids",
            "format": "json"
        }

        try:
            while True:
                response = session.get(url=url, params=params)
                data = response.json()
                pages = data['query']['pages']

                for page in pages:
                    title = pages[page].get('title', '')
                    revisions = pages[page].get('revisions', [])
                    
                    for revision in revisions:
                        revision_id = revision.get('revid')
                        user = revision.get('user')
                        timestamp = datetime.strptime(revision.get('timestamp'), "%Y-%m-%dT%H:%M:%SZ")

                        Revision.objects.update_or_create(
                            revision_id = revision_id,
                            defaults = {
                                'page_title': title,
                                'user': user,
                                'timestamp': timestamp,
                            }
                        )
                
                if 'continue' not in data:
                    break

                params['rvcontinue'] = data['continue']['rvcontinue']
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch revisions due to: {e}'))