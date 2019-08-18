import time

from django.core.management.base import BaseCommand

from hackernews.models import Item
from hackernews.parser import HackerNewsParser

TIME_SLEEP = 60 * 10


class Command(BaseCommand):
    help = 'Download and save the first 30 entries from Hacker News'

    def add_arguments(self, parser):
        parser.add_argument('--loop', action='store_true', help='Run loop')

    def handle(self, *args, **options):
        while True:
            parser = HackerNewsParser()
            parser.download()

            for item in parser.as_json():
                if Item.objects.filter(hacker_news_id=item['hacker_news_id']).exists():
                    continue

                Item.objects.create(**item)
                self.stdout.write(self.style.SUCCESS(f'Save hackernews post_id: {item["hacker_news_id"]}'))

            if not options['loop']:
                break

            self.stdout.write(self.style.SUCCESS(f'Sleep {TIME_SLEEP} seconds'))
            time.sleep(TIME_SLEEP)
