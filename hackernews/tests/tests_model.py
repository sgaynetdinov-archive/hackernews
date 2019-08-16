from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from hackernews.models import Item


class ItemTest(TestCase):
    def setUp(self):
        self.data = {
            'hacker_news_id': 100500,
            'title': 'a' * 250,
            'url': 'b' * 250
        }

    def test_create(self):
        self.assertEqual(Item.objects.count(), 0)

        Item.objects.create(**self.data)

        self.assertEqual(Item.objects.count(), 1)

    def test_field_hacker_news_id_unique(self):
        Item.objects.create(**self.data)

        with self.assertRaisesMessage(IntegrityError, "UNIQUE constraint failed: hackernews_item.hacker_news_id"):
            Item.objects.create(**self.data)

    @freeze_time('2000-01-01 10:00')
    def test_field_created(self):
        item = Item.objects.create(**self.data)

        self.assertEqual(item.created, timezone.now())
