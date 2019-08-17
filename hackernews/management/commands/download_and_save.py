from django.core.management.base import BaseCommand

from hackernews.models import Item
from hackernews.parser import HackerNewsParser


class Command(BaseCommand):
    help = 'Download and save the first 30 entries from Hacker News'

    def handle(self, *args, **options):
        parser = HackerNewsParser()
        parser.download()

        for item in parser.as_json():
            if Item.objects.filter(hacker_news_id=item['hacker_news_id']).exists():
                continue

            Item.objects.create(**item)
