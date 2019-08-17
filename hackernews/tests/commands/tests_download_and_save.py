from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from hackernews.models import Item


class DownloadAndSaveTest(TestCase):
    def setUp(self):
        self.assertEqual(Item.objects.count(), 0)

    @patch('hackernews.parser.HackerNewsParser.as_json')
    def test_call_command(self, mock):
        mock.return_value = [
                {'hacker_news_id': '20719095', 'url': 'https://async.rs/blog/announcing-async-std/#', 'title': 'Async-std: an async port of the Rust standard library'},
                {'hacker_news_id': '20715476', 'url': 'https://knobattack.com/', 'title': 'Key Negotiation of Bluetooth Attack'},
                {'hacker_news_id': '20715188', 'url': 'https://twitter.com/BenBajarin/status/1162048579654963200','title': 'US Gen Z and the iMessage Lock-In'},
                {'hacker_news_id': '20717238', 'url': 'https://jobs.lever.co/buildzoom','title': 'BuildZoom (YC W13) is hiring – Help us make remodeling cheaper'},
            ]

        call_command('download_and_save')

        self.assertEqual(Item.objects.count(), 4)
        self.assertListEqual(
            list(Item.objects.order_by('id').values_list('hacker_news_id', flat=True)),
            [20719095, 20715476, 20715188, 20717238]
        )

    @patch('hackernews.parser.HackerNewsParser.as_json')
    def test_hacker_news_id_not_unique(self, mock):
        mock.return_value = [
            {'hacker_news_id': '20719095', 'url': 'https://async.rs/blog/announcing-async-std/#', 'title': 'Async-std: an async port of the Rust standard library'},
            {'hacker_news_id': '20715476', 'url': 'https://knobattack.com/', 'title': 'Key Negotiation of Bluetooth Attack'},
            {'hacker_news_id': '20715476', 'url': 'https://twitter.com/BenBajarin/status/1162048579654963200', 'title': 'US Gen Z and the iMessage Lock-In'},
        ]

        call_command('download_and_save')

        self.assertEqual(Item.objects.count(), 2)
        self.assertListEqual(
            list(Item.objects.order_by('id').values_list('hacker_news_id', flat=True)),
            [20719095, 20715476]
        )
